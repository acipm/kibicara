# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

""" API classes for implementing bots for platforms. """

from asyncio import create_task, Queue
from kibicara.model import BadWord, Trigger
from logging import getLogger
from re import match


logger = getLogger(__name__)


class Message:
    """The Message object that is send through the censor.

    Examples:
        ```
        message = Message('Message sent by a user from platform xyz', xyz_message_id=123)
        ```

    Args:
        text (str): The message text
        **kwargs (object, optional): Other platform-specific data.

    Attributes:
        text (str): The message text
        **kwargs (object, optional): Other platform-specific data.
    """

    def __init__(self, text, **kwargs):
        self.text = text
        self.__dict__.update(kwargs)


class Censor:
    """ The superclass for a platform bot.

    The censor is the superclass for every platform bot. It distributes a message to all
    other bots from the same hood if it passes the message filter. It provides methods
    to start and stop the bot and an overwritable stub for a starting routine.

    Examples:
        ```
        class XYZPlatform(Censor):
            def __init__(self, xyz_model):
                super().__init__(xyz_model.hood)
            ...
            async def run(self):
                await gather(self.poll(), self.push())
            ...
            async def poll(self):
                while True:
                    # XXX get text message from platform xyz
                    await self.publish(Message(text))
            ...
            async def push(self):
                while True:
                    message = await self.receive()
                    # XXX send message.text to platform xyz
        ```

    Args:
        hood (Hood): A Hood Model object

    Attributes:
        hood (Hood): A Hood Model object
    """

    __instances = {}

    def __init__(self, hood):
        self.hood = hood
        self._inbox = Queue()
        self.__task = None
        self.__hood_censors = self.__instances.setdefault(hood.id, [])
        self.__hood_censors.append(self)

    def start(self):
        """ Start the bot.

        Note: This will be called by a spawner, a platform bot should not call this.
        """
        if self.__task is None:
            self.__task = create_task(self.__run())

    def stop(self):
        """ Stop the bot.

        Note: This will be called by a spawner, a platform bot should not call this.
        """
        if self.__task is not None:
            self.__task.cancel()
            self.__task = None

    async def __run(self):
        await self.hood.load()
        self.__task.set_name('%s %s' % (self.__class__.__name__, self.hood.name))
        await self.run()

    async def run(self):
        """ Entry point for a bot.

        Note: Override this in the derived bot class.
        """
        pass

    async def publish(self, message):
        """ Distribute a message to the bots in a hood.

        Args:
            message (Message): Message to distribute
        Returns (Boolean): returns True if message is accepted by Censor.
        """
        if not await self.__is_appropriate(message):
            return False
        for censor in self.__hood_censors:
            await censor._inbox.put(message)
        return True

    async def receive(self):
        """ Receive a message.

        Returns (Message): Received message
        """
        return await self._inbox.get()

    async def __is_appropriate(self, message):
        for badword in await BadWord.objects.filter(hood=self.hood).all():
            if match(badword.pattern, message.text):
                logger.debug('Matched bad word - dropped message: %s' % message.text)
                return False
        for trigger in await Trigger.objects.filter(hood=self.hood).all():
            if match(trigger.pattern, message.text):
                logger.debug('Matched trigger - passed message: %s' % message.text)
                return True
        logger.debug('Did not match any trigger - dropped message: %s' % message.text)
        return False


class Spawner:
    """ Spawns a bot with a specific bot model.

    Examples:
        ```
        class XYZPlatform(Censor):
            # bot class

        class XYZ(Model):
            # bot model

        spawner = Spawner(XYZ, XYZPlatform)
        ```

    Args:
        ORMClass (ORM Model subclass): A Bot Model object
        BotClass (Censor subclass): A Bot Class object

    Attributes:
        ORMClass (ORM Model subclass): A Hood Model object
        BotClass (Censor subclass): A Bot Class object
    """

    __instances = []

    def __init__(self, ORMClass, BotClass):
        self.ORMClass = ORMClass
        self.BotClass = BotClass
        self.__bots = {}
        self.__instances.append(self)

    @classmethod
    async def init_all(cls):
        """ Instantiate and start a bot for every row in the corresponding ORM model. """
        for spawner in cls.__instances:
            await spawner._init()

    async def _init(self):
        for item in await self.ORMClass.objects.all():
            self.start(item)

    def start(self, item):
        """ Instantiate and start a bot with the provided ORM object.

        Example:
            ```
            xyz = await XYZ.objects.create(hood=hood, **values.__dict__)
            spawner.start(xyz)
            ```

        Args:
            item (ORM Model object): Argument to the bot constructor
        """
        bot = self.__bots.setdefault(item.pk, self.BotClass(item))
        bot.start()

    def stop(self, item):
        """ Stop and delete a bot.

        Args:
            item (ORM Model object): ORM object corresponding to bot.
        """
        bot = self.__bots.pop(item.pk, None)
        if bot is not None:
            bot.stop()

    def get(self, item):
        """ Get a running bot.

        Args:
            item (ORM Model object): ORM object corresponding to bot.
        """
        return self.__bots.get(item.pk)

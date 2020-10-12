# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

"""API classes for implementing bots for platforms."""

from asyncio import Queue, create_task
from enum import Enum, auto
from logging import getLogger
from re import IGNORECASE, search

from kibicara.model import BadWord, Trigger

logger = getLogger(__name__)


class Message:
    """The Message object that is send through the censor.

    Examples:
        ```
        message = Message('Message sent from platform xyz', xyz_message_id=123)
        ```

    Attributes:
        text (str): The message text
        **kwargs (object, optional): Other platform-specific data.
    """

    def __init__(self, text, **kwargs):
        self.text = text
        self.__dict__.update(kwargs)


class BotStatus(Enum):
    INSTANTIATED = auto()
    RUNNING = auto()
    STOPPED = auto()


class Censor:
    """The superclass for a platform bot.

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

    Attributes:
        hood (Hood): A Hood Model object
    """

    __instances = {}

    def __init__(self, hood):
        self.hood = hood
        self.enabled = True
        self._inbox = Queue()
        self.__task = None
        self.__hood_censors = self.__instances.setdefault(hood.id, [])
        self.__hood_censors.append(self)
        self.status = BotStatus.INSTANTIATED

    def start(self):
        """Start the bot."""
        if self.__task is None:
            self.__task = create_task(self.__run())

    def stop(self):
        """Stop the bot."""
        if self.__task is not None:
            self.__task.cancel()

    async def __run(self):
        await self.hood.load()
        self.__task.set_name('{0} {1}'.format(self.__class__.__name__, self.hood.name))
        try:
            self.status = BotStatus.RUNNING
            await self.run()
        except Exception as e:
            logger.exception(e)
        finally:
            self.__task = None
            self.status = BotStatus.STOPPED

    async def run(self):
        """Entry point for a bot.

        Note: Override this in the derived bot class.
        """
        pass

    @classmethod
    async def destroy_hood(cls, hood):
        """Remove all of its database entries.

        Note: Override this in the derived bot class.
        """
        pass

    async def publish(self, message):
        """Distribute a message to the bots in a hood.

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
        """Receive a message.

        Returns (Message): Received message
        """
        return await self._inbox.get()

    async def __is_appropriate(self, message):
        for badword in await BadWord.objects.filter(hood=self.hood).all():
            if search(badword.pattern, message.text, IGNORECASE):
                logger.debug(
                    'Matched bad word - dropped message: {0}'.format(message.text)
                )
                return False
        for trigger in await Trigger.objects.filter(hood=self.hood).all():
            if search(trigger.pattern, message.text, IGNORECASE):
                logger.debug(
                    'Matched trigger - passed message: {0}'.format(message.text)
                )
                return True
        logger.debug(
            'Did not match any trigger - dropped message: {0}'.format(message.text)
        )
        return False


class Spawner:
    """Spawns a bot with a specific bot model.

    Examples:
        ```
        class XYZPlatform(Censor):
            # bot class

        class XYZ(Model):
            # bot model

        spawner = Spawner(XYZ, XYZPlatform)
        ```

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
        """Instantiate and start a bot for every row in the corresponding ORM model."""
        for spawner in cls.__instances:
            await spawner._init()

    @classmethod
    async def destroy_hood(cls, hood):
        for spawner in cls.__instances:
            for pk in list(spawner.__bots):
                bot = spawner.__bots[pk]
                if bot.hood.id == hood.id:
                    del spawner.__bots[pk]
                    bot.stop()
            await spawner.BotClass.destroy_hood(hood)

    async def _init(self):
        for item in await self.ORMClass.objects.all():
            self.start(item)

    def start(self, item):
        """Instantiate and start a bot with the provided ORM object.

        Example:
            ```
            xyz = await XYZ.objects.create(hood=hood, **values.__dict__)
            spawner.start(xyz)
            ```

        Args:
            item (ORM Model object): Argument to the bot constructor
        """
        bot = self.__bots.setdefault(item.pk, self.BotClass(item))
        if bot.enabled:
            bot.start()

    def stop(self, item):
        """Stop and delete a bot.

        Args:
            item (ORM Model object): ORM object corresponding to bot.
        """
        bot = self.__bots.pop(item.pk, None)
        if bot is not None:
            bot.stop()

    def get(self, item):
        """Get a running bot.

        Args:
            item (ORM Model object): ORM object corresponding to bot.
        """
        return self.__bots.get(item.pk)

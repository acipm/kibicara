# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from asyncio import create_task, Queue
from kibicara.model import BadWord, Trigger
from logging import getLogger
from re import match


logger = getLogger(__name__)


class Message:
    def __init__(self, text, **kwargs):
        self.text = text
        self.__dict__.update(kwargs)


class Censor:
    instances = {}

    def __init__(self, hood):
        self.hood = hood
        self.inbox = Queue()
        self.task = None
        self.hood_censors = self.instances.setdefault(hood.id, [])
        self.hood_censors.append(self)

    def start(self):
        if self.task is None:
            self.task = create_task(self.__run())

    def stop(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def __run(self):
        await self.hood.load()
        self.task.set_name('%s %s' % (self.__class__.__name__, self.hood.name))
        await self.run()

    # override this in derived class
    async def run(self):
        pass

    async def publish(self, message):
        if not await self.__is_appropriate(message):
            return
        for censor in self.hood_censors:
            await censor.inbox.put(message)

    async def receive(self):
        return await self.inbox.get()

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
    instances = []

    def __init__(self, ORMClass, BotClass):
        self.ORMClass = ORMClass
        self.BotClass = BotClass
        self.bots = {}
        self.instances.append(self)

    @classmethod
    async def init_all(cls):
        for spawner in cls.instances:
            await spawner._init()

    async def _init(self):
        for item in await self.ORMClass.objects.all():
            self.start(item)

    def start(self, item):
        bot = self.bots.setdefault(item.pk, self.BotClass(item))
        bot.start()

    def stop(self, item):
        bot = self.bots.pop(item.pk, None)
        if bot is not None:
            bot.stop()

    def get(self, item):
        return self.bots.get(item.pk)

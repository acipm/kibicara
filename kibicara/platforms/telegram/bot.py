# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from aiogram import Bot, Dispatcher, exceptions, types
from asyncio import gather, sleep
from kibicara.config import config
from kibicara.platformapi import Censor, Message, Spawner
from kibicara.platforms.telegram.model import Telegram, TelegramUser
from logging import getLogger


logger = getLogger(__name__)


class TelegramBot(Censor):
    def __init__(self, telegram_model):
        super().__init__(telegram_model.hood)
        self.telegram_model = telegram_model
        self.bot = Bot(token=telegram_model.api_token)
        self.dp = Dispatcher(self.bot)
        self.dp.register_message_handler(self._send_welcome, commands=['start'])
        self.dp.register_message_handler(self._receive_message)

    async def run(self):
        await gather(self.dp.start_polling(), self.push())

    async def push(self):
        while True:
            message = await self.receive()
            logger.debug(
                'Received message from censor (%s): %s'
                % (self.telegram_model.hood.name, message.text)
            )
            for user in await TelegramUser.objects.filter(
                bot=self.telegram_model
            ).all():
                await self._send_message(user.user_id, message.text)

    async def _send_message(self, user_id, message):
        try:
            await self.bot.send_message(user_id, message, disable_notification=False)
        except exceptions.BotBlocked:
            logger.error(
                'Target [ID:%s] (%s): blocked by user'
                % (user_id, self.telegram_model.hood.name)
            )
        except exceptions.ChatNotFound:
            logger.error(
                'Target [ID:%s] (%s): invalid user ID'
                % (user_id, self.telegram_model.hood.name)
            )
        except exceptions.RetryAfter as e:
            logger.error(
                'Target [ID:%s] (%s): Flood limit is exceeded. Sleep %d seconds.'
                % (user_id, self.telegram_model.hood.name, e.timeout)
            )
            await sleep(e.timeout)
            return await self._send_message(user_id, text)
        except exceptions.UserDeactivated:
            logger.error(
                'Target [ID:%s] (%s): user is deactivated'
                % (user_id, self.telegram_model.hood.name)
            )
        except exceptions.TelegramAPIError:
            logger.exception(
                'Target [ID:%s] (%s): failed' % (user_id, self.telegram_model.hood.name)
            )

    async def _send_welcome(self, message: types.Message):
        try:
            if message.from_user.is_bot:
                await message.reply('Error: Bots can not join here.')
                return
            await TelegramUser.objects.create(
                user_id=message.from_user.id, bot=self.telegram_model
            )
            await message.reply(self.telegram_model.welcome_message)
        except IntegrityError:
            await message.reply('Error: You are already registered.')

    async def _receive_message(self, message: types.Message):
        if not message.text:
            await message.reply('Error: Only text messages are allowed.')
            return
        await self.publish(Message(message.text))


spawner = Spawner(Telegram, TelegramBot)

# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from asyncio import CancelledError, gather, sleep
from logging import getLogger
from sqlite3 import IntegrityError

from aiogram import Bot, Dispatcher, exceptions, types
from ormantic.exceptions import NoMatch

from kibicara.platformapi import Censor, Message, Spawner
from kibicara.platforms.telegram.model import Telegram, TelegramUser

logger = getLogger(__name__)


class TelegramBot(Censor):
    def __init__(self, telegram_model):
        super().__init__(telegram_model.hood)
        self.telegram_model = telegram_model
        self.enabled = self.telegram_model.enabled

    @classmethod
    async def destroy_hood(cls, hood):
        """Removes all its database entries."""
        for telegram in await Telegram.objects.filter(hood=hood).all():
            for user in await TelegramUser.objects.filter(bot=telegram).all():
                await user.delete()
            await telegram.delete()

    def _create_dispatcher(self):
        dp = Dispatcher(self.bot)
        dp.register_message_handler(self._send_welcome, commands=['start'])
        dp.register_message_handler(self._remove_user, commands=['stop'])
        dp.register_message_handler(self._send_help, commands=['help'])
        dp.register_message_handler(self._receive_message)
        return dp

    async def run(self):
        try:
            self.bot = Bot(token=self.telegram_model.api_token)
            self.dp = self._create_dispatcher()
            logger.debug('Bot {0} starting.'.format(self.telegram_model.hood.name))
            user = await self.bot.get_me()
            if user.username:
                await self.telegram_model.update(username=user.username)
            await gather(self.dp.start_polling(), self._push())
        except CancelledError:
            logger.debug('Bot {0} received Cancellation.'.format(
                self.telegram_model.hood.name))
            self.dp = None
            raise
        except exceptions.ValidationError:
            logger.debug('Bot {0} has invalid auth token.'.format(
                self.telegram_model.hood.name))
            await self.telegram_model.update(enabled=False)
        finally:
            logger.debug('Bot {0} stopped.'.format(self.telegram_model.hood.name))

    async def _push(self):
        while True:
            message = await self.receive()
            logger.debug(
                'Received message from censor ({0}): {1}'.format(
                    self.telegram_model.hood.name, message.text)
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
                'Target [ID:{0}] ({1}): blocked by user'.format(user_id,
                    self.telegram_model.hood.name)
            )
        except exceptions.ChatNotFound:
            logger.error(
                'Target [ID:{0}] ({1}): invalid user ID'.format(user_id,
                    self.telegram_model.hood.name)
            )
        except exceptions.RetryAfter as e:
            logger.error(
                'Target [ID:{0}] ({1}): Flood limit is exceeded.'.format(
                    user_id, self.telegram_model.hood.name
                )
                + 'Sleep {0} seconds.'.format(e.timeout)
            )
            await sleep(e.timeout)
            return await self._send_message(user_id, message)
        except exceptions.UserDeactivated:
            logger.error(
                'Target [ID:{0}] ({1}): user is deactivated'.format(user_id,
                    self.telegram_model.hood.name)
            )
        except exceptions.TelegramAPIError:
            logger.exception(
                'Target [ID:{0}] ({1}): failed'.format(user_id, self.telegram_model.hood.name)
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

    async def _remove_user(self, message: types.Message):
        try:
            telegram_user = await TelegramUser.objects.get(
                user_id=message.from_user.id, bot=self.telegram_model
            )
            await telegram_user.delete()
            await message.reply('You were removed successfully from this bot.')
        except NoMatch:
            await message.reply('Error: You are not subscribed to this bot.')

    async def _send_help(self, message: types.Message):
        if message.from_user.is_bot:
            await message.reply('Error: Bots can\'t be helped.')
            return
        await message.reply('Send messages here to broadcast them to your hood')

    async def _receive_message(self, message: types.Message):
        if not message.text:
            await message.reply('Error: Only text messages are allowed.')
            return
        await self.publish(Message(message.text))


spawner = Spawner(Telegram, TelegramBot)

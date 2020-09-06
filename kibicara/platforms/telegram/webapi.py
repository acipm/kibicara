# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from aiogram.bot.api import check_token
from aiogram import exceptions
from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.platforms.telegram.bot import spawner
from kibicara.platforms.telegram.model import Telegram, TelegramUser
from kibicara.webapi.hoods import get_hood, get_hood_unauthorized
from logging import getLogger
from sqlite3 import IntegrityError
from ormantic.exceptions import NoMatch
from pydantic import BaseModel, validator


logger = getLogger(__name__)


class BodyTelegram(BaseModel):
    api_token: str
    welcome_message: str = 'Welcome!'

    @validator('api_token')
    def valid_api_token(cls, value):
        try:
            check_token(value)
            return value
        except exceptions.ValidationError as e:
            raise ValueError(e)


class BodyTelegramPublic(BaseModel):
    username: str


async def get_telegram(telegram_id: int, hood=Depends(get_hood)):
    try:
        return await Telegram.objects.get(id=telegram_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()
telegram_callback_router = APIRouter()


@router.get(
    '/public',
    # TODO response_model,
    operation_id='get_telegrams_public',
)
async def telegram_read_all_public(hood=Depends(get_hood_unauthorized)):
    telegrambots = await Telegram.objects.filter(hood=hood).all()
    return [
        BodyTelegramPublic(username=telegrambot.username)
        for telegrambot in telegrambots
        if telegrambot.enabled == 1
    ]


@router.get(
    '/',
    # TODO response_model,
    operation_id='get_telegrams',
)
async def telegram_read_all(hood=Depends(get_hood)):
    return await Telegram.objects.filter(hood=hood).all()


@router.get(
    '/{telegram_id}',
    # TODO response_model,
    operation_id='get_telegram',
)
async def telegram_read(telegram=Depends(get_telegram)):
    return telegram


@router.delete(
    '/{telegram_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='delete_telegram',
)
async def telegram_delete(telegram=Depends(get_telegram)):
    spawner.stop(telegram)
    for user in await TelegramUser.objects.filter(bot=telegram).all():
        await user.delete()
    await telegram.delete()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model,
    operation_id='create_telegram',
)
async def telegram_create(
    response: Response, values: BodyTelegram, hood=Depends(get_hood)
):
    try:
        telegram = await Telegram.objects.create(hood=hood, **values.__dict__)
        spawner.start(telegram)
        response.headers['Location'] = '%d' % telegram.id
        return telegram
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.put(
    '/{telegram_id}',
    status_code=status.HTTP_202_ACCEPTED,
    # TODO response_model,
    operation_id='update_telegram',
)
async def telegram_update(values: BodyTelegram, telegram=Depends(get_telegram)):
    try:
        spawner.stop(telegram)
        await telegram.update(**values.__dict__)
        spawner.start(telegram)
        return telegram
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get(
    '/{telegram_id}/status',
    status_code=status.HTTP_200_OK,
    # TODO response_model,
    operation_id='status_telegram',
)
async def telegram_status(telegram=Depends(get_telegram)):
    return {'status': spawner.get(telegram).status.name}


@router.post(
    '/{telegram_id}/start',
    status_code=status.HTTP_200_OK,
    # TODO response_model,
    operation_id='start_telegram',
)
async def telegram_start(telegram=Depends(get_telegram)):
    await telegram.update(enabled=True)
    spawner.get(telegram).start()
    return {}


@router.post(
    '/{telegram_id}/stop',
    status_code=status.HTTP_200_OK,
    # TODO response_model,
    operation_id='stop_telegram',
)
async def telegram_stop(telegram=Depends(get_telegram)):
    await telegram.update(enabled=False)
    spawner.get(telegram).stop()
    return {}

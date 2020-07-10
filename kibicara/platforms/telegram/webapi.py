# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.config import config
from kibicara.platforms.telegram.bot import spawner
from kibicara.platforms.telegram.model import Telegram
from kibicara.webapi.hoods import get_hood
from logging import getLogger
from sqlite3 import IntegrityError
from ormantic.exceptions import NoMatch
from pydantic import BaseModel


logger = getLogger(__name__)


class BodyTelegram(BaseModel):
    api_token: str
    welcome_message: str = 'Welcome!'


async def get_telegram(telegram_id: int, hood=Depends(get_hood)):
    try:
        return await Telegram.objects.get(id=telegram_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()
telegram_callback_router = APIRouter()


@router.get('/')
async def telegram_read_all(hood=Depends(get_hood)):
    return await Telegram.objects.filter(hood=hood).all()


@router.get('/{telegram_id}')
async def telegram_read(telegram=Depends(get_telegram)):
    return telegram


@router.delete('/{telegram_id}', status_code=status.HTTP_204_NO_CONTENT)
async def telegram_delete(telegram=Depends(get_telegram)):
    spawner.stop(telegram)
    await telegram.delete()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def telegram_create(values: BodyTelegram, hood=Depends(get_hood)):
    try:
        telegram = await Telegram.objects.create(hood=hood, **values.__dict__)
        spawner.start(telegram)
        response.headers['Location'] = '%d' % telegram.id
        return telegram
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

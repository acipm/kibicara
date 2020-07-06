# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.platforms.email.bot import spawner
from kibicara.platforms.email.model import Email
from kibicara.platformapi import Message
from kibicara.webapi.hoods import get_hood
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from sqlite3 import IntegrityError


class BodyMessage(BaseModel):
    text: str
    to: str
    author: str
    secret: str


async def get_email_bot(to, hood=Depends(get_hood)):
    try:
        return await Email.objects.get(hood=to)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()


"""
@router.get('/')
async def test_read_all(hood=Depends(get_hood)):
    return await Email.objects.filter(hood=hood).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def test_create(response: Response, hood=Depends(get_hood)):
    try:
        test = await Email.objects.create(hood=hood)
        spawner.start(test)
        response.headers['Location'] = '%d' % test.id
        return test
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/{test_id}')
async def test_read(test=Depends(get_email_bot)):
    return test
"""


@router.post('/messages/')
async def email_message_create(message: BodyMessage):
    # get bot via "To:" header
    email_bot = await get_email_bot(message.to)
    # check API secret
    if message.secret is not email_bot.secret:
        return status.HTTP_401_UNAUTHORIZED
    # pass message.text to bot.py
    if await spawner.get(email_bot).publish(Message(message.text)):
        return status.HTTP_201_CREATED
    else:
        return status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

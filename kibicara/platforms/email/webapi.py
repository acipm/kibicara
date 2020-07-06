# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, status
from kibicara.platforms.email.bot import spawner
from kibicara.platforms.email.model import Email, EmailRecipients
from kibicara.platformapi import Message
from kibicara.config import config
from kibicara.email import send_email
from kibicara.model import Hood
from kibicara.webapi.hoods import get_hood
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from sqlite3 import IntegrityError
import jwt
from os import urandom


class BodyMessage(BaseModel):
    text: str
    to: str
    author: str
    secret: str


class Recipient(BaseModel):
    email: str


async def get_email_bot(to):
    hood_name = to.split('@')[0]
    hood = await Hood.objects.get(name=hood_name)
    try:
        return await Email.objects.get(hood=hood.id)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


hood_router = APIRouter()
mailbox_router = APIRouter()


"""
# get Email row?
@router.get('/')
async def test_read_all(hood=Depends(get_hood)):
    return await Email.objects.filter(hood=hood).all()
"""


@hood_router.post('/', status_code=status.HTTP_201_CREATED)
async def email_create(hood=Depends(get_hood)):
    try:
        emailbot = await Email.objects.create(hood=hood, secret=urandom(32))
        spawner.start(emailbot)
        return emailbot
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@hood_router.delete('/', status_code=status.HTTP_200_OK)
async def email_delete(hood=Depends(get_hood)):
    # who calls this function usually?
    email_bot = await Email.objects.get(hood=hood)
    spawner.stop(email_bot)
    await EmailRecipients.objects.delete_many(hood=hood)
    await email_bot.delete()


@hood_router.post('/recipient/')
async def email_recipient_create(recipient: Recipient, hood=Depends(get_hood)):
    token = jwt.encode({'email': recipient.email}, Email.secret).decode('ascii')
    confirm_link = (
        config['root_url'] + "api/" + hood.id + "/email/recipient/confirm/" + token
    )
    send_email(
        recipient.email,
        "Subscribe to Kibicara " + hood.name,
        sender=hood.name,
        body="To confirm your subscription, follow this link: " + confirm_link,
    )
    return status.HTTP_200_OK


@hood_router.post('/recipient/confirm/{token}')
async def email_recipient_confirm(token, hood=Depends(get_hood)):
    json = jwt.decode(token, Email.secret)
    try:
        await EmailRecipients.objects.create(hood=hood.id, email=json['email'])
        return status.HTTP_201_CREATED
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@hood_router.get('/unsubscribe/{token}', status_code=status.HTTP_200_OK)
async def email_recipient_unsubscribe(token, hood=Depends(get_hood)):
    json = jwt.decode(token)
    if hood.id is not json['hood']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    await EmailRecipients.objects.delete_many(hood=json['hood'], email=json['email'])


@mailbox_router.post('/messages/')
async def email_message_create(message: BodyMessage):
    # get bot via "To:" header
    email_bot = await get_email_bot(message.to)
    # check API secret
    if message.secret is not email_bot.secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # pass message.text to bot.py
    if await spawner.get(email_bot).publish(Message(message.text)):
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, status
from kibicara.platforms.email.bot import spawner
from kibicara.platforms.email.model import Email, EmailRecipients
from kibicara.platformapi import Message
from kibicara.config import config
from kibicara.webapi.hoods import get_hood
from kibicara.email import send_email
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from sqlite3 import IntegrityError
import jwt


class BodyMessage(BaseModel):
    text: str
    to: str
    author: str
    secret: str


class Recipient(BaseModel):
    hood: int
    email: str


async def get_email_bot(to, hood=Depends(get_hood)):
    try:
        return await Email.objects.get(hood=to)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()


"""
# get Email row?
@router.get('/')
async def test_read_all(hood=Depends(get_hood)):
    return await Email.objects.filter(hood=hood).all()

# create Email row
@router.post('/', status_code=status.HTTP_201_CREATED)
async def test_create(response: Response, hood=Depends(get_hood)):
    try:
        test = await Email.objects.create(hood=hood)
        spawner.start(test)
        response.headers['Location'] = '%d' % test.id
        return test
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
"""
# delete Email row


@router.post('/recipient/')
async def email_recipient_create(recipient: Recipient):
    token = jwt.encode({
        'email': recipient.email,
        'hood': recipient.hood,
    }, Email.secret).decode('ascii')
    confirm_link = config['root_url'] + "api/email/recipient/confirm/" + token
    hood_name = await get_hood(recipient.hood)
    send_email(recipient.email,
               "Subscribe to Kibicara " + hood_name,
               sender=hood_name,
               body="To confirm your subscription, follow this link: " + confirm_link)
    return status.HTTP_200_OK


@router.post('/recipient/confirm/<token>')
async def email_recipient_confirm(token):
    json = jwt.decode(token, Email.secret)
    try:
        await EmailRecipients.objects.create(hood=json['hood'], email=json['email'])
        return status.HTTP_201_CREATED
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

# delete EmailRecipient



@router.post('/messages/')
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

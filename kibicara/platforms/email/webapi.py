# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, status
from kibicara.platforms.email.bot import spawner
from kibicara.platforms.email.model import Email, EmailSubscribers
from kibicara.platformapi import Message
from kibicara.config import config
from kibicara.email import send_email
from kibicara.webapi.hoods import get_hood
from pydantic import BaseModel
from sqlite3 import IntegrityError
from nacl.encoding import URLSafeBase64Encoder
from nacl.secret import SecretBox
from os import urandom


class BodyMessage(BaseModel):
    """ This model shows which values are supplied by the MDA listener script. """

    text: str
    author: str
    secret: str


class Subscriber(BaseModel):
    """ This model holds the email address of a fresh subscriber. """

    email: str


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def email_create(hood=Depends(get_hood)):
    """ Create an Email bot. Call this when creating a hood.

    :param hood: Hood.id of the hood the Email bot is supposed to belong to.
    :return: Email row of the new email bot.
    """
    try:
        emailbot = await Email.objects.create(hood=hood, secret=urandom(32))
        spawner.start(emailbot)
        return emailbot
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete('/', status_code=status.HTTP_200_OK)
async def email_delete(hood=Depends(get_hood)):
    """ Delete an Email bot. Call this when deleting a hood.
    Stops and deletes the Email bot as well as all subscribers.

    :param hood: Hood the Email bot belongs to.
    """
    email_bot = await Email.objects.get(hood=hood.id)
    spawner.stop(email_bot)
    await EmailSubscribers.objects.delete_many(hood=hood.id)
    await email_bot.delete()


@router.post('/subscribe/')
async def email_subscribe(subscriber: Subscriber, hood=Depends(get_hood)):
    """ Send a confirmation mail to subscribe to messages via email.

    :param subscriber: Subscriber object, holds the email address.
    :param hood: Hood the Email bot belongs to.
    :return: Returns status code 200 after sending confirmation email.
    """
    secretbox = SecretBox(Email.secret)
    token = secretbox.encrypt(
        {'email': subscriber.email,}, encoder=URLSafeBase64Encoder
    )
    asciitoken = token.decode('ascii')
    confirm_link = (
        config['root_url'] + "api/" + hood.id + "/email/subscribe/confirm/" + asciitoken
    )
    send_email(
        subscriber.email,
        "Subscribe to Kibicara " + hood.name,
        sender=hood.name,
        body="To confirm your subscription, follow this link: " + confirm_link,
    )
    return status.HTTP_200_OK


@router.post('/subscribe/confirm/{token}')
async def email_subscribe_confirm(token, hood=Depends(get_hood)):
    """ Confirm a new subscriber and add them to the database.

    :param token: encrypted JSON token, holds the email of the subscriber.
    :param hood: Hood the Email bot belongs to.
    :return: Returns status code 200 after adding the subscriber to the database.
    """
    secretbox = SecretBox(Email.secret)
    json = secretbox.decrypt(token.encode('ascii'), encoder=URLSafeBase64Encoder)
    try:
        await EmailSubscribers.objects.create(hood=hood.id, email=json['email'])
        return status.HTTP_201_CREATED
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/unsubscribe/{token}', status_code=status.HTTP_200_OK)
async def email_unsubscribe(token, hood=Depends(get_hood)):
    """ Remove a subscriber from the database when they click on an unsubscribe link.

    :param token: encrypted JSON token, holds subscriber email + hood.id.
    :param hood: Hood the Email bot belongs to.
    """
    secretbox = SecretBox(Email.secret)
    json = secretbox.decrypt(token.encode('ascii'), encoder=URLSafeBase64Encoder)
    # If token.hood and url.hood are different, raise an error:
    if hood.id is not json['hood']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    await EmailSubscribers.objects.delete_many(hood=json['hood'], email=json['email'])


@router.post('/messages/')
async def email_message_create(message: BodyMessage, hood=Depends(get_hood)):
    """ Receive a message from the MDA and pass it to the censor.

    :param message: BodyMessage object, holds the message.
    :param hood: Hood the Email bot belongs to.
    :return: returns status code 201 if the message is accepted by the censor.
    """
    # get bot via "To:" header
    email_row = await Email.objects.get(hood=hood.id)
    # check API secret
    if message.secret is not email_row.secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # pass message.text to bot.py
    if await spawner.get(email_row).publish(Message(message.text)):
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

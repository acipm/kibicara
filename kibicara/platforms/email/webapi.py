# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara import email
from kibicara.platforms.email.bot import spawner
from kibicara.platforms.email.model import Email, EmailSubscribers
from kibicara.platformapi import Message
from kibicara.config import config
from kibicara.webapi.admin import from_token, to_token
from kibicara.webapi.hoods import get_hood, get_hood_unauthorized
from logging import getLogger
from ormantic.exceptions import NoMatch
from os import urandom
from pydantic import BaseModel
from smtplib import SMTPException
from sqlite3 import IntegrityError


logger = getLogger(__name__)


class BodyEmail(BaseModel):
    name: str


class BodyMessage(BaseModel):
    """ This model shows which values are supplied by the MDA listener script. """

    text: str
    secret: str


class BodySubscriber(BaseModel):
    """ This model holds the email address of a fresh subscriber. """

    email: str


async def get_email(email_id: int, hood=Depends(get_hood)):
    """ Get Email row by hood.
    You can specify an email_id to nail it down, but it works without as well.

    :param hood: Hood the Email bot belongs to.
    :return: Email row of the found email bot.
    """
    try:
        return await Email.objects.get(id=email_id, hood=hood)
    except NoMatch:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def get_subscriber(subscriber_id: int, hood=Depends(get_hood)):
    try:
        return await EmailSubscriber.objects.get(id=subscriber_id, hood=hood)
    except NoMatch:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# registers the routes, gets imported in /kibicara/webapi/__init__.py
router = APIRouter()


@router.get('/')
async def email_read_all(hood=Depends(get_hood)):
    return await Email.objects.filter(hood=hood).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def email_create(values: BodyEmail, response: Response, hood=Depends(get_hood)):
    """ Create an Email bot. Call this when creating a hood.

    :param hood: Hood row of the hood the Email bot is supposed to belong to.
    :return: Email row of the new email bot.
    """
    if not values.name.startswith('kibicara-'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Recipient address didn\'t start with kibicara-',
        )
    try:
        email = await Email.objects.create(
            hood=hood, secret=urandom(32).hex(), **values.__dict__
        )
        spawner.start(email)
        response.headers['Location'] = '%d' % hood.id
        return email
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/{email_id}')
async def email_read(email=Depends(get_email)):
    return email


@router.put('/{email_id}', status_code=status.HTTP_204_NO_CONTENT)
async def email_update(email=Depends(get_email)):
    await email.update()  # TODO


@router.delete('/{email_id}', status_code=status.HTTP_204_NO_CONTENT)
async def email_delete(email=Depends(get_email)):
    """ Delete an Email bot.
    Stops and deletes the Email bot.

    :param hood: Hood the Email bot belongs to.
    """
    await email.delete()


@router.post('/subscribe/', status_code=status.HTTP_202_ACCEPTED)
async def email_subscribe(
    subscriber: BodySubscriber, hood=Depends(get_hood_unauthorized)
):
    """ Send a confirmation mail to subscribe to messages via email.

    :param subscriber: Subscriber object, holds the email address.
    :param hood: Hood the Email bot belongs to.
    :return: Returns status code 200 after sending confirmation email.
    """
    token = to_token(hood=hood.id, email=subscriber.email)
    confirm_link = '%s/api/hoods/%d/email/subscribe/confirm/%s' % (
        config['root_url'],
        hood.id,
        token,
    )
    try:
        email.send_email(
            subscriber.email,
            "Subscribe to Kibicara " + hood.name,
            sender=hood.name,
            body='To confirm your subscription, follow this link: ' + confirm_link,
        )
        return {}
    except ConnectionRefusedError:
        logger.info(token)
        logger.error("Sending subscription confirmation email failed.", exc_info=True)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
    except SMTPException:
        logger.info(token)
        logger.error("Sending subscription confirmation email failed.", exc_info=True)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


@router.post('/subscribe/confirm/{token}', status_code=status.HTTP_201_CREATED)
async def email_subscribe_confirm(token, hood=Depends(get_hood_unauthorized)):
    """ Confirm a new subscriber and add them to the database.

    :param token: encrypted JSON token, holds the email of the subscriber.
    :param hood: Hood the Email bot belongs to.
    :return: Returns status code 200 after adding the subscriber to the database.
    """
    payload = from_token(token)
    # If token.hood and url.hood are different, raise an error:
    if hood.id is not payload['hood']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        await EmailSubscribers.objects.create(hood=hood.id, email=payload['email'])
        return {}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete('/unsubscribe/{token}', status_code=status.HTTP_204_NO_CONTENT)
async def email_unsubscribe(token, hood=Depends(get_hood_unauthorized)):
    """ Remove a subscriber from the database when they click on an unsubscribe link.

    :param token: encrypted JSON token, holds subscriber email + hood.id.
    :param hood: Hood the Email bot belongs to.
    """
    logger.warning("token is: " + token)
    payload = from_token(token)
    # If token.hood and url.hood are different, raise an error:
    if hood.id is not payload['hood']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    subscriber = await EmailSubscribers.objects.filter(
        hood=payload['hood'], email=payload['email']
    ).get()
    await subscriber.delete()


@router.get('/subscribers/')
async def subscribers_read_all(hood=Depends(get_hood)):
    return await EmailSubscribers.objects.filter(hood=hood).all()


@router.get('/subscribers/{subscriber_id}')
async def subscribers_read(subscriber=Depends(get_subscriber)):
    return subscriber


@router.post('/messages/', status_code=status.HTTP_201_CREATED)
async def email_message_create(
    message: BodyMessage, hood=Depends(get_hood_unauthorized)
):
    """ Receive a message from the MDA and pass it to the censor.

    :param message: BodyMessage object, holds the message.
    :param hood: Hood the Email bot belongs to.
    :return: returns status code 201 if the message is accepted by the censor.
    """
    for email in await Email.objects.filter(hood=hood).all():
        if message.secret == email.secret:
            # check API secret
            logger.warning(str(message))
            logger.warning(str(email))
            # pass message.text to bot.py
            if await spawner.get(hood).publish(Message(message.text)):
                logger.warning("Message was accepted: " + message.text)
                return {}
            else:
                logger.warning("Message was't accepted: " + message.text)
                raise HTTPException(
                    status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
                )
    logger.warning(
        "Someone is trying to submit an email without the correct API secret"
    )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

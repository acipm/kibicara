# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from logging import getLogger
from os import urandom
from smtplib import SMTPException
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, Response, status
from nacl import exceptions
from ormantic.exceptions import NoMatch
from pydantic import BaseModel, validator

from kibicara import email
from kibicara.config import config
from kibicara.platformapi import Message
from kibicara.platforms.email.bot import spawner
from kibicara.platforms.email.model import Email, EmailSubscribers
from kibicara.webapi.admin import from_token, to_token
from kibicara.webapi.hoods import get_hood, get_hood_unauthorized

logger = getLogger(__name__)


class BodyEmail(BaseModel):
    name: str

    @validator('name')
    def valid_prefix(cls, value):
        if not value.startswith('kibicara-'):
            raise ValueError('Recipient address didn\'t start with kibicara-')
        return value


class BodyEmailPublic(BaseModel):
    name: str


class BodyMessage(BaseModel):
    """ This model shows which values are supplied by the MDA listener script. """

    text: str
    secret: str


class BodySubscriber(BaseModel):
    """ This model holds the email address of a fresh subscriber. """

    email: str


async def get_email(email_id: int, hood=Depends(get_hood)):
    """Get Email row by hood.
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
        return await EmailSubscribers.objects.get(id=subscriber_id, hood=hood)
    except NoMatch:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# registers the routes, gets imported in /kibicara/webapi/__init__.py
router = APIRouter()


@router.get(
    '/public',
    # TODO response_model
    operation_id='get_emails_public',
)
async def email_read_all_public(hood=Depends(get_hood_unauthorized)):
    if hood.email_enabled:
        emails = await Email.objects.filter(hood=hood).all()
        return [BodyEmailPublic(name=email.name) for email in emails]
    return []


@router.get(
    '/',
    # TODO response_model
    operation_id='get_emails',
)
async def email_read_all(hood=Depends(get_hood)):
    return await Email.objects.filter(hood=hood).select_related('hood').all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model
    operation_id='create_email',
)
async def email_create(values: BodyEmail, response: Response, hood=Depends(get_hood)):
    """Create an Email bot. Call this when creating a hood.

    :param hood: Hood row of the hood the Email bot is supposed to belong to.
    :return: Email row of the new email bot.
    """
    try:
        email = await Email.objects.create(
            hood=hood, secret=urandom(32).hex(), **values.__dict__
        )
        response.headers['Location'] = str(hood.id)
        return email
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get(
    '/status',
    status_code=status.HTTP_200_OK,
    # TODO response_model
    operation_id='status_email',
)
async def email_status(hood=Depends(get_hood)):
    return {'status': spawner.get(hood).status.name}


@router.post(
    '/start',
    status_code=status.HTTP_200_OK,
    # TODO response_model
    operation_id='start_email',
)
async def email_start(hood=Depends(get_hood)):
    await hood.update(email_enabled=True)
    spawner.get(hood).start()
    return {}


@router.post(
    '/stop',
    status_code=status.HTTP_200_OK,
    # TODO response_model
    operation_id='stop_email',
)
async def email_stop(hood=Depends(get_hood)):
    await hood.update(email_enabled=False)
    spawner.get(hood).stop()
    return {}


@router.get(
    '/{email_id}',
    # TODO response_model
    operation_id='get_email',
)
async def email_read(email=Depends(get_email)):
    return email


@router.delete(
    '/{email_id}', status_code=status.HTTP_204_NO_CONTENT, operation_id='delete_email'
)
async def email_delete(email=Depends(get_email)):
    """Delete an Email bot.
    Stops and deletes the Email bot.

    :param hood: Hood the Email bot belongs to.
    """
    await email.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/subscribe/',
    status_code=status.HTTP_202_ACCEPTED,
    operation_id='subscribe',
    response_model=BaseModel,
)
async def email_subscribe(
    subscriber: BodySubscriber, hood=Depends(get_hood_unauthorized)
):
    """Send a confirmation mail to subscribe to messages via email.

    :param subscriber: Subscriber object, holds the email address.
    :param hood: Hood the Email bot belongs to.
    :return: Returns status code 200 after sending confirmation email.
    """
    token = to_token(hood=hood.id, email=subscriber.email)
    confirm_link = '{0}/hoods/{1}/email-confirm?token={2}'.format(
        config['frontend_url'],
        hood.id,
        token,
    )
    try:
        subs = await EmailSubscribers.objects.filter(email=subscriber.email).all()
        if subs:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        email.send_email(
            subscriber.email,
            'Subscribe to Kibicara {0}'.format(hood.name),
            body='To confirm your subscription, follow this link: {0}'.format(
                confirm_link
            ),
        )
        return {}
    except ConnectionRefusedError:
        logger.info(token)
        logger.error('Sending subscription confirmation email failed.', exc_info=True)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
    except SMTPException:
        logger.info(token)
        logger.error('Sending subscription confirmation email failed.', exc_info=True)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


@router.post(
    '/subscribe/confirm/{token}',
    status_code=status.HTTP_201_CREATED,
    operation_id='confirm_subscriber',
    response_model=BaseModel,
)
async def email_subscribe_confirm(token, hood=Depends(get_hood_unauthorized)):
    """Confirm a new subscriber and add them to the database.

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


@router.delete(
    '/unsubscribe/{token}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='unsubscribe',
)
async def email_unsubscribe(token, hood=Depends(get_hood_unauthorized)):
    """Remove a subscriber from the database when they click on an unsubscribe link.

    :param token: encrypted JSON token, holds subscriber email + hood.id.
    :param hood: Hood the Email bot belongs to.
    """
    try:
        logger.warning('token is: {0}'.format(token))
        payload = from_token(token)
        # If token.hood and url.hood are different, raise an error:
        if hood.id is not payload['hood']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        subscriber = await EmailSubscribers.objects.filter(
            hood=payload['hood'], email=payload['email']
        ).get()
        await subscriber.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except exceptions.CryptoError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/subscribers/',
    # TODO response_model
    operation_id='get_subscribers',
)
async def subscribers_read_all(hood=Depends(get_hood)):
    return await EmailSubscribers.objects.filter(hood=hood).all()


@router.get(
    '/subscribers/{subscriber_id}',
    # TODO response_model
    operation_id='get_subscriber',
)
async def subscribers_read(subscriber=Depends(get_subscriber)):
    return subscriber


@router.post(
    '/messages/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model
    operation_id='send_message',
)
async def email_message_create(
    message: BodyMessage, hood=Depends(get_hood_unauthorized)
):
    """Receive a message from the MDA and pass it to the censor.

    :param message: BodyMessage object, holds the message.
    :param hood: Hood the Email bot belongs to.
    :return: returns status code 201 if the message is accepted by the censor.
    """
    for receiver in await Email.objects.filter(hood=hood).all():
        if message.secret == receiver.secret:
            # pass message.text to bot.py
            if await spawner.get(hood).publish(Message(message.text)):
                logger.warning('Message was accepted: {0}'.format(message.text))
                return {}
            else:
                logger.warning('Message wasn\'t accepted: {0}'.format(message.text))
                raise HTTPException(
                    status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
                )
    logger.warning(
        'Someone is trying to submit an email without the correct API secret'
    )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

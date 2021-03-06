# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Christian Hagenest <c.hagenest@pm.me>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

"""REST API endpoints for hood admins."""

from datetime import datetime, timedelta
from logging import getLogger
from pickle import dumps, loads
from smtplib import SMTPException
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from nacl.encoding import URLSafeBase64Encoder
from nacl.exceptions import CryptoError
from nacl.secret import SecretBox
from ormantic.exceptions import NoMatch
from passlib.hash import argon2
from pydantic import BaseModel, validator

from kibicara import email
from kibicara.config import config
from kibicara.model import Admin, AdminHoodRelation, Hood
from kibicara.webapi.utils import delete_hood

logger = getLogger(__name__)


class BodyEmail(BaseModel):
    email: str


class BodyPassword(BaseModel):
    password: str

    @validator('password')
    def valid_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password is too short')
        return value


class BodyAdmin(BodyEmail, BodyPassword):
    pass


class BodyAccessToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/admin/login')
secret_box = SecretBox(bytes.fromhex(config['secret']))


def to_token(**kwargs):
    return secret_box.encrypt(dumps(kwargs), encoder=URLSafeBase64Encoder).decode(
        'ascii'
    )


def from_token(token):
    return loads(
        secret_box.decrypt(token.encode('ascii'), encoder=URLSafeBase64Encoder)
    )


async def get_auth(email, password):
    try:
        admin = await Admin.objects.get(email=email)
        if argon2.verify(password, admin.passhash):
            return admin
        raise ValueError
    except NoMatch:
        raise ValueError


async def get_admin(access_token=Depends(oauth2_scheme)):
    try:
        admin = await get_auth(**from_token(access_token))
    except (CryptoError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return admin


router = APIRouter()


@router.post(
    '/register/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BaseModel,
    operation_id='register',
)
async def admin_register(values: BodyAdmin):
    """Sends an email with a confirmation link.

    - **email**: E-Mail Address of new hood admin
    - **password**: Password of new hood admin
    """
    register_token = to_token(**values.__dict__)
    logger.debug('register_token={0}'.format(register_token))
    try:
        admin = await Admin.objects.filter(email=values.email).all()
        if admin:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        body = '{0}/confirm?token={1}'.format(config['frontend_url'], register_token)
        logger.debug(body)
        email.send_email(
            to=values.email,
            subject='Confirm Account',
            body=body,
        )
    except (ConnectionRefusedError, SMTPException):
        logger.exception('Email sending failed')
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
    return {}


@router.post(
    '/confirm/{register_token}',
    response_model=BodyAccessToken,
    operation_id='confirm',
)
async def admin_confirm(register_token: str):
    """Registration confirmation and account creation.

    - **register_token**: Registration token received in email from /register
    """
    try:
        values = from_token(register_token)
        passhash = argon2.hash(values['password'])
        await Admin.objects.create(email=values['email'], passhash=passhash)
        return BodyAccessToken(access_token=register_token)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.post(
    '/login/',
    response_model=BodyAccessToken,
    operation_id='login',
)
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get an access token.

    - **username**: Email of a registered hood admin
    - **password**: Password of a registered hood admin
    """
    try:
        await get_auth(form_data.username, form_data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password',
        )
    token = to_token(email=form_data.username, password=form_data.password)
    return BodyAccessToken(access_token=token)


@router.post(
    '/reset/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BaseModel,
    operation_id='reset',
)
async def admin_reset_password(values: BodyEmail):
    """Sends an email with a password reset link.

    - **email**: E-Mail Address of new hood admin
    - **password**: Password of new hood admin
    """
    register_token = to_token(datetime=datetime.now().isoformat(), **values.__dict__)
    logger.debug('register_token={0}'.format(register_token))
    try:
        admin = await Admin.objects.filter(email=values.email).all()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        body = '{0}/password-reset?token={1}'.format(
            config['frontend_url'], register_token
        )
        logger.debug(body)
        email.send_email(
            to=values.email,
            subject='Reset your password',
            body=body,
        )
    except (ConnectionRefusedError, SMTPException):
        logger.exception('Email sending failed')
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
    return {}


@router.post(
    '/reset/{reset_token}',
    response_model=BodyAccessToken,
    operation_id='confirm_reset',
)
async def admin_confirm_reset(reset_token: str, values: BodyPassword):
    try:
        token_values = from_token(reset_token)
        if (
            datetime.fromisoformat(token_values['datetime']) + timedelta(hours=3)
            < datetime.now()
        ):
            raise HTTPException(status_code=status.HTTP_410_GONE)
        passhash = argon2.hash(values.password)
        admins = await Admin.objects.filter(email=token_values['email']).all()
        if len(admins) != 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await admins[0].update(passhash=passhash)
        return BodyAccessToken(access_token=reset_token)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except CryptoError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/hoods/',
    # TODO response_model,
    operation_id='get_hoods_admin',
)
async def admin_hood_read_all(admin=Depends(get_admin)):
    """Get a list of all hoods of a given admin."""
    return (
        await AdminHoodRelation.objects.select_related('hood').filter(admin=admin).all()
    )


@router.get(
    '/',
    # TODO response_model,
    operation_id='get_admin',
)
async def admin_read(admin=Depends(get_admin)):
    """Get a list of all hoods of a given admin."""
    admin = await Admin.objects.filter(email=admin.email).all()
    if len(admin) != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return BodyEmail(email=admin[0].email)


@router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='delete_admin',
)
async def admin_delete(admin=Depends(get_admin)):
    hood_relations = (
        await AdminHoodRelation.objects.select_related('hood').filter(admin=admin).all()
    )
    for hood in hood_relations:
        admins = (
            await AdminHoodRelation.objects.select_related('admin')
            .filter(hood=hood.id)
            .all()
        )
        if len(admins) == 1 and admins[0].id == admin.id:
            actual_hood = await Hood.objects.filter(id=hood.id).all()
            await delete_hood(actual_hood[0])
    await admin.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from kibicara.email import send_email
from kibicara.model import Admin, AdminHoodRelation
from kibicara.config import config
from logging import getLogger
from nacl.encoding import URLSafeBase64Encoder
from nacl.exceptions import CryptoError
from nacl.secret import SecretBox
from nacl.utils import random
from passlib.hash import argon2
from ormantic.exceptions import NoMatch
from pickle import dumps, loads
from pydantic import BaseModel
from sqlite3 import IntegrityError


logger = getLogger(__name__)


class BodyAdmin(BaseModel):
    email: str
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/admin/login')
secret_box = SecretBox(random(SecretBox.KEY_SIZE))


def to_token(**kwargs):
    return secret_box.encrypt(dumps(kwargs), encoder=URLSafeBase64Encoder).decode(
        'ascii'
    )


def from_token(token):
    return loads(
        secret_box.decrypt(token.encode('ascii'), encoder=URLSafeBase64Encoder)
    )


def url(route):
    return config['domainname'] + route


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


@router.post('/register/', status_code=status.HTTP_202_ACCEPTED)
async def admin_register(values: BodyAdmin):
    register_token = to_token(**values.__dict__)
    logger.debug(register_token)
    try:
        send_email(
            to=values.email,
            subject='Confirm Account',
            # XXX create real confirm link
            body=register_token,
        )
    except ConnectionRefusedError:
        logger.exception('Email sending failed')
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
    return {}


@router.post('/confirm/{register_token}')
async def admin_confirm(register_token: str):
    try:
        values = from_token(register_token)
        passhash = argon2.hash(values['password'])
        await Admin.objects.create(email=values['email'], passhash=passhash)
        return {'access_token': register_token, 'token_type': 'bearer'}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.post('/login/')
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        await get_auth(form_data.username, form_data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password',
        )
    token = to_token(email=form_data.username, password=form_data.password)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/hoods/')
async def admin_hood_read_all(admin=Depends(get_admin)):
    return (
        await AdminHoodRelation.objects.select_related('hood').filter(admin=admin).all()
    )

# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.config import config
from kibicara.platforms.twitter.bot import spawner
from kibicara.platforms.twitter.model import Twitter
from kibicara.webapi.hoods import get_hood
from logging import getLogger
from sqlite3 import IntegrityError
from peony.oauth_dance import get_oauth_token, get_access_token


logger = getLogger(__name__)


async def get_twitter(twitter_id: int, hood=Depends(get_hood)):
    try:
        return await Twitter.objects.get(id=twitter_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()
twitter_callback_router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def twitter_create(response: Response, hood=Depends(get_hood)):
    try:
        twitter = await Twitter.objects.create(hood=hood)
        oauth_token = await get_oauth_token(
            config['twitter_consumer_key'],
            config['twitter_consumer_secret'],
            callback_uri='http://127.0.0.1:8000/api/twitter/callback',
        )
        if oauth_token['oauth_callback_confirmed'] != 'true':
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        await twitter.update(
            access_token=oauth_token['oauth_token'],
            access_token_secret=oauth_token['oauth_token_secret'],
        )
        response.headers['Location'] = '%d' % twitter.id
        return twitter
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@twitter_callback_router.get('/callback')
async def twitter_read_callback(oauth_token: str, oauth_verifier: str):
    try:
        twitter = await Twitter.objects.filter(access_token=oauth_token).get()
        access_token = await get_access_token(
            config['twitter_consumer_key'],
            config['twitter_consumer_secret'],
            twitter.access_token,
            twitter.access_token_secret,
            oauth_verifier,
        )
        await twitter.update(
            access_token=access_token['oauth_token'],
            access_token_secret=access_token['oauth_token_secret'],
        )
        spawner.start(twitter)
        response.headers['Location'] = '%d' % twitter.id
        return []
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

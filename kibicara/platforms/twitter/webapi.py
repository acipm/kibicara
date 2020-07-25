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
from ormantic.exceptions import NoMatch
from peony.oauth_dance import get_oauth_token, get_access_token
from peony.exceptions import NotAuthenticated


logger = getLogger(__name__)


async def get_twitter(twitter_id: int, hood=Depends(get_hood)):
    try:
        return await Twitter.objects.get(id=twitter_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()
twitter_callback_router = APIRouter()


@router.get(
    '/',
    # TODO response_model,
    operation_id='get_twitters',
)
async def twitter_read_all(hood=Depends(get_hood)):
    return await Twitter.objects.filter(hood=hood).all()


@router.get(
    '/{twitter_id}',
    # TODO response_model
    operation_id='get_twitter',
)
async def twitter_read(twitter=Depends(get_twitter)):
    return twitter


@router.delete(
    '/{twitter_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    # TODO response_model
    operation_id='delete_twitter',
)
async def twitter_delete(twitter=Depends(get_twitter)):
    spawner.stop(twitter)
    await twitter.delete()


@router.get(
    '/{twitter_id}/status',
    status_code=status.HTTP_200_OK,
    # TODO response_model
    operation_id='status_twitter',
)
async def twitter_status(twitter=Depends(get_twitter)):
    return {'status': spawner.get(twitter).status.name}


@router.post(
    '/{twitter_id}/start',
    status_code=status.HTTP_200_OK,
    # TODO response_model
    operation_id='start_twitter',
)
async def twitter_start(twitter=Depends(get_twitter)):
    await twitter.update(enabled=True)
    spawner.get(twitter).start()
    return {}


@router.post(
    '/{twitter_id}/stop',
    status_code=status.HTTP_200_OK,
    # TODO response_model
    operation_id='stop_twitter',
)
async def twitter_stop(twitter=Depends(get_twitter)):
    await twitter.update(enabled=False)
    spawner.get(twitter).stop()
    return {}


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model
    operation_id='create_twitter',
)
async def twitter_create(response: Response, hood=Depends(get_hood)):
    """
    `https://api.twitter.com/oauth/authorize?oauth_token=`
    """
    try:
        request_token = await get_oauth_token(
            config['twitter']['consumer_key'],
            config['twitter']['consumer_secret'],
            callback_uri='http://127.0.0.1:8000/api/twitter/callback',
        )
        if request_token['oauth_callback_confirmed'] != 'true':
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        twitter = await Twitter.objects.create(
            hood=hood,
            access_token=request_token['oauth_token'],
            access_token_secret=request_token['oauth_token_secret'],
        )
        response.headers['Location'] = '%d' % twitter.id
        return twitter
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except (KeyError, ValueError, NotAuthenticated):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@twitter_callback_router.get(
    '/callback',
    # TODO response_model
    operation_id='callback_twitter',
)
async def twitter_read_callback(oauth_token: str, oauth_verifier: str):
    try:
        twitter = await Twitter.objects.filter(access_token=oauth_token).get()
        access_token = await get_access_token(
            config['twitter']['consumer_key'],
            config['twitter']['consumer_secret'],
            twitter.access_token,
            twitter.access_token_secret,
            oauth_verifier,
        )
        await twitter.update(
            access_token=access_token['oauth_token'],
            access_token_secret=access_token['oauth_token_secret'],
            verified=True,
            enabled=True,
        )
        spawner.start(twitter)
        return {}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except (KeyError, ValueError, NotAuthenticated):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

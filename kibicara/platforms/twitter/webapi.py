# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from logging import getLogger
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, Response, status
from ormantic.exceptions import NoMatch
from peony.exceptions import NotAuthenticated
from peony.oauth_dance import get_access_token, get_oauth_token
from pydantic import BaseModel

from kibicara.config import config
from kibicara.platforms.twitter.bot import spawner
from kibicara.platforms.twitter.model import Twitter
from kibicara.webapi.hoods import get_hood, get_hood_unauthorized

logger = getLogger(__name__)


class BodyTwitterPublic(BaseModel):
    username: str


async def get_twitter(twitter_id: int, hood=Depends(get_hood)):
    try:
        return await Twitter.objects.get(id=twitter_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()
twitter_callback_router = APIRouter()


@router.get(
    '/public',
    # TODO response_model,
    operation_id='get_twitters_public',
)
async def twitter_read_all_public(hood=Depends(get_hood_unauthorized)):
    twitterbots = await Twitter.objects.filter(hood=hood).all()
    return [
        BodyTwitterPublic(username=twitterbot.username)
        for twitterbot in twitterbots
        if twitterbot.verified == 1 and twitterbot.enabled == 1 and twitterbot.username
    ]


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
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
        # Purge Twitter corpses
        for corpse in await Twitter.objects.filter(hood=hood, verified=False).all():
            await corpse.delete()
        # Create Twitter
        request_token = await get_oauth_token(
            config['twitter']['consumer_key'],
            config['twitter']['consumer_secret'],
            callback_uri='{0}/dashboard/twitter-callback?hood={1}'.format(
                config['frontend_url'], hood.id
            ),
        )
        if request_token['oauth_callback_confirmed'] != 'true':
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        twitter = await Twitter.objects.create(
            hood=hood,
            access_token=request_token['oauth_token'],
            access_token_secret=request_token['oauth_token_secret'],
        )
        response.headers['Location'] = str(twitter.id)
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
async def twitter_read_callback(
    oauth_token: str, oauth_verifier: str, hood=Depends(get_hood)
):
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

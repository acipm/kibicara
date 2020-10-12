# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from pytest import fixture, mark

from kibicara import config
from kibicara.platforms import twitter
from kibicara.platforms.twitter.model import Twitter


@fixture(scope='function')
def receive_oauth_request_token(monkeypatch, twitter_request_response):
    @mark.asyncio
    async def mock_get_oauth_request_token(
        consumer_key, consumer_secret, callback_uri=''
    ):
        return twitter_request_response

    monkeypatch.setattr(twitter.webapi, 'get_oauth_token', mock_get_oauth_request_token)


@fixture(scope='function')
def receive_oauth_access_token(monkeypatch, twitter_access_response):
    @mark.asyncio
    async def mock_get_oauth_access_token(
        consumer_key, consumer_secret, access_token, access_token_secret, oauth_verifier
    ):
        return twitter_access_response

    monkeypatch.setattr(twitter.webapi, 'get_access_token', mock_get_oauth_access_token)


@fixture(scope='function')
def disable_spawner(monkeypatch):
    class DoNothing:
        def start(self, bot):
            assert bot is not None

    monkeypatch.setattr(twitter.webapi, 'spawner', DoNothing())


@mark.parametrize(
    'twitter_request_response, twitter_access_response',
    [
        (
            {
                'oauth_callback_confirmed': 'true',
                'oauth_token': 'oauth_request_token123',
                'oauth_token_secret': 'oauth_request_secret123',
            },
            {
                'oauth_token': 'oauth_access_token123',
                'oauth_token_secret': 'oauth_access_secret123',
            },
        )
    ],
)
def test_twitter_create_bot(
    client,
    event_loop,
    monkeypatch,
    auth_header,
    hood_id,
    receive_oauth_request_token,
    receive_oauth_access_token,
    disable_spawner,
    twitter_request_response,
    twitter_access_response,
):
    monkeypatch.setitem(
        config.config,
        'twitter',
        {'consumer_key': 'consumer_key123', 'consumer_secret': 'consumer_secret123'},
    )

    # Twitter create endpoint
    response = client.post(
        '/api/hoods/{0}/twitter/'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_201_CREATED
    bot_id = response.json()['id']
    twitter = event_loop.run_until_complete(Twitter.objects.get(id=bot_id))
    assert (
        response.json()['access_token']
        == twitter_request_response['oauth_token']
        == twitter.access_token
    )
    assert (
        response.json()['access_token_secret']
        == twitter_request_response['oauth_token_secret']
        == twitter.access_token_secret
    )
    assert not twitter.verified
    assert response.json()['verified'] == twitter.verified
    assert not twitter.enabled
    assert response.json()['enabled'] == twitter.enabled
    assert response.json()['hood']['id'] == hood_id

    # Twitter callback endpoint should enable bot
    response = client.get(
        '/api/twitter/callback',
        headers=auth_header,
        params={
            'hood_id': hood_id,
            'oauth_token': twitter_request_response['oauth_token'],
            'oauth_verifier': 'oauth_verifier123',
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}
    twitter = event_loop.run_until_complete(Twitter.objects.get(id=bot_id))
    assert twitter_access_response['oauth_token'] == twitter.access_token
    assert twitter_access_response['oauth_token_secret'] == twitter.access_token_secret
    assert twitter.verified
    assert twitter.enabled


def test_twitter_callback_invalid_oauth_token(client, auth_header):
    response = client.get(
        '/api/twitter/callback',
        headers=auth_header,
        params={'hood_id': '1', 'oauth_token': 'abc', 'oauth_verifier': 'def'},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_twitter_create_twitter_invalid_id(client, auth_header):
    response = client.post('/api/hoods/1337/twitter/', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.post('/api/hoods/wrong/twitter/', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_twitter_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/{hood_id}/twitter/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_twitter_create_wrong_consumer_keys(client, monkeypatch, auth_header, hood_id):
    # No consumer keys
    response = client.post(
        '/api/hoods/{0}/twitter/'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    # Invalid consumer keys
    monkeypatch.setitem(
        config.config,
        'twitter',
        {'consumer_key': 'consumer_key123', 'consumer_secret': 'consumer_secret123'},
    )

    response = client.post(
        '/api/hoods/{0}/twitter/'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status

from kibicara.model import Hood
from kibicara.platforms.twitter.model import Twitter


def test_twitter_get_bots(client, auth_header, event_loop, hood_id):
    hood = event_loop.run_until_complete(Hood.objects.get(id=hood_id))
    twitter0 = event_loop.run_until_complete(
        Twitter.objects.create(
            hood=hood,
            access_token='access_token123',
            access_token_secret='access_token_secret123',
        )
    )
    twitter1 = event_loop.run_until_complete(
        Twitter.objects.create(
            hood=hood,
            access_token='access_token456',
            access_token_secret='access_token_secret456',
        )
    )
    response = client.get(
        '/api/hoods/{0}/twitter'.format(twitter0.hood.id), headers=auth_header
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == twitter0.id
    assert response.json()[0]['access_token'] == twitter0.access_token
    assert response.json()[1]['id'] == twitter1.id
    assert response.json()[1]['access_token'] == twitter1.access_token


def test_twitter_get_bots_invalid_id(client, auth_header, hood_id):
    response = client.get('/api/hoods/1337/twitter', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get('/api/hoods/wrong/twitter', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_twitter_get_bots_unauthorized(client, hood_id):
    response = client.get('/api/hoods/{0}/twitter'.format(hood_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

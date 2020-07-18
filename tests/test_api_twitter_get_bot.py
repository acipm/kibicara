# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_twitter_get_bot(client, auth_header, event_loop, twitter):
    response = client.get(
        f'/api/hoods/{twitter.hood.id}/twitter/{twitter.id}', headers=auth_header
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == twitter.id
    assert response.json()['access_token'] == twitter.access_token
    assert response.json()['access_token_secret'] == twitter.access_token_secret


def test_twitter_get_bot_invalid_id(client, auth_header, hood_id):
    response = client.get('/api/hoods/1337/twitter/123', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get('/api/hoods/wrong/twitter/123', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.get(f'/api/hoods/{hood_id}/twitter/7331', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get(f'/api/hoods/{hood_id}/twitter/wrong', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_twitter_get_bot_unauthorized(client, twitter):
    response = client.get(f'/api/hoods/{twitter.hood.id}/twitter/{twitter.id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

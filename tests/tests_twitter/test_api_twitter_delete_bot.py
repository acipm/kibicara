# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from kibicara.platforms.twitter.model import Twitter
from ormantic.exceptions import NoMatch
from pytest import raises


def test_twitter_delete_bot(client, event_loop, twitter, auth_header):
    response = client.delete(
        f'/api/hoods/{twitter.hood.id}/twitter/{twitter.id}', headers=auth_header
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with raises(NoMatch):
        event_loop.run_until_complete(Twitter.objects.get(id=twitter.id))


def test_twitter_delete_bot_invalid_id(client, auth_header, hood_id):
    response = client.delete('/api/hoods/1337/twitter/123', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete('/api/hoods/wrong/twitter/123', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.delete(f'/api/hoods/{hood_id}/twitter/7331', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete(f'/api/hoods/{hood_id}/twitter/wrong', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_twitter_delete_bot_unauthorized(client, twitter):
    response = client.delete(f'/api/hoods/{twitter.hood.id}/twitter/{twitter.id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

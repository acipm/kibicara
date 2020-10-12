# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from ormantic.exceptions import NoMatch
from pytest import raises

from kibicara.platforms.twitter.model import Twitter


def test_twitter_delete_bot(client, event_loop, twitter, auth_header):
    response = client.delete(
        '/api/hoods/{0}/twitter/{1}'.format(twitter.hood.id, twitter.id),
        headers=auth_header,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with raises(NoMatch):
        event_loop.run_until_complete(Twitter.objects.get(id=twitter.id))


def test_twitter_delete_bot_invalid_id(client, auth_header, hood_id):
    response = client.delete('/api/hoods/1337/twitter/123', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete('/api/hoods/wrong/twitter/123', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.delete(
        '/api/hoods/{0}/twitter/7331'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete(
        '/api/hoods/{0}/twitter/wrong'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_twitter_delete_bot_unauthorized(client, twitter):
    response = client.delete(
        '/api/hoods/{0}/twitter/{1}'.format(twitter.hood.id, twitter.id)
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

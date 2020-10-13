# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD


from fastapi import status
from pytest import fixture


@fixture(scope='function')
def email_row(client, hood_id, auth_header):
    response = client.post(
        '/api/hoods/{0}/email/'.format(hood_id),
        json={'name': 'kibicara-test'},
        headers=auth_header,
    )
    assert response.status_code == status.HTTP_201_CREATED
    email_id = int(response.headers['Location'])
    yield response.json()
    client.delete('/api/hoods/{0}/email/{1}'.format(hood_id, email_id), headers=auth_header)

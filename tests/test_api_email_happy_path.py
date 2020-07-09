# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_email_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/%d/email/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

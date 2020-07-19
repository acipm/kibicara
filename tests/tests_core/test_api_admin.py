# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_hoods_unauthorized(client):
    response = client.get('/api/admin/hoods/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hoods_success(client, auth_header):
    response = client.get('/api/admin/hoods/', headers=auth_header)
    assert response.status_code == status.HTTP_200_OK

# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.platforms.test.bot import spawner
from kibicara.platforms.test.model import Test
from kibicara.platformapi import Message
from kibicara.webapi.hoods import get_hood
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from sqlite3 import IntegrityError


class BodyMessage(BaseModel):
    text: str


async def get_test(test_id: int, hood=Depends(get_hood)):
    try:
        return await Test.objects.get(id=test_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()


@router.get('/')
async def test_read_all(hood=Depends(get_hood)):
    return await Test.objects.filter(hood=hood).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def test_create(response: Response, hood=Depends(get_hood)):
    try:
        test = await Test.objects.create(hood=hood)
        spawner.start(test)
        response.headers['Location'] = str(test.id)
        return test
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/{test_id}')
async def test_read(test=Depends(get_test)):
    return test


@router.delete('/{test_id}', status_code=status.HTTP_204_NO_CONTENT)
async def test_delete(test=Depends(get_test)):
    spawner.stop(test)
    await test.delete()


@router.get('/{test_id}/messages/')
async def test_message_read_all(test=Depends(get_test)):
    return spawner.get(test).messages


@router.post('/{test_id}/messages/')
async def test_message_create(message: BodyMessage, test=Depends(get_test)):
    await spawner.get(test).publish(Message(message.text))
    return {}

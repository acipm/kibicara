# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.model import Trigger
from kibicara.webapi.hoods import get_hood
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from re import compile as regex_compile, error as RegexError
from sqlite3 import IntegrityError


class BodyTrigger(BaseModel):
    pattern: str


async def get_trigger(trigger_id: int, hood=Depends(get_hood)):
    try:
        return await Trigger.objects.get(id=trigger_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()


@router.get('/')
async def trigger_read_all(hood=Depends(get_hood)):
    return await Trigger.objects.filter(hood=hood).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def trigger_create(
    values: BodyTrigger, response: Response, hood=Depends(get_hood)
):
    try:
        regex_compile(values.pattern)
        trigger = await Trigger.objects.create(hood=hood, **values.__dict__)
        response.headers['Location'] = '%d' % trigger.id
        return trigger
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except RegexError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get('/{trigger_id}')
async def trigger_read(trigger=Depends(get_trigger)):
    return trigger


@router.put('/{trigger_id}', status_code=status.HTTP_204_NO_CONTENT)
async def trigger_update(values: BodyTrigger, trigger=Depends(get_trigger)):
    await trigger.update(**values.__dict__)


@router.delete('/{trigger_id}', status_code=status.HTTP_204_NO_CONTENT)
async def trigger_delete(trigger=Depends(get_trigger)):
    await trigger.delete()

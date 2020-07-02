# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.model import AdminHoodRelation, Hood
from kibicara.webapi.admin import get_admin
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from sqlite3 import IntegrityError


class BodyHood(BaseModel):
    name: str
    landingpage: str = '''
    Default Landing Page
    '''


async def get_hood(hood_id: int, admin=Depends(get_admin)):
    try:
        hood = await Hood.objects.get(id=hood_id)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        await AdminHoodRelation.objects.get(admin=admin, hood=hood)
    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return hood


router = APIRouter()


@router.get('/')
async def hood_read_all():
    return await Hood.objects.all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def hood_create(values: BodyHood, response: Response, admin=Depends(get_admin)):
    try:
        hood = await Hood.objects.create(**values.__dict__)
        await AdminHoodRelation.objects.create(admin=admin.id, hood=hood.id)
        response.headers['Location'] = '%d' % hood.id
        return hood
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get('/{hood_id}')
async def hood_read(hood=Depends(get_hood)):
    return hood


@router.put('/{hood_id}', status_code=status.HTTP_204_NO_CONTENT)
async def hood_update(values: BodyHood, hood=Depends(get_hood)):
    await hood.update(**values.__dict__)


@router.delete('/{hood_id}', status_code=status.HTTP_204_NO_CONTENT)
async def hood_delete(hood=Depends(get_hood)):
    for relation in await AdminHoodRelation.objects.filter(hood=hood).all():
        await relation.delete()
    await hood.delete()

# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

""" REST API Endpoints for managing hoods. """

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.model import AdminHoodRelation, BadWord, Hood, Trigger
from kibicara.platformapi import Spawner
from kibicara.platforms.email.bot import spawner
from kibicara.webapi.admin import get_admin
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from sqlite3 import IntegrityError


class BodyHood(BaseModel):
    name: str
    landingpage: str = '''
    Default Landing Page
    '''


async def get_hood_unauthorized(hood_id: int):
    try:
        hood = await Hood.objects.get(id=hood_id)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return hood


async def get_hood(hood=Depends(get_hood_unauthorized), admin=Depends(get_admin)):
    try:
        await AdminHoodRelation.objects.get(admin=admin, hood=hood)
    except NoMatch:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return hood


router = APIRouter()


@router.get(
    '/',
    # TODO response_model,
    operation_id='get_hoods',
    tags=['hoods'],
)
async def hood_read_all():
    """ Get all existing hoods. """
    return await Hood.objects.all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model,
    operation_id='create_hood',
    tags=['hoods'],
)
async def hood_create(values: BodyHood, response: Response, admin=Depends(get_admin)):
    """Creates a hood.

    - **name**: Name of the hood
    - **landingpage**: Markdown formatted description of the hood
    """
    try:
        hood = await Hood.objects.create(**values.__dict__)
        await AdminHoodRelation.objects.create(admin=admin.id, hood=hood.id)
        spawner.start(hood)

        # Initialize Triggers to match all
        await Trigger.objects.create(hood=hood, pattern='.')

        response.headers['Location'] = '%d' % hood.id
        return hood
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get(
    '/{hood_id}',
    # TODO response_model,
    operation_id='get_hood',
    tags=['hoods'],
)
async def hood_read(hood=Depends(get_hood_unauthorized)):
    """ Get hood with id **hood_id**. """
    return hood


@router.put(
    '/{hood_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='update_hood',
    tags=['hoods'],
)
async def hood_update(values: BodyHood, hood=Depends(get_hood)):
    """Updates hood with id **hood_id**.

    - **name**: New name of the hood
    - **landingpage**: New Markdown formatted description of the hood
    """
    await hood.update(**values.__dict__)


@router.delete(
    '/{hood_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='delete_hood',
    tags=['hoods'],
)
async def hood_delete(hood=Depends(get_hood)):
    """ Deletes hood with id **hood_id**. """
    await Spawner.destroy_hood(hood)
    for trigger in await Trigger.objects.filter(hood=hood).all():
        await trigger.delete()
    for badword in await BadWord.objects.filter(hood=hood).all():
        await badword.delete()
    for relation in await AdminHoodRelation.objects.filter(hood=hood).all():
        await relation.delete()
    await hood.delete()

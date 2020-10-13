# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

"""REST API endpoints for managing triggers.

Provides API endpoints for adding, removing and reading regular expressions that allow a
message to be passed through by a censor. A published message must match one of these
regular expressions otherwise it gets dropped by the censor. This provides a message
filter customizable by the hood admins.
"""

from re import compile as regex_compile
from re import error as RegexError
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, Response, status
from ormantic.exceptions import NoMatch
from pydantic import BaseModel

from kibicara.model import Trigger
from kibicara.webapi.hoods import get_hood


class BodyTrigger(BaseModel):
    pattern: str


async def get_trigger(trigger_id: int, hood=Depends(get_hood)):
    try:
        return await Trigger.objects.get(id=trigger_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()


@router.get(
    '/',
    # TODO response_model,
    operation_id='get_triggers',
)
async def trigger_read_all(hood=Depends(get_hood)):
    """Get all triggers of hood with id **hood_id**."""
    return await Trigger.objects.filter(hood=hood).all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model,
    operation_id='create_trigger',
)
async def trigger_create(
    values: BodyTrigger, response: Response, hood=Depends(get_hood)
):
    """Creates a new trigger for hood with id **hood_id**.

    - **pattern**: Regular expression which is used to match a trigger.
    """
    try:
        regex_compile(values.pattern)
        trigger = await Trigger.objects.create(hood=hood, **values.__dict__)
        response.headers['Location'] = str(trigger.id)
        return trigger
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except RegexError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get(
    '/{trigger_id}',
    # TODO response_model,
    operation_id='get_trigger',
)
async def trigger_read(trigger=Depends(get_trigger)):
    """Reads trigger with id **trigger_id** for hood with id **hood_id**."""
    return trigger


@router.put(
    '/{trigger_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='update_trigger',
)
async def trigger_update(values: BodyTrigger, trigger=Depends(get_trigger)):
    """Updates trigger with id **trigger_id** for hood with id **hood_id**.

    - **pattern**: Regular expression which is used to match a trigger
    """
    await trigger.update(**values.__dict__)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    '/{trigger_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='delete_trigger',
)
async def trigger_delete(trigger=Depends(get_trigger)):
    """Deletes trigger with id **trigger_id** for hood with id **hood_id**."""
    await trigger.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

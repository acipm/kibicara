# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

""" REST API endpoints for managing badwords.

Provides API endpoints for adding, removing and reading regular expressions that block a
received message to be dropped by a censor. This provides a message filter customizable
by the hood admins.
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from kibicara.model import BadWord
from kibicara.webapi.hoods import get_hood
from ormantic.exceptions import NoMatch
from pydantic import BaseModel
from re import compile as regex_compile, error as RegexError
from sqlite3 import IntegrityError


class BodyBadWord(BaseModel):
    pattern: str


async def get_badword(badword_id: int, hood=Depends(get_hood)):
    try:
        return await BadWord.objects.get(id=badword_id, hood=hood)
    except NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


router = APIRouter()


@router.get(
    '/',
    # TODO response_model,
    operation_id='get_badwords',
)
async def badword_read_all(hood=Depends(get_hood)):
    """ Get all badwords of hood with id **hood_id**. """
    return await BadWord.objects.filter(hood=hood).all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # TODO response_model,
    operation_id='create_badword',
)
async def badword_create(
    values: BodyBadWord, response: Response, hood=Depends(get_hood)
):
    """Creates a new badword for hood with id **hood_id**.

    - **pattern**: Regular expression which is used to match a badword.
    """
    try:
        regex_compile(values.pattern)
        badword = await BadWord.objects.create(hood=hood, **values.__dict__)
        response.headers['Location'] = '%d' % badword.id
        return badword
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except RegexError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get(
    '/{badword_id}',
    # TODO response_model,
    operation_id='get_badword',
)
async def badword_read(badword=Depends(get_badword)):
    """ Reads badword with id **badword_id** for hood with id **hood_id**. """
    return badword


@router.put(
    '/{badword_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='update_badword',
)
async def badword_update(values: BodyBadWord, badword=Depends(get_badword)):
    """Updates badword with id **badword_id** for hood with id **hood_id**.

    - **pattern**: Regular expression which is used to match a badword
    """
    await badword.update(**values.__dict__)


@router.delete(
    '/{badword_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='delete_badword',
)
async def badword_delete(badword=Depends(get_badword)):
    """ Deletes badword with id **badword_id** for hood with id **hood_id**. """
    await badword.delete()

# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

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


@router.get('/')
async def badword_read_all(hood=Depends(get_hood)):
    return await BadWord.objects.filter(hood=hood).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def badword_create(
    values: BodyBadWord, response: Response, hood=Depends(get_hood)
):
    try:
        regex_compile(values.pattern)
        badword = await BadWord.objects.create(hood=hood, **values.__dict__)
        response.headers['Location'] = '%d' % badword.id
        return badword
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except RegexError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get('/{badword_id}')
async def badword_read(badword=Depends(get_badword)):
    return badword


@router.put('/{badword_id}', status_code=status.HTTP_204_NO_CONTENT)
async def badword_update(values: BodyBadWord, badword=Depends(get_badword)):
    await badword.update(**values.__dict__)


@router.delete('/{badword_id}', status_code=status.HTTP_204_NO_CONTENT)
async def badword_delete(badword=Depends(get_badword)):
    await badword.delete()

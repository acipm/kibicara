# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter
from kibicara.platforms.test.webapi import router as test_router
from kibicara.webapi.admin import router as admin_router
from kibicara.webapi.hoods import router as hoods_router
from kibicara.webapi.hoods.badwords import router as badwords_router
from kibicara.webapi.hoods.triggers import router as triggers_router


router = APIRouter()
router.include_router(admin_router, prefix='/admin', tags=['admin'])
hoods_router.include_router(triggers_router, prefix='/{hood_id}/triggers')
hoods_router.include_router(badwords_router, prefix='/{hood_id}/badwords')
hoods_router.include_router(
    test_router, prefix='/{hood_id}/test', tags=['test'])
router.include_router(hoods_router, prefix='/hoods', tags=['hoods'])

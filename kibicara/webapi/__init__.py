# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

""" Routing definitions for the REST API.

A platform bot shall add its API router in this `__init__.py`
file to get included into the main application.
"""

from fastapi import APIRouter
from kibicara.platforms.test.webapi import router as test_router
from kibicara.platforms.telegram.webapi import router as telegram_router
from kibicara.platforms.twitter.webapi import router as twitter_router
from kibicara.platforms.twitter.webapi import twitter_callback_router
from kibicara.platforms.email.webapi import mailbox_router, hood_router as email_router
from kibicara.webapi.admin import router as admin_router
from kibicara.webapi.hoods import router as hoods_router
from kibicara.webapi.hoods.badwords import router as badwords_router
from kibicara.webapi.hoods.triggers import router as triggers_router


router = APIRouter()
router.include_router(admin_router, prefix='/admin', tags=['admin'])
router.include_router(mailbox_router, prefix='/email', tags=['email'])
hoods_router.include_router(triggers_router, prefix='/{hood_id}/triggers')
hoods_router.include_router(badwords_router, prefix='/{hood_id}/badwords')
hoods_router.include_router(test_router, prefix='/{hood_id}/test', tags=['test'])
hoods_router.include_router(
    telegram_router, prefix='/{hood_id}/telegram', tags=['telegram']
)
hoods_router.include_router(
    twitter_router, prefix='/{hood_id}/twitter', tags=['twitter']
)
router.include_router(twitter_callback_router, prefix='/twitter', tags=['twitter'])
hoods_router.include_router(email_router, prefix='/{hood_id}/email', tags=['email'])
router.include_router(hoods_router, prefix='/hoods', tags=['hoods'])

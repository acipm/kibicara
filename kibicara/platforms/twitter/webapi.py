# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import APIRouter
from kibicara.platforms.twitter.bot import spawner
from kibicara.platforms.twitter.model import Twitter


router = APIRouter()

# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import AdminHoodRelation, BadWord, Trigger
from kibicara.platformapi import Spawner


async def delete_hood(hood):
    await Spawner.destroy_hood(hood)
    for trigger in await Trigger.objects.filter(hood=hood).all():
        await trigger.delete()
    for badword in await BadWord.objects.filter(hood=hood).all():
        await badword.delete()
    for relation in await AdminHoodRelation.objects.filter(hood=hood).all():
        await relation.delete()
    await hood.delete()

# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.platforms.test.model import Test
from kibicara.platformapi import Censor, Spawner


class TestBot(Censor):
    def __init__(self, test):
        super().__init__(test.hood)
        self.messages = []

    async def run(self):
        while True:
            self.messages.append(await self.receive())


spawner = Spawner(Test, TestBot)

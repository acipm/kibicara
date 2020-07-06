# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.platforms.email.model import EmailRecipients, Email
from kibicara.platformapi import Censor, Spawner, Message
from logging import getLogger

logger = getLogger(__name__)


class EmailBot(Censor):
    def __init__(self, email_model):
        super().__init__(email_model.hood)
        self.model = email_model
        self.messages = []

    async def run(self):
        while True:
            message = await self.receive()
            print("push " + message.text)
            # send message to everyone in EmailRecipients(hood=self.hood)


spawner = Spawner(Email, EmailBot)

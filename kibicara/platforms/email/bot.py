# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.platforms.email.model import EmailRecipients, Email
from kibicara.platformapi import Censor, Spawner, Message
from logging import getLogger
from kibicara.email import send_email

logger = getLogger(__name__)


class EmailBot(Censor):
    def __init__(self, email_model):
        super().__init__(email_model.hood)
        self.model = email_model
        self.messages = []

    async def run(self):
        while True:
            message = await self.receive()
            for recipient in EmailRecipients(hood=self.hood):
                send_email(recipient.email, "Kibicara " + self.hood, body=message.text)


spawner = Spawner(Email, EmailBot)

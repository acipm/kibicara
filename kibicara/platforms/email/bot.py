# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.platforms.email.model import EmailRecipients, Email
from kibicara.model import Hood
from kibicara.platformapi import Censor, Spawner, Message
from kibicara.email import send_email
from kibicara.config import config
import jwt


class EmailBot(Censor):
    def __init__(self, email_model):
        super().__init__(email_model.hood)
        self.model = email_model
        self.messages = []

    async def run(self):
        while True:
            hood_name = await Hood.objects.get(id=self.model.hood).name
            message = await self.receive()
            for recipient in EmailRecipients(hood=self.model.hood):
                json = {
                    'email': recipient.email,
                    'hood': self.model.hood,
                }
                token = jwt.encode(json, self.model.secret).decode('ascii')
                unsubscribe_link = (
                    config['root_url']
                    + 'api/'
                    + self.model.id
                    + '/email/unsubscribe/'
                    + token
                )
                message.text += (
                    "\n\n--\nIf you want to stop receiving these mails, "
                    "follow this link: " + unsubscribe_link
                )
                send_email(recipient.email, "Kibicara " + hood_name, body=message.text)


spawner = Spawner(Email, EmailBot)

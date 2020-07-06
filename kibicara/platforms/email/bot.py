# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.platforms.email.model import EmailSubscribers, Email
from kibicara.model import Hood
from kibicara.platformapi import Censor, Spawner
from kibicara.email import send_email
from kibicara.config import config
from nacl.encoding import URLSafeBase64Encoder
from nacl.secret import SecretBox


class EmailBot(Censor):
    def __init__(self, email_model):
        super().__init__(email_model.hood)
        self.model = email_model
        self.messages = []

    async def run(self):
        """ Loop which waits for new messages and sends emails to all subscribers. """
        hood_name = await Hood.objects.get(id=self.model.hood).name
        while True:
            message = await self.receive()
            for subscriber in EmailSubscribers(hood=self.model.hood):
                json = {
                    'email': subscriber.email,
                    'hood': self.model.hood,
                }
                secretbox = SecretBox(Email.secret)
                token = secretbox.encrypt(json, encoder=URLSafeBase64Encoder)
                asciitoken = token.decode('ascii')
                unsubscribe_link = (
                    config['root_url']
                    + 'api/'
                    + self.model.id
                    + '/email/unsubscribe/'
                    + asciitoken
                )
                message.text += (
                    "\n\n--\nIf you want to stop receiving these mails, "
                    "follow this link: " + unsubscribe_link
                )
                send_email(subscriber.email, "Kibicara " + hood_name, body=message.text)


spawner = Spawner(Email, EmailBot)

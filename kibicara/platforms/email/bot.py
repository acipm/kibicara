# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.platforms.email.model import EmailSubscribers, Email
from kibicara.platformapi import Censor, Spawner
from kibicara.email import send_email
from kibicara.config import config
from kibicara.webapi.admin import to_token
from smtplib import SMTPException
from logging import getLogger


logger = getLogger(__name__)


class EmailBot(Censor):
    def __init__(self, email_model):
        super().__init__(email_model.hood)
        self.model = email_model
        self.messages = []

    async def run(self):
        """ Loop which waits for new messages and sends emails to all subscribers. """
        while True:
            message = await self.receive()
            logger.info("Received Email from %s: %s" % (message.author, message.text))
            for subscriber in EmailSubscribers.objects.filter(hood=self.hood.id):
                token = to_token(email=subscriber.email, hood=self.hood.id)
                unsubscribe_link = (
                    config['root_url']
                    + 'api/hoods/%d/email/unsubscribe/' % self.hood.id
                    + token
                )
                message.text += (
                    "\n\n--\nIf you want to stop receiving these mails, "
                    "follow this link: " + unsubscribe_link
                )
                try:
                    send_email(
                        subscriber.email,
                        "Kibicara " + self.hood.name,
                        body=message.text,
                    )
                except (ConnectionRefusedError, SMTPException):
                    logger.exception("Sending subscription confirmation email failed.")


spawner = Spawner(Email, EmailBot)

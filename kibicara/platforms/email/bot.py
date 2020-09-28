# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara import email
from kibicara.config import config
from kibicara.model import Hood
from kibicara.platformapi import Censor, Spawner
from kibicara.platforms.email.model import Email, EmailSubscribers
from kibicara.webapi.admin import to_token
from logging import getLogger
from smtplib import SMTPException


logger = getLogger(__name__)


class EmailBot(Censor):
    def __init__(self, hood):
        super().__init__(hood)
        self.enabled = hood.email_enabled

    @classmethod
    async def destroy_hood(cls, hood):
        """Removes all its database entries."""
        for inbox in await Email.objects.filter(hood=hood).all():
            await inbox.delete()
        for subscriber in await EmailSubscribers.objects.filter(hood=hood).all():
            await subscriber.delete()

    async def run(self):
        """ Loop which waits for new messages and sends emails to all subscribers. """
        while True:
            message = await self.receive()
            logger.debug(
                'Received message from censor ({0}): {1}'.format(self.hood.name, message.text)
            )
            for subscriber in await EmailSubscribers.objects.filter(
                hood=self.hood
            ).all():
                token = to_token(email=subscriber.email, hood=self.hood.id)
                body = (
                    '{0}\n\n--\n'
                    'If you want to stop receiving these mails,'
                    'follow this link: {1}/hoods/{2}/email-unsubscribe?token={3}'
                ).format(message.text, config['frontend_url'], self.hood.id, token)
                try:
                    logger.debug('Trying to send: \n{0}'.format(body))
                    email.send_email(
                        subscriber.email,
                        "Kibicara {0}".format(self.hood.name),
                        body=body,
                    )
                except (ConnectionRefusedError, SMTPException):
                    logger.exception("Sending email to subscriber failed.")


spawner = Spawner(Hood, EmailBot)

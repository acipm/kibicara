# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.config import config
from kibicara.email import send_email
from kibicara.model import Hood
from kibicara.platformapi import Censor, Spawner
from kibicara.platforms.email.model import EmailSubscribers
from kibicara.webapi.admin import to_token
from logging import getLogger
from smtplib import SMTPException


logger = getLogger(__name__)


class EmailBot(Censor):
    def __init__(self, hood):
        super().__init__(hood)

    async def run(self):
        """ Loop which waits for new messages and sends emails to all subscribers. """
        while True:
            message = await self.receive()
            logger.debug(
                'Received message from censor (%s): %s' % (self.hood.name, message.text)
            )
            logger.debug('a')
            for subscriber in await EmailSubscribers.objects.filter(
                hood=self.hood
            ).all():
                token = to_token(email=subscriber.email, hood=self.hood.id)
                body = (
                    '%s\n\n--\n'
                    'If you want to stop receiving these mails,'
                    'follow this link: %s/api/hoods/%d/email/unsubscribe/%s'
                ) % (message.text, config['root_url'], self.hood.id, token)
                try:
                    logger.debug('Trying to send: \n%s' % body)
                    send_email(
                        subscriber.email, "Kibicara " + self.hood.name, body=body,
                    )
                except (ConnectionRefusedError, SMTPException):
                    logger.exception("Sending email to subscriber failed.")


spawner = Spawner(Hood, EmailBot)

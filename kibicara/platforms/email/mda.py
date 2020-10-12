# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from asyncio import run as asyncio_run
from email.parser import BytesParser
from email.policy import default
from email.utils import parseaddr
from logging import getLogger
from re import sub
from sys import stdin

from fastapi import status
from ormantic import NoMatch
from requests import post

from kibicara.config import args, config
from kibicara.platforms.email.model import Email, EmailSubscribers

logger = getLogger(__name__)


class Main:
    def __init__(self):
        asyncio_run(self.__run())

    async def __run(self):
        # extract email from the recipient
        email_name = args.recipient.lower()
        try:
            email = await Email.objects.get(name=email_name)
        except NoMatch:
            logger.error('No recipient with this name')
            exit(1)

        # read mail from STDIN and parse to EmailMessage object
        message = BytesParser(policy=default).parsebytes(stdin.buffer.read())

        sender = ''
        if message.get('sender'):
            sender = message.get('sender')
        elif message.get('from'):
            sender = message.get('from')
        else:
            logger.error('No Sender of From header')
            exit(1)

        sender = parseaddr(sender)[1]
        if not sender:
            logger.error('Could not parse sender')
            exit(1)

        maybe_subscriber = await EmailSubscribers.objects.filter(email=sender).all()
        if len(maybe_subscriber) != 1 or maybe_subscriber[0].hood.id != email.hood.id:
            logger.error('Not a subscriber')
            exit(1)

        # extract relevant data from mail
        text = sub(
            r'<[^>]*>',
            '',
            message.get_body(preferencelist=('plain', 'html')).get_content(),
        )

        response = post(
            '{0}/api/hoods/{1}/email/messages/'.format(
                config['root_url'], email.hood.pk
            ),
            json={'text': text, 'secret': email.secret},
        )
        if response.status_code == status.HTTP_201_CREATED:
            exit(0)
        elif response.status_code == status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS:
            logger.error('Message was\'t accepted: {0}'.format(text))
        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            logger.error('Malformed request: {0}'.format(response.json()))
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            logger.error('Wrong API secret. kibicara_mda seems to be misconfigured')
        else:
            logger.error(
                'REST-API failed with response status {0}'.format(response.status_code)
            )
        exit(1)

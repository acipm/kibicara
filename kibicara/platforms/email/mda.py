# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from argparse import ArgumentParser
from asyncio import run as asyncio_run
from email.parser import BytesParser
from email.policy import default
from fastapi import status
from kibicara.config import args, config
from kibicara.model import Hood
from kibicara.platforms.email.model import Email
from logging import getLogger
from ormantic import NoMatch
from re import sub
from requests import post
from sys import stdin


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

        # extract relevant data from mail
        text = sub(
            r'<[^>]*>',
            '',
            message.get_body(preferencelist=('plain', 'html')).get_content(),
        )

        response = post(
            '%s/api/hoods/%d/email/messages/' % (config['root_url'], email.hood.pk),
            json={'text': text, 'secret': email.secret},
        )
        if response.status_code == status.HTTP_201_CREATED:
            exit(0)
        elif response.status_code == status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS:
            logger.error('Message was\'t accepted: %s' % text)
        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            logger.error('Malformed request: %s' % response.json())
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            logger.error('Wrong API secret. kibicara_mda seems to be misconfigured')
        else:
            logger.error(
                'REST-API failed with response status %d' % response.status_code
            )
        exit(1)

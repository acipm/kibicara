# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

import email.parser
import json
import sys
import re
from logging import getLogger
from kibicara.platforms.email.model import Email


def main():
    logger = getLogger(__name__)

    # read mail from STDIN
    mailbytes = bytes(sys.stdin.read())

    # parse plaintext to email.EmailMessage object
    myparser = email.parser.BytesParser()
    mail = myparser.parsebytes(mailbytes)

    # extract relevant data from mail
    for part in mail.walk():
        try:
            text = part.get_body(('plain',))
            if not text:
                text = re.sub(r'<[^>]*>', '', part.get_body(('html',)))
            if not text:
                logger.error('No suitable message body')
                exit(0)
        except Exception:
            logger.info("No Body in this message part", exc_info=True)
            exit(0)
    body = {
        'text': text,
        'to': mail['To'].lower(),
        'author': mail.get_unixfrom(),
        'secret': Email.secret,
    }

    # POST request mit API-key und JSON-body an /api/email/messages/:
    print(
        "curl "
        "-X POST http://localhost/api/email/messages/ "
        "-H 'Content-Type: application/json' "
        "-d " + json.dumps(body)
    )

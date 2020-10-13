# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

"""E-Mail handling."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
from smtplib import SMTP
from socket import getfqdn

logger = getLogger(__name__)


def send_email(to, subject, sender='kibicara', body=''):
    """E-Mail sender.

    Sends an E-Mail to a specified recipient with a body

    Example:
        ```
        from kibicara import email
        email.send_email('abc@de.fg', 'Email subject', body='Hi this is a mail body.')
        ```

    Args:
        to (str): Recipients' e-mail address
        subject (str): The subject of the e-mail
        sender (str): optional, Sender of the e-mail
        body (str): The body of the e-mail
    """
    msg = MIMEMultipart()
    msg['From'] = 'Kibicara <{0}@{1}>'.format(sender, getfqdn())
    msg['To'] = to
    msg['Subject'] = '[Kibicara] {0}'.format(subject)
    msg.attach(MIMEText(body))

    with SMTP('localhost') as smtp:
        smtp.send_message(msg)

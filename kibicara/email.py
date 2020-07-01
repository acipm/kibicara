# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger
from smtplib import SMTP
from socket import getfqdn


logger = getLogger(__name__)


def send_email(to, subject, sender='kibicara', body=''):
    msg = MIMEMultipart()
    msg['From'] = 'Kibicara <%s@%s>' % (sender, getfqdn())
    msg['To'] = to
    msg['Subject'] = '[Kibicara] %s' % subject
    msg.attach(MIMEText(body))

    with SMTP('localhost') as smtp:
        smtp.send_message(msg)

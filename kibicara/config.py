# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from argparse import ArgumentParser
from pytoml import load
from sys import argv


config = {
    'database_connection': 'sqlite:////tmp/kibicara.sqlite',
    'frontend_path': None,
    'root_url': 'http://localhost:8000/',
}

if argv[0] == 'kibicara':
    parser = ArgumentParser()
    parser.add_argument(
        '-f',
        '--config',
        dest='configfile',
        default='/etc/kibicara.conf',
        help='path to config file',
    )
    args = parser.parse_args()

    try:
        with open(args.configfile) as configfile:
            config.update(load(configfile))
    except FileNotFoundError:
        # run with default config
        pass

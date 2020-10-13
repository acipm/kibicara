# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

"""Configuration file and command line argument parser.

Gives a dictionary named `config` with configuration parsed either from
`/etc/kibicara.conf` or from a file given by command line argument `-f`.
If no configuration was found at all, the defaults are used.

Example:
    ```
    from kibicara.config import config
    print(config)
    ```
"""

from argparse import ArgumentParser
from sys import argv

from nacl.secret import SecretBox
from nacl.utils import random
from pytoml import load

config = {
    'database_connection': 'sqlite:////tmp/kibicara.sqlite',
    'frontend_url': 'http://127.0.0.1:4200',  # url of frontend, change in prod
    'secret': random(SecretBox.KEY_SIZE).hex(),  # generate with: openssl rand -hex 32
    # production params
    'frontend_path': None,  # required, path to frontend html/css/js files
    'production': True,
    'behind_proxy': False,
    'keyfile': None,  # optional for ssl
    'certfile': None,  # optional for ssl
    # dev params
    'root_url': 'http://localhost:8000',  # url of backend
    'cors_allow_origin': 'http://127.0.0.1:4200',
}
"""Default configuration.

The default configuration gets overwritten by a configuration file if one exists.
"""

args = None

if argv[0].endswith('kibicara'):
    parser = ArgumentParser()
    parser.add_argument(
        '-f',
        '--config',
        dest='configfile',
        default='/etc/kibicara.conf',
        help='path to config file',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Raise verbosity level',
    )
    args = parser.parse_args()

if argv[0].endswith('kibicara_mda'):
    parser = ArgumentParser()
    parser.add_argument(
        '-f',
        '--config',
        dest='configfile',
        default='/etc/kibicara.conf',
        help='path to config file',
    )
    # the MDA passes the recipient address as command line argument
    parser.add_argument('recipient')
    args = parser.parse_args()

if args is not None:
    try:
        with open(args.configfile) as configfile:
            config.update(load(configfile))
    except FileNotFoundError:
        # run with default config
        pass

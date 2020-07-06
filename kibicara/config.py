# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from optparse import OptionParser
from pytoml import load


config = {
    'database_connection': 'sqlite:////tmp/kibicara.sqlite',
    'frontend_path': None,
    'url': 'http://localhost:8000',
}

parser = OptionParser()
parser.add_option('-f', dest='configfile', default='/etc/kibicara.conf')
(option, args) = parser.parse_args()

try:
    with open(option.configfile) as configfile:
        config.update(load(configfile))
except FileNotFoundError:
    # run with default config
    pass

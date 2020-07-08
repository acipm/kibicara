# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

import argparse
from pytoml import load


config = {
    "database_connection": "sqlite:////tmp/kibicara.sqlite",
    "frontend_path": None,
    "root_url": "http://localhost:8000/",
}
parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    dest="configfile",
    default="/etc/kibicara.conf",
    help="path to config file",
)
args = parser.parse_args()

try:
    with open(args.configfile) as configfile:
        config.update(load(configfile))
except FileNotFoundError:
    # run with default config
    pass

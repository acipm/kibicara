# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

""" Entrypoint of Kibicara. """

from asyncio import run as asyncio_run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from hypercorn.config import Config
from hypercorn.asyncio import serve
from kibicara.config import args, config
from kibicara.model import Mapping
from kibicara.platformapi import Spawner
from kibicara.webapi import router
from logging import basicConfig, DEBUG, getLogger, INFO, WARNING


logger = getLogger(__name__)


class Main:
    """Entrypoint for Kibicara.

    Initializes the platform bots and starts the hypercorn webserver serving the
    Kibicara application and the specified frontend on port 8000.
    """

    def __init__(self):
        asyncio_run(self.__run())

    async def __run(self):
        LOGLEVELS = {
            None: WARNING,
            1: INFO,
            2: DEBUG,
        }
        basicConfig(
            level=LOGLEVELS.get(args.verbose, DEBUG),
            format="%(asctime)s %(name)s %(message)s",
        )
        getLogger('aiosqlite').setLevel(WARNING)
        Mapping.create_all()
        await Spawner.init_all()
        await self.__start_webserver()

    async def __start_webserver(self):
        class SinglePageApplication(StaticFiles):
            async def get_response(self, path, scope):
                response = await super().get_response(path, scope)
                if response.status_code == 404:
                    response = await super().get_response('.', scope)
                return response

        app = FastAPI()
        server_config = Config()
        server_config.accesslog = '-'
        server_config.behind_proxy = config['behind_proxy']
        server_config.keyfile = config['keyfile']
        server_config.certfile = config['certfile']
        if config['production']:
            server_config.bind = ['0.0.0.0:8000', '[::]:8000']
        api = FastAPI()
        api.include_router(router)
        app.mount('/api', api)
        if not config['production'] and config['cors_allow_origin']:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=config['cors_allow_origin'],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        if config['frontend_path'] is not None:
            app.mount(
                '/',
                app=SinglePageApplication(directory=config['frontend_path'], html=True),
            )
        await serve(app, server_config)

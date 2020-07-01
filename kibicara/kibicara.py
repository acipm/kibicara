# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from asyncio import run as asyncio_run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from hypercorn.config import Config
from hypercorn.asyncio import serve
from kibicara.config import config
from kibicara.model import Mapping
from kibicara.platformapi import Spawner
from kibicara.webapi import router
from logging import basicConfig, DEBUG, getLogger


logger = getLogger(__name__)


class Main:
    def __init__(self):
        asyncio_run(self.run())

    async def run(self):
        basicConfig(level=DEBUG, format="%(levelname)s %(name)s %(message)s")
        Mapping.create_all()
        await Spawner.init_all()
        await self._start_webserver()

    async def _start_webserver(self):
        class SinglePageApplication(StaticFiles):
            async def get_response(self, path, scope):
                response = await super().get_response(path, scope)
                if response.status_code == 404:
                    response = await super().get_response('.', scope)
                return response
        app = FastAPI()
        server_config = Config()
        server_config.accesslog = '-'
        app.include_router(router, prefix='/api')
        if config['frontend_path'] is not None:
            app.mount('/', app=SinglePageApplication(
                    directory=config['frontend_path'],
                    html=True))
        await serve(app, server_config)

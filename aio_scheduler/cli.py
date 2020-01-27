"""Console script for aio_scheduler."""
import sys
import logging
import os
import asyncio
import importlib

import click
from daemon import DaemonContext

from .utils import maybe_future
from .adapter import RedisAdapter
from .job import Job
from . import worker


logging.basicConfig(level=logging.INFO)
Job.logger = logging.getLogger('aio_scheduler')


@click.group()
def cli(): pass


@cli.command('start')
@click.option('--daemon', is_flag=True)
@click.option('--init-script')
def start(daemon=False, init_script=False):
    async def main():
        if init_script:
            sys.path.insert(0, '.')
            importlib.import_module(init_script)

        worker_instance = worker.worker_class()
        await maybe_future(worker_instance.initialize())

        if daemon:
            with DaemonContext():
                await worker_instance.start()
        else:
            await worker_instance.start()
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(cli())

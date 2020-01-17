"""Console script for aio_scheduler."""
import sys
import logging
import os
import asyncio

import click
from daemon import DaemonContext

from .adapter import RedisAdapter
from .job import Job


logging.basicConfig(level=logging.INFO)
Job.logger = logging.getLogger('aio_scheduler')


@click.group()
def cli(): pass


@cli.command('start')
@click.option('--daemon', is_flag=True)
def start(daemon=False):
    async def main():
        sys.path.insert(0, os.getcwd())
        Job.adapter = await RedisAdapter.create()
        if daemon:
            with DaemonContext():
                await Job.start_loop()
        else:
            await Job.start_loop()
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(cli())

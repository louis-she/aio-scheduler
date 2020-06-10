import asyncio

from .job import Job
from .adapter import RedisAdapter


class Worker:

    async def initialize(self):
        Job.adapter = await RedisAdapter.create()
        self._stop = False

    async def start(self):
        self._done = False
        while True:
            if self._stop:
                break
            Job.logger.debug('checking redis')
            for encode in await Job.adapter.dequeue():
                job = Job.deserialize(encode)
                Job.logger.info(f'Get Job.{job.uuid}, encoded: {encode}')
                await job.execute()
            await asyncio.sleep(3)
        self._done = True

    async def stop(self):
        self._stop = True
        while not self._done:
            await asyncio.sleep(0.5)
        await Job.adapter.clean()


worker_class = Worker

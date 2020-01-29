import asyncio

from .job import Job


class Worker:

    def initialize(self):
        pass

    async def start(self):
        while True:
            Job.logger.debug('checking redis')
            for encode in await Job.adapter.dequeue():
                job = Job.deserialize(encode)
                Job.logger.info(f'Get Job.{job.uuid}, encoded: {encode}')
                await job.execute()
            await asyncio.sleep(3)


worker_class = Worker

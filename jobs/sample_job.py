import asyncio
from aio_scheduler import Job


class SampleJob(Job):

    async def perform(self, message):
        await asyncio.sleep(2)
        with open('/tmp/sample.txt', 'w') as f:
            f.write(message)

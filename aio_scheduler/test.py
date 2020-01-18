import asyncio
from datetime import datetime
from aio_scheduler import Job, RedisAdapter

class MyJob(Job):

    async def perform(self, message):
        await asyncio.sleep(2)
        with open('/tmp/my_job.txt', 'w') as f:
            f.write(message)


async def main():
    # globally setup adapter
    Job.adapter = await RedisAdapter.create()

    await MyJob().perform_at(datetime.now(), message='Hey')


if __name__ == '__main__':
    asyncio.run(main())
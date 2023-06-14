import asyncio
from datetime import datetime, timedelta
from aio_scheduler import Job, RedisAdapter
from jobs.sample_job import SampleJob


async def main():
    # globally setup adapter
    Job.adapter = await RedisAdapter.create()

    # execute job right away
    await SampleJob().perform_at(datetime.utcnow(), message='Hey')
    # execute job tomorrow
    await SampleJob().perform_at(datetime.utcnow() + timedelta(days=1), message='Hey in tomorrow')


if __name__ == '__main__':
    asyncio.run(main())

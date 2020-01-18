## aio-scheduler

Async io scheduler based on redis(currently).

# Installation

```
pip install aio-scheduler
```

# Usage

In `sample.py`:

```py
import asyncio
from datetime import datetime, timedelta
from aio_scheduler import Job, RedisAdapter
from jobs.sample_job import SampleJob


async def main():
    # globally setup adapter
    Job.adapter = await RedisAdapter.create()

    # execute job right away
    await SampleJob().perform_at(datetime.now(), message='Hey')
    # execute job tomorrow
    await SampleJob().perform_at(datetime.now() + timedelta(days=1), message='Hey in tomorrow')


if __name__ == '__main__':
    asyncio.run(main())
```


In `jobs/sample_job.py`
```py
import asyncio
from aio_scheduler import Job


class SampleJob(Job):

    async def perform(self, message):
        await asyncio.sleep(2)
        with open('/tmp/sample.txt', 'w') as f:
            f.write(message)

```

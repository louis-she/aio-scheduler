## aio-scheduler

Async io scheduler based on redis(currently).

### Installation

```
pip install aio-scheduler
```

### Usage


1. Start the worker by
```
aio_scheduler start
```

2. Write a class inherit from `Job` class

`jobs/sample_job.py`
```py
import asyncio
from aio_scheduler import Job


class SampleJob(Job):

    async def perform(self, message):
        await asyncio.sleep(2)
        with open('/tmp/sample.txt', 'w') as f:
            f.write(message)

```

3. Call `perform_at` on the `Job` instance like `sample.py` do to enqueue a job at specified datetime.

```py
import asyncio
from datetime import datetime, timedelta
from aio_scheduler import Job, RedisAdapter
from jobs.sample_job import SampleJob


async def main():
    # globally setup adapter
    Job.adapter = await RedisAdapter.create()

    # perform job in current thread
    await SampleJob(message='Hey from main').perform()

    # perform job in worker right away
    await SampleJob(message='Hey from worker').perform_async()

    # perform job in tomorrow
    await SampleJob(message='Hey from the future').perform_at(datetime.now() + timedelta(days=1))


if __name__ == '__main__':
    asyncio.run(main())
```

4. Customized Worker(Optional)

Sometimes the working process needs to be initialied by custom environment(like db, tornado settings etc..), we can achieve this by implementing a custom `Worker` class.

`my_worker.py`

```py
from aio_scheduler import worker, Job, RedisAdapter


class CustomWorker(worker.Worker):

    async def initialize(self):
        # custom initialize
        # Job.tornado_app = my_tornado_application


worker.worker_class = CustomWorker
```

Start the worker:
```
aio_scheduler start --init-script my_worker
```

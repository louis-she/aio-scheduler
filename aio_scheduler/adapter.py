from datetime import datetime

import aioredis


class BaseAdapter:

    def enqueue(self, activate_at: int, encode: str):
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError

    def clean(self):
        pass


class RedisAdapter(BaseAdapter):

    @classmethod
    async def create(cls, redis_server='redis://localhost', scheduled_jobs_key="job:redis_adapter_key"):
        self = cls()
        self.redis_server = redis_server
        self.scheduled_jobs_key = scheduled_jobs_key
        self.redis = await aioredis.create_redis_pool(self.redis_server)
        return self

    async def enqueue(self, activate_at: int, encode: str):
        return await self.redis.zadd(self.scheduled_jobs_key, activate_at, encode)

    async def dequeue(self, time: datetime = None):
        if time is None:
            time = datetime.now()
        records = await self.redis.zrangebyscore(
            self.scheduled_jobs_key,
            max=datetime.timestamp(time),
        )
        await self.redis.zremrangebyscore(
            self.scheduled_jobs_key,
            max=datetime.timestamp(time)
        )
        return records

    async def clean(self):
        self.redis.close()
        await self.redis.wait_closed()

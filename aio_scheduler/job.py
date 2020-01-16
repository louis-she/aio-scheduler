import asyncio
import importlib
import json
from datetime import datetime


class Job:

    adapter = None

    async def perform_at(self, at: datetime, **arguments):
        self.arguments = arguments
        await self.adapter.enqueue(activate_at=int(datetime.timestamp(at)), encode=self.serialize())

    @classmethod
    def deserialize(cls, encoded: str):
        data = json.loads(encoded)
        klass = importlib.import_module(data['class'], data['module'])
        return klass()

    @classmethod
    async def start_loop(cls):
        while True:
            for encode in await cls.adapter.dequeue():
                job = cls.deserialize(encode)
                await job.execute()
            await asyncio.sleep(3)

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'module': self.__module__.__name__,
            'arguments': self.arguments,
        })

    async def execute(self):
        await self.perform(**self.arguments)

    def perform(self):
        raise NotImplementedError

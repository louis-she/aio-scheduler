import asyncio
import importlib
import json
from uuid import uuid4
from datetime import datetime, timedelta

from .utils import maybe_future


class Job:

    adapter = None
    logger = None

    def __init__(self, uuid=None, **arguments):
        self.arguments = arguments
        self.uuid = uuid if uuid else uuid4().hex

    def before_perform(self, *args, **kwargs):
        pass

    def after_perform(self, *args, **kwargs):
        pass

    async def perform_at(self, at: datetime, **arguments):
        self.arguments.update(arguments)
        await self.adapter.enqueue(
            activate_at=int(datetime.timestamp(at)),
            encode=self.serialize())

    async def perform_later(
            self, days=0, seconds=0, microseconds=0,
            milliseconds=0, minutes=0, hours=0, weeks=0, **arguments):
        delta = timedelta(
            days=days, seconds=seconds, microseconds=microseconds,
            milliseconds=milliseconds, minutes=minutes, hours=hours,
            weeks=weeks)
        self.arguments.update(arguments)
        await self.adapter.enqueue(
            activate_at=int(datetime.timestamp(datetime.now() + delta)),
            encode=self.serialize())

    async def perform_async(self, **arguments):
        self.arguments.update(arguments)
        await self.adapter.enqueue(
            activate_at=int(datetime.timestamp(datetime.now())),
            encode=self.serialize()
        )

    @classmethod
    def deserialize(cls, encoded: str):
        data = json.loads(encoded)
        module = importlib.import_module(data['module'], data['class'])
        klass = getattr(module, data['class'])
        return klass(uuid=data['uuid'], **data['arguments'])

    @classmethod
    async def start(cls):
        while True:
            for encode in await cls.adapter.dequeue():
                job = cls.deserialize(encode)
                cls.logger.info(f'Get Job.{job.uuid}, encoded: {encode}')
                await job.execute()
            await asyncio.sleep(3)

    def serialize(self):
        return json.dumps({
            'uuid': self.uuid,
            'class': self.__class__.__name__,
            'module': self.__module__,
            'arguments': self.arguments,
        })

    async def execute(self):
        try:
            await asyncio.wait_for(self._perform(), 30)
            self.logger.info(f'Job.{self.uuid} seccessfully processed')
        except asyncio.TimeoutError:
            self.logger.error(f'Job.{self.uuid} timeout')
            await maybe_future(self.handle_timeout())
        except Exception as e:
            self.logger.error(f'Failed to process Job.{self.uuid}', exc_info=True)
            await maybe_future(self.handle_exception(e))

    async def handle_exception(self, e):
        pass

    async def handle_timeout(self):
        pass

    def perform(self, *args, **kwargs):
        raise NotImplementedError

    async def _perform(self):
        await maybe_future(self.before_perform(**self.arguments))
        await maybe_future(self.perform(**self.arguments))
        await maybe_future(self.after_perform(**self.arguments))
import asyncio
import inspect
import concurrent.futures


def maybe_future(obj):
    if inspect.isawaitable(obj):
        # already awaitable, use ensure_future
        return asyncio.ensure_future(obj)
    elif isinstance(obj, concurrent.futures.Future):
        return asyncio.wrap_future(obj)
    else:
        # could also check for tornado.concurrent.Future
        # but with tornado >= 5 tornado.Future is asyncio.Future
        f = asyncio.Future()
        f.set_result(obj)
        return f

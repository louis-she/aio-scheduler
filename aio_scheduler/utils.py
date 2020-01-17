import asyncio


def maybe_await(func, *args, **kwargs):
    if not asyncio.iscoroutinefunction(func):
        return func(*args, **kwargs)
    return asyncio.get_running_loop().create_task(func(*args, **kwargs))

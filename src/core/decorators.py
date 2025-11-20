import functools
import time
from typing import Any, Callable

from loguru import logger


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Counts function execution time in seconds.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Callable[..., Any]:
        start_time = time.perf_counter()

        result = await func(*args, **kwargs)

        logger.info(
            f"Function {func.__name__} completed in {time.perf_counter() - start_time:.5f} seconds"
        )
        return result

    return wrapper

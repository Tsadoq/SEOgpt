import asyncio
from typing import Iterable, Coroutine, Any


async def concurrency_with_semaphores(coroutines: Iterable[Coroutine], num_concurrent_tasks: int = 3) -> Any:
    """
    Gather async tasks with maximum number of concurrent processes
    :param coroutines: The iterable of Coroutines to gather
    :param num_concurrent_tasks: the maximum amount of concurrent processes
    :return: The result of the coroutines to gather
    """
    semaphore = asyncio.Semaphore(num_concurrent_tasks)

    async def semaphore_coroutine(coroutine: Coroutine) -> Coroutine:
        async with semaphore:
            return await coroutine

    return await asyncio.gather(*(semaphore_coroutine(coroutine) for coroutine in coroutines))

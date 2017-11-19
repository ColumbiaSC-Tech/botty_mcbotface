# Testing routine/task-queue overeager threading
import asyncio
import concurrent.futures


# Async/MultiThread searching all channels
@asyncio.coroutine
def routine_test(_loop):
    """
    Async periodic task to keep db Channels and Users tables up to date.
    :param _loop: Routine delegated asyncio event loop.
    :return:
    """
    print('routine_test::RUNNING')

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # print(executor.__dict__)
    tasks = [lambda: 1 + 1, lambda: 2 + 2]

    def periodic(loop):
        with executor:
            futures = [loop.run_in_executor(executor, t) for t in tasks]
            yield from asyncio.gather(*futures)

    yield from periodic(_loop)

import asyncio
import concurrent.futures
from botty_mcbotface.botty.db import populate_channels, populate_users

print('working')


# Async/MultiThread searching all channels
async def pool_api_search():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [loop.run_in_executor(executor, client.search.messages, s) for s in searches]

        return [res.body for res in await asyncio.gather(*futures)]


results = loop.run_until_complete(pool_api_search())

task = asyncio.ensure_future(populate_periodic)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)

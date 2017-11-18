import asyncio
import threading
from botty_mcbotface.botty.db.routines.populate_db import populate_periodic


#######################
#   Main task queue   #
#######################
def async_queue():
    print('async-queue')
    # Start a new event loop for async requests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Set and start async work thread
    work = threading.Thread(target=lambda: loop.run_until_complete(populate_periodic(loop)))
    work.start()

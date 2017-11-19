import os
import asyncio
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from importlib import import_module
from importlib.util import find_spec
from botty_mcbotface.botty.db.routines.populate_db import populate_periodic

# Main scheduler instantiation
scheduler = BackgroundScheduler()
print(os.listdir(os.curdir))


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


def async_queue_scheduler():
    print('scheduler started')
    scheduler.add_job(async_queue, 'interval', seconds=15)
    scheduler.start()

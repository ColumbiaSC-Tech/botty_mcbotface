import os
import re
import asyncio
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from importlib import import_module

# Main scheduler instantiation
scheduler = BackgroundScheduler()

# Create task queue from routines in routines dir.
r_match = re.compile('^routine_')
r_path = os.listdir(__name__.replace('.', '/'))
routines = [r.split('.py')[0] for r in r_path if r_match.match(r)]

# Todo: CHeck on thread limiting. ThreadPoolExecutor seems to spawn threads infinitely
#######################
#   Main task queue   #
#######################

def spawn_task_thread(routine):

    print('Jobs::', scheduler.get_jobs())
    print('Threads::', len(threading.enumerate()))

    # Start a new event loop for async requests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Spawn and start routine work threads
    work = threading.Thread(target=lambda: loop.run_until_complete(routine(loop)))
    work.start()
    # return loop.run_until_complete(routine(loop))


def task_queue_scheduler():
    print('scheduler started', routines)
    for r in routines:
        routine = getattr(import_module('.'.join([__name__, r])), r)
        scheduler.add_job(lambda: spawn_task_thread(routine), 'interval', seconds=1)

    scheduler.start()

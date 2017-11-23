import os
import logging
import re
import asyncio
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from importlib import import_module

logger = logging.getLogger(__name__)
logger.info('INFO WORKING')

# Main scheduler instantiation
scheduler = BackgroundScheduler(daemon=False)

# TODO: Explain routine naming convention. Also move this to run.py and have task_queue_scheduler accept routines and interval


def get_default_routines():
    # Create task queue from routines in routines dir.
    r_match = re.compile('^routine_')
    r_path = os.listdir(__name__.replace('.', '/'))
    routines = [r.split('.py')[0] for r in r_path if r_match.match(r)]
    return routines


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
    return work.start()


def task_queue_scheduler(routines):
    print('scheduler started', routines)
    for r in routines:
        routine, interval = getattr(import_module('.'.join([__name__, r])), r, 'INTERVAL')
        scheduler.add_job(lambda: spawn_task_thread(routine), 'interval', seconds=interval)
        spawn_task_thread(routine)

    return scheduler.start()

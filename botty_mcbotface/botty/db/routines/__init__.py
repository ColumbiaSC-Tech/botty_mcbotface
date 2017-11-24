import os
import logging
import re
import asyncio
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from botty_mcbotface.utils.tools import WorkThread
from importlib import import_module

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

    # logging.info('Jobs::{}'.format(scheduler.get_jobs()))
    logging.info('Threads::{}'.format(len(threading.enumerate())))

    # Start a new event loop for async requests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Spawn and start routine work threads
    # work = WorkThread(target=lambda: loop.run_until_complete(routine(loop)), daemon=False)
    # return work.run_interval(10)
    work = WorkThread(task=lambda: loop.run_until_complete(routine(loop)), interval=5)
    work.run()


def task_queue_scheduler(routines):
    logging.info('scheduler started::{}'.format(routines))

    # def routine_queue():
        # queue = []
        # for r in routines:
        #     routine = getattr(import_module('.'.join([__name__, r])), r)
        #     scheduler.add_job(lambda: spawn_task_thread(routine), 'interval', seconds=5)
            # queue.append(spawn_task_thread(routine))
        # return queue

    for r in routines:
        routine = getattr(import_module('.'.join([__name__, r])), r)
        scheduler.add_job(lambda: spawn_task_thread(routine), 'interval', seconds=5)

    # print('QUEUE::\n', routine_queue())
    # main_work_thread = WorkThread(daemon=True, interval=5)
    # main_work_thread.run_queue(routine_queue)
    main_work_thread = WorkThread(task=scheduler.start, daemon=True, interval=5)
    # main_work_thread.run_queue(routine_queue)
    return main_work_thread.run()

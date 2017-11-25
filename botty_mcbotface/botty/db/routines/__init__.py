import os
import logging
import re
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
    logging.info('Jobs::{}'.format(scheduler.get_jobs()))
    logging.info('Threads::{}'.format(len(threading.enumerate())))
    work = WorkThread(task=routine)
    return work.run


def task_queue_scheduler():
    for r in get_default_routines():
        routine = getattr(import_module('.'.join([__name__, r])), r)
        print('ROUTINE::', routine)

        # TODO: Make an accessible interval property on routine modules
        scheduler.add_job(spawn_task_thread, 'interval', args=(routine,), seconds=5)

    main_work_thread = threading.Thread(target=scheduler.start, daemon=True)
    main_work_thread.run()

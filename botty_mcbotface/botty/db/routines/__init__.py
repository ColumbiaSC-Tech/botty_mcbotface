import os
import re
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from botty_mcbotface import log
from botty_mcbotface.utils.tools import AsyncWorkThread
from importlib import import_module

"""
In order for routines to be registered properly the 
following naming conventions must be followed:

* The routine filename should start with "routine_".

* The routine file should have only one routine to run.

* The name of the routine function should be the same as the .py filename.

(See routine_populate_db.py for an example)
"""

# Main scheduler instantiation
scheduler = BackgroundScheduler(daemon=False)

# TODO: Have task_queue_scheduler accept routines and interval


def get_default_routines():
    """
    Create task queue from routines in routines dir.
    :return: A list of routine module/function pair names
    """
    r_match = re.compile('^routine_')
    r_path = os.listdir(__name__.replace('.', '/'))
    routines = [r.split('.py')[0] for r in r_path if r_match.match(r)]

    return routines


# *** Main task queue *** #

def spawn_task_thread(routine):
    """
    Utility function for dynamically generating WorkerThread's for registered routines.
    :param routine: Name of routine module/function to generate a worker for.
    :return: The `run` method for the newly created worker thread.
    """
    work = AsyncWorkThread(task=routine)

    return work.run


def task_queue_scheduler():
    """
    Manages the creation of worker threads and their schedules.
    :return:
    """
    for r in get_default_routines():
        routine = getattr(import_module('.'.join([__name__, r])), str(r))
        interval = getattr(import_module('.'.join([__name__, 'INTERVAL'])), str(r))

        # TODO: Make an accessible interval property on routine modules
        scheduler.add_job(spawn_task_thread, 'interval', args=(routine,), seconds=interval)
        log.info('Registered routine: %s', routine.__name__)

    main_work_thread = threading.Thread(target=scheduler.start, daemon=True)
    main_work_thread.run()

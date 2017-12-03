import threading
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from asyncio import coroutines, new_event_loop, set_event_loop

# Main scheduler instantiation
scheduler = BackgroundScheduler(daemon=False)


class AsyncWorkThread(object):
    """
    Custom Thread class that accepts functions to run async in
    event loop in a new thread.

    This thread has only one job, to run the given task. It is
    then managed by APScheduler parent thread (BackgroundScheduler).
    """
    def __init__(self, task, daemon=False):
        """
        :param task: Properly formatted routine to run async in thread.
        :param daemon: Boolean indicating the worker thread is daemon or not.
        """
        self.thread = threading.Thread(target=self.run, args=(task,), daemon=daemon)
        self.thread.daemon = daemon
        self.thread.start()

    @staticmethod
    def run(task):
        """
        Set, start then close the async task event loop.
        :param task: Function to run as a scheduled task.
        """
        loop = new_event_loop()
        set_event_loop(loop)
        loop.run_until_complete(task())
        loop.close()


def start_task_runner():
    """Starts the scheduler by delegating it to a daemon thread."""
    main_work_thread = threading.Thread(target=scheduler.start, daemon=True)
    main_work_thread.run()


def stop_task_runner():
    """Stops the task-runner, scheduler and task threads."""
    scheduler.shutdown()


def spawn_task_thread(routine):
    """
    Utility function for dynamically generating WorkerThread's for registered routines.
    :param routine: Name of routine module/function to generate a worker for.
    :return work.run: The `run` method for the newly created worker thread.
    """
    work = AsyncWorkThread(task=routine)

    return work.run


def register_routine(interval, routine):
    """
    Adds a new routine to the scheduler. This can be done at any time before, during,
    or after the scheduler has started.
    :param routine: Function to run at a given time interval.
    :param interval: The interval (seconds) at which to run the function.
    :return scheduler.add_job(*):
    """
    return scheduler.add_job(spawn_task_thread, 'interval', args=(routine,), seconds=interval)


def bot_routine(interval, delay=True):
    """
    Function decorator to designate function as a task.
    :param interval: Interval in seconds to run the task.
    :param delay: Boolean indicating whether to run task immediately or offset by interval.
    :return decorator:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not delay:
                AsyncWorkThread.run(coroutines.coroutine(lambda: func(*args, **kwargs)))
            return register_routine(interval, coroutines.coroutine(lambda: func(*args, **kwargs)))
        return wrapper()
    return decorator

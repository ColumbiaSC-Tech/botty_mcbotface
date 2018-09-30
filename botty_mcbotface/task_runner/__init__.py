import threading
from apscheduler.schedulers.background import BackgroundScheduler
from asyncio import coroutines, new_event_loop, set_event_loop
from botty_mcbotface import log, bot_tz
from time import sleep
from typing import Callable

# Main scheduler instantiation
scheduler = BackgroundScheduler(daemon=False, timezone=bot_tz)


class AsyncWorkThread(object):
    """
    Custom Thread class that accepts functions to run async in
    event loop in a new thread.

    This thread has only one job, to run the given task. It is
    then managed by APScheduler parent thread (BackgroundScheduler).
    """

    def __init__(self, task: Callable, delay=0, daemon=False):
        """
        :param task: Properly formatted routine to run async in thread.
        :param daemon: Boolean indicating the worker thread is daemon or not.
        """
        self.thread = threading.Thread(target=self.run, args=(task, delay), daemon=daemon)
        self.thread.daemon = daemon
        self.thread.start()

    @staticmethod
    def run(task: Callable, delay=0, debug=False):
        """
        Set, start then close the async task event loop.
        :param task: Function to run as a scheduled task.
        :param delay: Optional delay in seconds before running task.
        :param debug: Optional debug logging.
        """

        if delay > 0:
            sleep(delay)

        if debug:
            for job in scheduler.get_jobs():
                if hasattr(job, 'next_run_time'):
                    log.info(job.next_run_time)

        loop = new_event_loop()
        set_event_loop(loop)
        loop.run_until_complete(task())
        # log.info('RAN::', delay, task)
        loop.close()


def start_task_runner():
    """Starts the scheduler by delegating it to a daemon thread."""
    main_work_thread = threading.Thread(target=scheduler.start, daemon=True)
    main_work_thread.run()


def stop_task_runner():
    """Stops the task-runner, scheduler and task threads."""
    scheduler.shutdown()


def spawn_task_thread(routine: Callable):
    """
    Utility function for dynamically generating WorkerThread's for registered routines.
    :param routine: Name of routine module/function to generate a worker for.
    :return AsyncWorkThreadrun: The newly created worker thread.
    """
    return AsyncWorkThread(task=routine)


def register_routine_cron(cron: dict, routine: Callable):
    """
    Adds a new cron triggered routine to the scheduler. This can be done at any time before, during,
    or after the scheduler has started.
    :param routine: Function to run at a given time interval.
    :param cron: A dictionary containing keyword arguments for APScheduler cron trigger.
    :return scheduler.add_job(*):
    """
    return scheduler.add_job(spawn_task_thread, 'cron', args=(routine,), **cron)


def register_routine_interval(interval: int, routine: Callable):
    """
    Adds a new interval triggered routine to the scheduler. This can be done at any time before,
    during, or after the scheduler has started.
    :param routine: Function to run at a given time interval.
    :param interval: The interval (seconds) at which to run the function.
    :return scheduler.add_job(*):
    """
    return scheduler.add_job(spawn_task_thread, 'interval', args=(routine,), seconds=interval)


def bot_routine(interval, cron=None, delay=0, run_once=False):
    """
    Function decorator to designate function as a task.
    :param interval: Interval
        if cron=False:
            seconds to run the task.
        else:
            dict containing cron day/time params
    :param cron: Boolean indicating whether to run task as cron job or interval in seconds.
    :param delay: Integer indicating whether to run task immediately or offset by interval.
    :param run_once: Boolean indicating whether to run task once or as a routine.
    :return decorator:
    """

    def decorator(func):
        def wrapper(*args, **kwargs):

            # Wrap the function/task as coroutine
            coro = coroutines.coroutine(lambda: func(*args, **kwargs))

            if run_once or delay:
                assert not cron, 'Cron jobs do not support delays'

            if cron:
                return register_routine_cron(cron, coro)

            elif delay:
                if run_once:
                    return AsyncWorkThread(coro, delay=delay)

                # Send coroutine with delay to run before registered
                AsyncWorkThread(coro, delay=delay)

                return threading.Timer(delay, lambda: register_routine_interval(interval, coro) and None).start()

            elif run_once:
                # Return before routine is registered
                return AsyncWorkThread(coro)

            else:
                # Run once immediately before registering with interval
                AsyncWorkThread(coro)

            return register_routine_interval(interval, coro)

        # Invoke the wrapped function immediately
        return wrapper()

    return decorator

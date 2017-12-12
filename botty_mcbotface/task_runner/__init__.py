import threading
from apscheduler.schedulers.background import BackgroundScheduler
from asyncio import coroutines, new_event_loop, set_event_loop
from botty_mcbotface import log, bot_tz
from time import sleep

# Main scheduler instantiation
scheduler = BackgroundScheduler(daemon=False, timezone=bot_tz)

# FIXME: Delay is fucked

class AsyncWorkThread(object):
    """
    Custom Thread class that accepts functions to run async in
    event loop in a new thread.

    This thread has only one job, to run the given task. It is
    then managed by APScheduler parent thread (BackgroundScheduler).
    """
    def __init__(self, task, delay=0, daemon=False):
        """
        :param task: Properly formatted routine to run async in thread.
        :param daemon: Boolean indicating the worker thread is daemon or not.
        """
        self.thread = threading.Thread(target=self.run, args=(task, delay), daemon=daemon)
        self.thread.daemon = daemon
        self.thread.start()

    @staticmethod
    def run(task, delay, debug=False):
        """
        Set, start then close the async task event loop.
        :param task: Function to run as a scheduled task.
        :param delay: Optional delay in seconds before running task.
        :param debug: Optional debug logging.
        """
        print('in run', delay)

        if delay > 0:
            sleep(delay)

        if debug:
            for job in scheduler.get_jobs():
                if hasattr(job, 'next_run_time'):
                    log.info(job.next_run_time)
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


def spawn_task_thread(routine, delay):
    """
    Utility function for dynamically generating WorkerThread's for registered routines.
    :param routine: Name of routine module/function to generate a worker for.
    :param delay: Optional delay for first run.
    :return work.run: The `run` method for the newly created worker thread.
    """
    if delay > 0:
        # Delay for first run
        print('Delay for first run', delay)
        AsyncWorkThread.run(routine, delay=delay)

    return AsyncWorkThread(task=routine).run


def register_routine_cron(interval, routine):
    """
    Adds a new cron triggered routine to the scheduler. This can be done at any time before, during,
    or after the scheduler has started.
    :param routine: Function to run at a given time interval.
    :param interval: A dictionary containing keyword arguments for APScheduler cron trigger.
    :return scheduler.add_job(*):
    """
    print('REALLy?')
    return scheduler.add_job(spawn_task_thread, 'cron', args=(routine, 0), **interval)


def register_routine_interval(interval, routine, delay=0):
    """
    Adds a new interval triggered routine to the scheduler. This can be done at any time before,
    during, or after the scheduler has started.
    :param routine: Function to run at a given time interval.
    :param interval: The interval (seconds) at which to run the function.
    :return scheduler.add_job(*):
    """
    return scheduler.add_job(spawn_task_thread, 'interval', args=(routine,), kwargs={'delay':delay}, seconds=interval)


def bot_routine(interval, cron=False, delay=0, run_once=False):
    """
    Function decorator to designate function as a task.
    :param interval: Interval
        if cron=False:
            seconds to run the task.
        else:
            dict containing cron day/time params
    :param cron: Boolean indicating whether to run task as cron job or interval in seconds.
    :param delay: Integer or None indicating whether to run task immediately or offset by interval.
    :param run_once: Boolean indicating whether to run task once or as a routine.
    :return decorator:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('delay', delay)
            # wrap the function/task as coroutine
            coro = coroutines.coroutine(lambda: func(*args, **kwargs))

            if run_once or delay:
                assert cron is False, 'Cron jobs do not support delays'

            if run_once and delay:
                # return before routine is registered and run coro with a delay
                return AsyncWorkThread.run(coro, delay=delay)

            elif run_once:
                # return before routine is registered
                return AsyncWorkThread.run(coro)

            elif delay:
                return register_routine_interval(interval, coro, delay=delay)

            if not delay and not cron:
                # run once immediately before registering with interval
                AsyncWorkThread.run(coro)

            if cron:
                return register_routine_cron(interval, coro)

            return register_routine_interval(interval, coro)

        # invoke the wrapped function immediately
        return wrapper()
    return decorator

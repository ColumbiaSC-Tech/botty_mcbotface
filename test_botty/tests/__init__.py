from botty_mcbotface.task_runner import stop_task_runner


def tearDownModule():
    """called once, after everything else in this module"""
    stop_task_runner()

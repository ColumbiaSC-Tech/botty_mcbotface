import logging

# Setup application logger
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# TODO: Config logger for error logging to file in prod
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def init_db():
    """Setup database and db routines/task-queue"""

    from botty_mcbotface.botty.db import Base, db

    # Initialize db
    Base.metadata.create_all(bind=db.engine)

    from botty_mcbotface.task_runner import start_task_runner
    import botty_mcbotface.botty.db.routines

    # Start the default task queue
    start_task_runner()


init_db()

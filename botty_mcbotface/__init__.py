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

    from botty_mcbotface.tasq_runner import start_tasq
    import botty_mcbotface.botty.db.routines

    # Start the default task queue
    start_tasq()


init_db()

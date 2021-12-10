import shutil
import tempfile

from examples.config import *
from src.palpable.servants.server import Server


class ExampleServer(Server):
    def __init__(self):
        super(ExampleServer, self).__init__(
            logging_folder=tempfile.mkdtemp(),
            address=SERVER_ADDRESS,
            family=SERVER_FAMILY,
            authkey=SECRET,
            num_workers=NUM_OF_WORKERS,
            task_timeout_seconds=TASK_TIMEOUT_SECONDS,
            result_retention_capacity=RESULT_RETENTION_CAPACITY,
            result_retention_seconds=RESULT_RETENTION_SECONDS,
        )

    def close(self):
        super(ExampleServer, self).close()
        shutil.rmtree(self._logging_folder)



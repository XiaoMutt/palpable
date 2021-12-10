import shutil
import tempfile
from unittest import TestCase

from src.palpable.servants.server import Server
from src.palpable.units.client import Client

address = ("127.0.0.1", 8087)
family = "AF_INET"
secret = b"29r8in389rhd"


class TesterClient(Client):
    def __init__(self):
        super(TesterClient, self).__init__(address, family, secret)


class TesterServer(Server):
    def __init__(self, logging_folder,
                 num_of_workers,
                 task_timeout_seconds,
                 result_retention_capacity,
                 result_retention_seconds
                 ):
        super(TesterServer, self).__init__(logging_folder,
                                           address, family, secret,
                                           num_of_workers,
                                           task_timeout_seconds,
                                           result_retention_capacity,
                                           result_retention_seconds
                                           )


class BaseTest(object):
    class Case(TestCase):
        num_of_workers = 4
        task_timeout_seconds: float = 3600 * 3
        result_retention_capacity = 100000
        result_retention_seconds: float = 60

        server: TesterServer
        client: TesterClient

        logging_folder = tempfile.mkdtemp()

        @classmethod
        def setUpClass(cls) -> None:
            cls.client = TesterClient()
            cls.server = TesterServer(cls.logging_folder,
                                      cls.num_of_workers,
                                      cls.task_timeout_seconds,
                                      cls.result_retention_capacity,
                                      cls.result_retention_seconds).start()

        @classmethod
        def tearDownClass(cls) -> None:
            shutil.rmtree(cls.logging_folder)
            cls.server.stop()
            cls.server.join()
            cls.server.close()

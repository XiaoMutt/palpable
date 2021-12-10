import typing as tp
from io import StringIO
from multiprocessing.queues import Queue as ProcessQueue

import dill

from ..basis.immutable import Immutable
from ..units.task import Task
from ..units.task_result import TaskResult


class Messenger(Immutable):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUBMIT = "SUBMIT"
    QUERY = "QUERY"

    RESULT = "RESULT"

    def __init__(self, to_thread_queue: ProcessQueue, to_process_queue: ProcessQueue):
        """
        Used by Worker process to exchange information with the Worker thread.
        :param to_thread_queue: the queue receives message from the Worker process and get by the Worker Thread
        :param to_process_queue: the queue receives message from the Worker thread and get by the Worker Process
        """
        self.to_thread_queue = to_thread_queue
        self.to_process_queue = to_process_queue

    def debug(self, message: str):
        self.to_thread_queue.put((self.DEBUG, message))

    def info(self, message: str):
        self.to_thread_queue.put((self.INFO, message))

    def warning(self, message: str):
        self.to_thread_queue.put((self.WARNING, message))

    def error(self, message: str):
        self.to_thread_queue.put((self.ERROR, message))

    def print(self, *args, **kwargs):
        with StringIO() as buf:
            kwargs["file"] = buf
            kwargs["flush"] = True
            print(*args, **kwargs)
            self.info(buf.getvalue())

    def submit_tasks(self, tasks: tp.List[Task]):
        """
        submit Tasks to Server
        """

        self.to_thread_queue.put((self.SUBMIT, dill.dumps(tasks)))

    def query_results(self, task_ids: tp.List[str]) -> tp.List[tp.Optional[TaskResult]]:
        """
        Query a list of task_ids with results
        This method blocks until results return
        """
        self.to_thread_queue.put((self.QUERY, task_ids))
        results = self.to_process_queue.get()
        res = dill.loads(results)
        return res

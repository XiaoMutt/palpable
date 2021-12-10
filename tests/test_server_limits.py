from time import sleep

from src.palpable.procedures.run_function import RunFunction
from src.palpable.units.task_exceptions import TaskTimeout
from tests.basis import BaseTest


def long_task(*args):
    sleep(5)
    return True


def square(num):
    return num * num


class TestServerLimits(BaseTest.Case):
    task_timeout_seconds = 3
    result_retention_capacity = 2
    result_retention_seconds = 5

    def test_timeout(self):
        with self.assertRaises(TaskTimeout):
            self.client.run(long_task, None)

    def test_result_retention_capacity(self):
        result1 = self.client.run_procedure(RunFunction(square, 5), 0)
        self.assertEqual(None, result1.is_successful)
        sleep(1)  # wait 1 second to make sure the task get submitted and finished

        result2 = self.client.run_procedure(RunFunction(square, 7), 0)
        self.assertEqual(None, result2.is_successful)
        sleep(1)  # wait 1 second to make sure the task get submitted and finished

        result3 = self.client.run_procedure(RunFunction(square, 11), 0)
        self.assertEqual(None, result3.is_successful)
        sleep(1)  # wait 1 second to make sure the task get submitted and finished

        resultA = self.client.query_result(result1.task_id)
        self.assertEqual(None, resultA)  # task1 has been outdated because the capacity is 2

        resultB = self.client.query_result(result2.task_id)
        self.assertEqual(49, resultB.data)  # task2 result is taken out

        result4 = self.client.run_procedure(RunFunction(square, 13), 0)
        self.assertEqual(None, result4.is_successful)
        sleep(1)  # wait 1 second to make sure the task get submitted and finished

        resultC = self.client.query_result(result3.task_id)
        self.assertEqual(121, resultC.data)

        resultD = self.client.query_result(result4.task_id)
        self.assertEqual(169, resultD.data)

    def test_result_retention_seconds(self):
        result1 = self.client.run_procedure(RunFunction(square, 5), 0)
        self.assertEqual(None, result1.is_successful)
        sleep(3)

        result2 = self.client.run_procedure(RunFunction(square, 7), 0)
        self.assertEqual(None, result2.is_successful)
        sleep(1)

        status = self.server.status
        self.assertEqual(0, status["task_queue_size"])
        self.assertEqual(2, status["result_cache_size"])

        sleep(3)  # expire result1

        resultA = self.client.query_result(result1.task_id)
        self.assertEqual(None, resultA)
        resultB = self.client.query_result(result2.task_id)
        self.assertEqual(49, resultB.data)

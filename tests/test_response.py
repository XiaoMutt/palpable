from math import sqrt
from time import sleep

from src.palpable.procedures.map_function import MapFunction
from src.palpable.procedures.procedure import Procedure
from src.palpable.procedures.run_function import RunFunction
from src.palpable.units.task import Task
from src.palpable.units.task_response import TaskResponse
from tests.basis import BaseTest

TEST_DATA = tuple([x * x for x in range(10)])


class SqrtNegative(Procedure):
    def __init__(self, nums):
        self.nums = nums

    def run(self, messenger):
        messenger.submit_tasks([Task(RunFunction(sqrt, -num)) for num in self.nums], need_followup=True)
        return True


class TestResponse(BaseTest.Case):
    num_of_workers = 1  # use only one worker

    def test_tbd(self):
        response = self.client.ajax_run_procedure(MapFunction(sqrt, TEST_DATA), 0)
        self.assertEqual(TaskResponse.TBD.__name__, response["status"])

    def test_success(self):
        response = self.client.ajax_run_procedure(MapFunction(sqrt, TEST_DATA), -1)
        self.assertEqual(TaskResponse.SUCCESS.__name__, response["status"])
        self.assertEqual(tuple(map(sqrt, TEST_DATA)), tuple(response["data"]))

    def test_error(self):
        response = self.client.ajax_run_procedure(MapFunction(sqrt, [-1]), -1)
        self.assertEqual(TaskResponse.ERROR.__name__, response["status"])

    def test_none(self):
        response = self.client.ajax_query_result("abc")
        self.assertEqual(TaskResponse.NONE.__name__, response["status"])

    def test_followup_ids(self):
        response = self.client.ajax_run_procedure(SqrtNegative([-x for x in TEST_DATA]), -1)
        self.assertEqual(TaskResponse.SUCCESS.__name__, response["status"])
        self.assertTrue(response["status"])
        self.assertEqual(len(TEST_DATA), len(response["followup_task_ids"]))

        followup_task_ids = set(response["followup_task_ids"])
        results = []
        while len(followup_task_ids) > 0:
            sleep(0.1)
            done = set()
            for task_id in followup_task_ids:
                r = self.client.ajax_query_result(task_id)
                self.assertTrue(r["status"] != TaskResponse.NONE.__name__)
                self.assertTrue(r["status"] != TaskResponse.ERROR.__name__)
                if r["status"] == TaskResponse.SUCCESS.__name__:
                    results.append(r["data"])
                    done.add(task_id)
            followup_task_ids -= done
        self.assertEqual(tuple(map(sqrt, TEST_DATA)), tuple(sorted(results)))

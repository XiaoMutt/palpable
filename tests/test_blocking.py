from src.palpable.procedures.run_function import RunFunction
from tests.basis import BaseTest, TesterClient


def square(num):
    return num * num


def distribute(nums):
    # blocking at this process and waiting for map function to finish
    return TesterClient().map(square, nums)


class TestBlocking(BaseTest.Case):
    num_of_workers = 1  # use only one worker

    def test_blocking(self):
        result = self.client.run_procedure(RunFunction(distribute, range(10)), -1)
        self.assertTrue(result.is_successful)
        self.assertEqual(tuple([i * i for i in range(10)]), tuple(result.data))
        self.assertEqual(0, len(result.followup_task_ids))

from src.palpable.units.task_exceptions import TaskFailed
from tests.basis import BaseTest, TesterClient


class CustomException(Exception):
    pass


def failed(*args):
    raise TaskFailed("task failed")


def custom_error(*args):
    raise CustomException("custom exception")


def square(num):
    return num * num


def double(num):
    return 2 * num


def distribute(nums):
    # blocking at this process and waiting for map function to finish
    return TesterClient().map(square, nums)


class TestRunFunction(BaseTest.Case):

    def test_run_function(self):
        result = self.client.run(square, 5)
        self.assertEqual(25, result)

    def test_map_function(self):
        result = self.client.map(square, range(100))
        self.assertEqual(tuple([i * i for i in range(100)]), tuple(result))

    def test_high_volume(self):
        result = self.client.map(double, range(1000))
        self.assertEqual(tuple([2 * i for i in range(1000)]), tuple(result))

    def test_failed(self):
        with self.assertRaises(TaskFailed):
            self.client.run(failed, None)

    def test_custom_exception(self):
        with self.assertRaises(CustomException):
            self.client.run(custom_error, None)

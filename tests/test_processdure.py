import math

from src.palpable.procedures.map_function import MapFunction
from src.palpable.procedures.procedure import Procedure
from src.palpable.units.task import Task
from tests.basis import BaseTest


def is_prime(x):
    print(f"checking {x}")
    i = 2
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


class GetPrimeNumbers(Procedure):
    def __init__(self, num):
        """
        Check if all the nums are odd numbers
        """
        self.num = num

    def run(self, messenger):
        is_prime.__globals__["print"] = messenger.print
        candidates = range(2, self.num + 1)
        results = messenger.run_procedure(MapFunction(is_prime, candidates))
        res = []
        for num, result in zip(candidates, results):
            if result:
                res.append(num)
        return res


class IntegerFactorization(Procedure):
    def __init__(self, nums):
        """
        Check if the nums are all odd, if so double the value of the nums
        :param nums: odd numbers
        """
        self.nums = nums

    def run(self, messenger):
        messenger.info("get prime numbers")
        prime_numbers = messenger.run_procedure(GetPrimeNumbers(max(self.nums)))

        def get_factors(x):
            res = []
            while x > 1:
                for prime in prime_numbers:
                    if prime > x:
                        break

                    if x % prime == 0:
                        res.append(prime)
                        x /= prime
                        break
            return res

        return messenger.run_procedure(MapFunction(get_factors, self.nums))


class GCD(Procedure):
    def __init__(self, a, b):
        self.a = min(a, b)
        self.b = max(a, b)

    def run(self, messenger):
        messenger.info(f"find GCD of {self.a} and {self.b}")
        if self.a > 0:
            task = Task(GCD(self.a, self.b % self.a))
            messenger.submit_tasks([task], need_followup=True)
        return self.b


class TestProcedure(BaseTest.Case):

    def test_procedure(self):
        result = self.client.run_procedure(IntegerFactorization([5, 9, 45]), waiting_seconds=-1)
        self.assertTrue(result.is_successful)
        self.assertEqual(((5,), (3, 3), (3, 3, 5)), tuple([tuple(r) for r in result.data]))

    def test_followup(self):
        a = 1362
        b = 67365
        result = self.client.run_procedure(GCD(a, b), waiting_seconds=-1)
        self.assertTrue(result.is_successful)
        self.assertEqual(1, len(result.followup_task_ids))
        while len(result.followup_task_ids) > 0:
            followup_id = result.followup_task_ids[0]
            while True:
                result = self.client.query_result(followup_id)
                self.assertTrue(result is not None)
                self.assertTrue(result.is_successful is not False)
                if result.is_successful:
                    break
        self.assertEqual(3, result.data)

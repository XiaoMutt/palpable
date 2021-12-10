from src.palpable.procedures.procedure import Procedure
from src.palpable.units.task import Task


def square(x):
    return x * x


def double(x):
    print(f"processing {x}")
    return 2 * x


class CheckIfOdd(Procedure):
    def __init__(self, nums):
        """
        Check if all the nums are odd numbers
        """
        self.nums = nums

    def run(self, messenger):
        for n in self.nums:
            if n % 2 == 0:
                return False
        return True


class DoubleOddNumberProc(Procedure):
    def __init__(self, nums):
        """
        Check if the nums are all odd, if so double the value of the nums
        :param nums: odd numbers
        """
        self.nums = nums

    def run(self, messenger):
        double.__globals__["print"] = messenger.print  # inject messenger.print as print

        messenger.info("check if the numbers are all odd numbers")
        # submit new CheckIfOddTask
        # is_source_blocking is set to True because, we are waiting for the results before moving on
        check_if_odd_task = Task(CheckIfOdd(self.nums), is_source_blocking=True)

        # submit tasks. ATTENTION: submit_tasks accepts a list of tasks as arguments
        messenger.submit_tasks([check_if_odd_task])

        # query results. ATTENTION: query_results accepts a list of task_ids as arguments and return a list of
        # TaskResults
        while True:
            result = messenger.query_results([check_if_odd_task.task_id])[0]
            if result is None:
                # no such task
                raise Exception(f"The check_if_odd_task (ID: {check_if_odd_task.task_id}) does not exist. "
                                f"This should not occur.")
            else:
                if result.is_successful is True:
                    # task successful
                    check_if_odd_task_result = result.data
                    break

                elif result.is_successful is False:
                    # task unsuccessful
                    if isinstance(result.data, Exception):
                        raise result.data
                    else:
                        raise Exception(str(result.data))
                else:
                    # task is still running
                    pass

        if not check_if_odd_task_result:
            raise Exception("Error: the given numbers are not all odd")

        res = [double(x) for x in self.nums]

        return res

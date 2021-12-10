from src.palpable.procedures.procedure import Procedure


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
        # submit new CheckIfOdd procedure and wait for results
        check_if_odd_task_result = messenger.run_procedure(CheckIfOdd(self.nums))

        if not check_if_odd_task_result:
            raise Exception("Error: the given numbers are not all odd")

        res = [double(x) for x in self.nums]

        return res

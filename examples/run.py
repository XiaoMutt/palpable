from examples.example_client import ExampleClient
from examples.example_server import ExampleServer
from utils import square, DoubleOddNumberProc

if __name__ == "__main__":
    with ExampleServer() as server:
        client = ExampleClient()
        result = client.map(square, range(1000))
        print(result)
        result = client.run(square, 4)
        print(result)

        # this task will succeed
        task_result = client.run_procedure(DoubleOddNumberProc(range(1, 100, 2)))
        print(task_result.is_successful, task_result.data)

        # this task will fail
        task_result = client.run_procedure(DoubleOddNumberProc(range(2, 100, 2)))
        print(task_result.is_successful, task_result.data)

from ..procedures.procedure import Procedure
from ..units.messenger import Messenger


class RunFunction(Procedure):
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self, messenger: Messenger):
        messenger.info(f"Run function `{self.function.__name__}` with args: `{self.args}` and kwargs: `{self.kwargs}`")
        self.function.__globals__["print"] = messenger.print  # inject messenger.print as print
        return self.function(*self.args, **self.kwargs)

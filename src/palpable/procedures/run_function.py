from ..procedures.procedure import Procedure
from ..units.messenger import Messenger


class RunFunction(Procedure):
    def __init__(self, function, param):
        self.function = function
        self.param = param

    def run(self, messenger: Messenger):
        messenger.info(f"Run function `{self.function.__name__}` with params: `{self.param}`")
        self.function.__globals__["print"] = messenger.print  # inject messenger.print as print
        return self.function(self.param)

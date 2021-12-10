class TaskFailed(Exception):
    pass


class TaskTimeout(Exception):
    pass


class TaskKilledByQuitSignal(Exception):
    pass


class TaskKilledByMonitoringError(Exception):
    pass

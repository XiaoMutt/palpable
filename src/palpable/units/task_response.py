import typing as tp


class _Response_(dict):
    def __init__(self, task_id: tp.Optional[str], data: object):
        super(_Response_, self).__init__(
            task_id=task_id,
            status=self.__class__.__name__,
            data=data,
        )

    def __eq__(self, other):
        if isinstance(other, _Response_):
            return self["status"] == other["status"]

        if issubclass(other, _Response_):
            return self["status"] == other.__name__

        raise Exception(f"Cannot compare with {other}")

    def __ne__(self, other):
        if isinstance(other, _Response_):
            return self["status"] != other["status"]

        if issubclass(other, _Response_):
            return self["status"] != other.__name__

        raise Exception(f"Cannot compare with {other}")


class TASK_RESPONSE(object):
    RESPONSE = _Response_

    class ERROR(_Response_):
        """
        There is an exception thrown during process of the task
        The data is the exception message
        """
        pass

    class SUCCESS(_Response_):
        """
        Processing is successful. The data is the result
        """
        pass

    class NONE(_Response_):
        """
        There are no tasks related to the request can be found
        """
        pass

    class TBD(_Response_):
        """
        The process is still running. the data is the ajax_relay url
        """
        pass

"""Contains task classes for the task queue."""


class PyTask:
    """Base class for all tasks."""

    __class__ = "PyTask"

    def __init__(self, task_function: callable, max_retries: int = 0):
        self._max_retries = max_retries
        self._task_function = task_function
        self.previous = []
        self.next = []
        self.hash = hash(self._task_function)

    def __repr__(self):
        return f"{self.__class__}({self._task_function})"

    def __hash__(self):
        return self.hash

    def __call__(self, function_args: dict = None):
        return self._task_function(**function_args)

    def __rshift__(self, other: "PyTask"):
        self.next.append(other)
        other.previous.append(self)
        return other

    def __lshift__(self, other: "PyTask"):
        raise NotImplementedError(
            "Cannot use the left shift operator on the first task in the chain."
        )

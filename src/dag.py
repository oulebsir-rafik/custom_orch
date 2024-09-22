"""Contains code for DAGs."""
import sys
from tasks import PyTask


class DAG:
    def __enter__(self):
        # Store a reference to the frame at the start of the context
        self.start_locals = sys._getframe(1).f_locals.copy()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Capture locals at the end of the context
        end_locals = sys._getframe(1).f_locals

        # Collect variables that were added inside the context
        self.dag_tasks = []
        for var in end_locals:
            if var not in self.start_locals and end_locals[var].__class__ == "PyTask":
                self.dag_tasks.append(end_locals[var])

        # Organize the tasks in the DAG
        self.organized_execution = organize_dag(self.dag_tasks)


def organize_dag(dag_tasks: list[PyTask]):
    """Organize execution of tasks in a DAG."""
    # get all end tasks
    end_tasks = [
        task for task in dag_tasks if len(task.next) == 0 and len(task.previous) != 0
    ]

    previous_tasks = end_tasks.copy()
    organized_execution = []
    organized_execution.append(previous_tasks)

    while len(previous_tasks) != 0:
        next_tasks = []
        for task in previous_tasks:
            next_tasks.extend(task.previous)
        previous_tasks = next_tasks.copy()

        if len(previous_tasks) != 0:
            organized_execution.append(previous_tasks)

    # reverse the list to get the correct order
    organized_execution.reverse()
    return organized_execution

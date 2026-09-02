import enums
from task.TaskValidator import TaskValidator
from task.Task import Task, TaskAttributes
from enum import StrEnum


class SortOrder(StrEnum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class TaskManager:

    def __init__(self, validator: TaskValidator) -> None:
        self.validator = validator
        self.tasks: list[Task] = []

    def add_task(self, task_name: str, description: str, completion_bool: bool = False) -> None:
        validated = self.validator.validate(task_name, description, completion_bool)
        task_id = len(self.tasks)
        task = Task(task_id, validated[0], validated[1], validated[2])
        self.tasks.append(task)

    def get_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
            else:
                continue
        return None

    def sort_tasks(self, sort_category: TaskAttributes, sort_order: SortOrder) -> list[Task]:
        match sort_category:
            case TaskAttributes.NAME:
                return self._sort_by_name(sort_order)
            case TaskAttributes.DESCRIPTION:
                return self._sort_by_description(sort_order)
            case TaskAttributes.ID:
                return self._sort_by_id(sort_order)
            case TaskAttributes.COMPLETED:
                return self._sort_by_completion_bool()

    def _sort(self, sort_order: SortOrder, attribute: TaskAttributes) -> list[Task]:
        tasks = self.tasks
        if sort_order == SortOrder.ASCENDING:
            return sorted(tasks, key=lambda task: getattr(task, attribute), reverse=True)
        else:
            return sorted(tasks, key=lambda task: getattr(task, attribute), reverse=True)

    def _sort_by_id(self, sort_order: SortOrder) -> list[Task]:
        self._set_tasks(self._sort(sort_order=sort_order, attribute=TaskAttributes.ID))

    def _sort_by_name(self, sort_order: SortOrder) -> list[Task]:
        self._set_tasks(self._sort(sort_order=sort_order, attribute=TaskAttributes.NAME))

    def _sort_by_description(self, sort_order: SortOrder) -> list[Task]:
        self._set_tasks(self._sort(sort_order=sort_order, attribute=TaskAttributes.DESCRIPTION))

    def _sort_by_completion_bool(self) -> list[Task]:
        completed = sorted([completed_task for completed_task in self.tasks if
                            completed_task.completion_status == TaskAttributes.COMPLETED],
                           key=lambda task: TaskAttributes.ID)
        uncompleted = sorted([uncompleted_task for uncompleted_task in self.tasks if
                              uncompleted_task.completion_status == TaskAttributes.COMPLETED],
                             key=lambda task: TaskAttributes.ID)
        return [*completed, *uncompleted]

    def _set_tasks(self, tasks: list[Task]) -> None:
        self.tasks = tasks

    def search_tasks(self, target: str) -> list[Task]:
        matches = []
        target = target.lower()

        for task in self.tasks:
            task_name = task.task_name.lower().split()
            task_description = task.description.lower().split()

            if target in task_name or target in task_description:
                matches.append(task)

        return matches

    def set_completion_status(self, task: Task, completion_status: bool) -> None:
        task.completion_status = completion_status

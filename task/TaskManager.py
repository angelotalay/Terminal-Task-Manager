from task.TaskValidator import TaskValidator
from task.Task import Task

class TaskManager:
    def __init__(self, validator: TaskValidator):
        self.validator = validator
        self.tasks: list[Task] = []

    def add_task(self, task_name: str, description:str,  completion_bool: bool = False):
        validated = self.validator.validate(task_name, description, completion_bool)
        self.tasks.append(validated)








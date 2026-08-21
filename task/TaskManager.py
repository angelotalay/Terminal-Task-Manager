from TaskValidator import TaskValidator


class TaskManager:
    def __init__(self, validator: TaskValidator):
        self.validator = validator
        self.tasks: list[dict[str, bool]] = []

    def add_task(self, task_name: str, completion_bool: bool = False):
        try:
            task = self.validator.validate(task_name, completion_bool)
            self.tasks.append(task)
        except TypeError as error:
            print(f"Could add not add task: {error}")
        except ValueError as error:
            print(f"Could add not add task: {error}")


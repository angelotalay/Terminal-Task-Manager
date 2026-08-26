from task.Task import Task

class TaskValidator:
    def validate(self, task_name, description, completion_bool) -> Task:
        if not self._task_name_is_string(task_name):
            raise TypeError("The task name must be a string")
        if not self._is_completion_bool(completion_bool):
            raise TypeError("The completion state must be a boolean")
        if not self._is_task_name_valid(task_name):
            raise ValueError("The task name must not be empty")
        if not self._task_description_is_string(description):
            raise TypeError("The task description must be a string")
        return Task(task_name, description, completion_bool)

    @staticmethod
    def _task_name_is_string(task_name):
        return isinstance(task_name, str)

    @staticmethod
    def _task_description_is_string(task_description):
        return isinstance(task_description, str)

    @staticmethod
    def _is_completion_bool(completion_state):
        return isinstance(completion_state, bool)

    @staticmethod
    def _is_task_name_valid(task_name):
        if task_name == "":
            return False
        else:
            return True

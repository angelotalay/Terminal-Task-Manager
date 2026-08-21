class Task:
    def __init__(self, task_name: str, completion_status: bool):
        self.task_name = task_name
        self.completion_status = completion_status

    def get_task_name(self):
        return self.task_name

    def get_completion_status(self):
        return self.completion_status
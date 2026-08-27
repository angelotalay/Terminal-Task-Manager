class Task:
    def __init__(self, task_id: int, task_name: str, description:str, completion_status: bool):
        self.task_id = task_id
        self.task_name = task_name
        self.description = description
        self.completion_status = completion_status

    def get_task_name(self):
        return self.task_name

    def get_completion_status(self):
        return self.completion_status
    def get_description(self):
        return self.description
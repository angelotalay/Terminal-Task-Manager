from enum import StrEnum

class TaskAttributes(StrEnum):
    ID = "task_id"
    NAME = "task_name"
    DESCRIPTION = "description"
    COMPLETED = "completion_bool"

class Task:
    def __init__(self, task_id: int, task_name: str, description:str, completion_status: bool):
        self.task_id = task_id
        self.task_name = task_name
        self.description = description
        self.completion_status = completion_status


from textual.message import Message
from task.Task import Task

class BackToMenu(Message):
    """ Return focus to  the side menu """

class EditTask(Message):
    """ Take task to the edit view """
    def __init__(self, task: Task):
        super().__init__()
        self.task = task
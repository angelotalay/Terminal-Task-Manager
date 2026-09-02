from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Label
from textual.containers import HorizontalGroup
from textual.message import Message

from task.TaskManager import TaskManager

class SearchTask(Widget):
    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Search Task")
            yield Input(id="search_input")

    class Back(Message):
        """ Message to get back to the menu """

    def action_back(self):
        self.post_message(self.Back())

    def focus_default(self) -> None:
        self.query_one("#sort_input", Input).focus()
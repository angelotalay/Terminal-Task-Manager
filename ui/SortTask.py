from textual.app import Widget, ComposeResult
from textual.containers import VerticalGroup, HorizontalGroup
from textual.widgets import Select, Label, Button
from textual.message import Message

from task.TaskManager import TaskManager


class SortTask(Widget):
    OPTIONS = [("ID", "id"), ("Task Name", "name"), ("Task Details", "details"), ("Status", "status")]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("How do you want to sort the tasks?")
            with HorizontalGroup():
                yield Select(self.OPTIONS, id="sort_select")
                yield Button("Ok", id="sort_button")

    class Sort(Message):
        """ Message class to sort the tasks """

        def __init__(self, sort_by):
            super().__init__()
            self.sort_by = sort_by

    def focus_default(self) -> None:
        self.query_one("#sort_select", Select).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if len(self.task_manager.tasks) <= 1:
            self.notify("Not enough tasks to sort.", severity="warning")
        else:
            sort_by = self.query_one("sort_select", Select).value
            if sort_by in [option[1] for option in self.OPTIONS]:
                self.post_message(self.Sort(sort_by))


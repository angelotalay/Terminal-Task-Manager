from textual.app import Widget, ComposeResult
from textual.containers import VerticalGroup, HorizontalGroup
from textual.widgets import Select, Label, Button
from textual.message import Message

from task.TaskManager import TaskManager, SortOrder
from task.Task import TaskAttributes
from task.Task import Task


class SortTask(Widget):
    OPTIONS = [
        ("ID", TaskAttributes.ID),
        ("Task Name", TaskAttributes.NAME),
        ("Task Details", TaskAttributes.DESCRIPTION),
        ("Status", TaskAttributes.COMPLETED),
    ]

    ORDER_OPTIONS = [
        ("Ascending", SortOrder.ASCENDING),
        ("Descending", SortOrder.DESCENDING),
    ]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("How do you want to sort the tasks?")
            with HorizontalGroup():
                yield Select(self.OPTIONS, id="sort_select")
                yield Select(self.ORDER_OPTIONS, id="sort_order")
                yield Button("Ok", id="sort_button")

    class Sort(Message):
        """ Message class to sort the tasks """

        def __init__(self, sort_by: TaskAttributes, sort_order: SortOrder):
            super().__init__()
            self.sort_by = sort_by
            self.sort_order = sort_order

    def focus_default(self) -> None:
        self.query_one("#sort_select", Select).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if len(self.task_manager.tasks) <= 1:
            self.notify(
                "Not enough tasks to sort.",
                severity="warning"
            )
            return

        sort_by = self.query_one("#sort_select", Select).selection
        sort_order = self.query_one("#sort_order", Select).selection

        if not isinstance(sort_by, TaskAttributes):
            self.notify(
                "Please select what to sort by.",
                severity="warning"
            )
            return

        if not isinstance(sort_order, SortOrder):
            self.notify(
                "Please select a sort order.",
                severity="warning"
            )
            return

        self.post_message(
            self.Sort(sort_by, sort_order)
        )

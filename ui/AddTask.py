from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.message import Message
from textual.widgets import Button, Footer, Label

from messages import BackToMenu
from task.TaskManager import TaskManager
from ui.TaskForm import TaskForm


class AddTask(VerticalGroup):
    BINDINGS = [("escape", "back", "Back To Menu")]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    class TaskAdded(Message):
        """Notify the parent that a task was added."""

    def compose(self) -> ComposeResult:
        yield Label("Add Task", id="add_task_title")
        yield TaskForm(
            id="add_task_form",
            submit_label="Add Task",
        )
        yield Footer()

    def action_back(self) -> None:
        self.query_one("#add_task_form", TaskForm).clear_form()
        self.post_message(BackToMenu())

    def focus_default(self) -> None:
        self.query_one("#add_task_form", TaskForm).focus_default()

    def submit_task(self) -> None:
        form = self.query_one("#add_task_form", TaskForm)

        try:
            task_name, description, complete = form.get_values()
            self.task_manager.add_task(task_name, description, complete)
        except (TypeError, ValueError) as error:
            self.notify(
                f"Unable to add task: {error}",
                severity="error",
                title="Error Adding Task",
            )
            return

        self.notify(
            "Task added successfully. Add another!",
            severity="information",
            title="Added a Task!",
        )
        form.clear_form()
        form.focus_default()
        self.post_message(self.TaskAdded())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.has_class("task_submit_button"):
            event.stop()
            self.submit_task()

        elif event.button.has_class("task_cancel_button"):
            event.stop()
            form = self.query_one("#add_task_form", TaskForm)
            form.clear_form()
            form.focus_default()

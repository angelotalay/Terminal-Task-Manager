from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.message import Message
from textual.widgets import Button, Footer, Label

from task.Task import Task
from task.TaskManager import TaskManager
from ui.TaskForm import TaskForm
from messages import BackToMenu


class EditTask(VerticalGroup):
    def __init__(self, task_manager: TaskManager, **kwargs) -> None:
        super().__init__(**kwargs)
        self.task_manager = task_manager
        self.selected_task: Task | None = None

    def compose(self) -> ComposeResult:
        yield Label("Edit Task", id="edit_task_title")
        yield TaskForm(
            id="edit_task_form",
            submit_label="Save Changes",
        )
        yield Footer()

    class TaskEdited(Message):
        """Notify the parent that a task was edited."""

    def focus_default(self) -> None:
        self.query_one("#edit_task_form", TaskForm).focus_default()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.has_class("task_submit_button"):
            event.stop()
            self.submit_task()

        elif event.button.has_class("task_cancel_button"):
            event.stop()
            form = self.query_one("#edit_task_form", TaskForm)
            form.clear_form()
            self.post_message(BackToMenu())

    def submit_task(self) -> None:
        task = self.selected_task

        if task is None:
            self.notify(
                "Please select a task to edit.",
                severity="error",
            )
            return

        form = self.query_one("#edit_task_form", TaskForm)

        try:
            task_name, description, complete = form.get_values()

            task.task_name = task_name
            task.description = description
            task.completion_status = complete
        except (TypeError, ValueError) as error:
            self.notify(
                f"Cannot save the edited task: {error}",
                severity="error",
            )
            return

        self.notify(
            "Task updated successfully.",
            severity="information",
        )
        self.post_message(self.TaskEdited())

    def load_task(self, task: Task) -> None:
        self.selected_task = task
        self.query_one("#edit_task_form", TaskForm).populate(task)

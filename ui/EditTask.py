from textual.widget import Widget
from textual.widgets import Footer, Input, TextArea, Select, Button
from textual.app import ComposeResult
from textual.message import Message

from task.TaskManager import TaskManager
from task.Task import Task
from ui.TaskForm import TaskForm


class EditTask(Widget):
    def __init__(self, task_manager: TaskManager, **kwargs) -> None:
        super().__init__(**kwargs)
        self.task_manager = task_manager
        self.selected_task : Task | None = None

    def compose(self) -> ComposeResult:
        yield TaskForm(id="edit_task_form")
        yield Footer()

    class TaskEdited(Message):
        """ Message to show the task was successfully edited"""

    def focus_default(self):
        self.query_one("#edit_task_form", Input).focus()


    def on_button_pressed(self, event: Button.Pressed):
        form = self.query_one("#edit_task_form", TaskForm)
        if event.button.id == "add-task-button":
            self.submit_task()
        elif event.button.id == "add-task-cancel-button":
            form.clear_form()

    def submit_task(self):
        task_name = self.query_one("#add-task-name-input", Input).value
        description = self.query_one("#add-task-description-input", TextArea).text
        complete = self.query_one("#add-task-complete-input", Select).value
        try:
            self.selected_task.task_name = task_name
            self.selected_task.description = description
            self.selected_task.completion_status = complete
            self.post_message(self.TaskEdited())
        except TypeError as error:
            self.notify(f"Cannot save the edited task. {error}", severity="error")

    def load_task(self, task: Task) -> None:
        self.selected_task = task
        self.query_one("#edit_task_form",TaskForm).clear_form()
        self.query_one("#add_task_name_input", Input).value = task.task_name
        self.query_one("#add_task_description", TextArea).text = task.description
        self.query_one("#add_task_complete", Select).value = task.completion_status





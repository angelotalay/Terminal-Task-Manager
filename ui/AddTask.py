from textual.widgets import Input, Label, Select, Button, TextArea, Footer
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.app import ComposeResult
from textual.message import Message

from task.TaskManager import TaskManager
from ui.TaskForm import TaskForm


class AddTask(VerticalGroup):
    BINDINGS = [("escape", "back", "Back To Menu")]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        yield Label("Add Task", id="add-task-title")
        yield TaskForm(id="task_form")
        yield Footer()

    class Back(Message):
        """ Message to return focus to the menu """

    class TaskAdded(Message):
        """Message to add a task to the task list"""

    def action_back(self):
        form = self.query_one("#task_form", TaskForm)
        form.clear_form()
        self.post_message(self.Back())

    def focus_default(self) -> None:
        self.query_one("#add_task_name_input", Input).focus()

    def submit_task(self) -> None:
        form = self.query_one("#task_form", TaskForm)
        task_name = self.query_one("#add_task_name_input", Input).value
        description = self.query_one("#add_task_description_input", TextArea).text
        complete = self.query_one("#add_task_complete_input", Select).value

        try:
            self.app.task_manager.add_task(task_name, description, complete)
            self.notify("Task Added Successfully. Add another!", severity="information", title="Added a Task!")
            self.post_message(self.TaskAdded())
            form.clear_form()
        except TypeError | ValueError as error:
            self.notify(f"Unable to add task: {error}", severity="error", title="Error Adding Task")

    def on_button_pressed(self, event: Button.Pressed):
        form = self.query_one("#task_form", TaskForm)
        if event.button.id == "add_task_button":
            self.submit_task()
        elif event.button.id == "add_task_cancel_button":
            form.clear_form()

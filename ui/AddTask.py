from textual.widgets import Input, Label, Select, Button, TextArea, Footer
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.app import ComposeResult
from textual.message import Message

from task.TaskManager import TaskManager


class AddTask(VerticalScroll):
    OPTIONS = [("Yes", True), ("No", False)]
    BINDINGS = [("escape", "back", "Back To Menu")]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager


    def compose(self) -> ComposeResult:
        yield Label("Add Task", id="add-task-title")

        with VerticalGroup(classes="form-field"):
            yield Label("Enter the task name")
            yield Input(
                placeholder="Eg: Read book.",
                id="add-task-name-input",
            )

        with VerticalGroup(classes="form-field", id="add-task-description-group"):
            yield Label("Enter the task details / description")
            yield TextArea(placeholder="Eg. Finish chapter 11.", id="add-task-description-input")

        with VerticalGroup(classes="form-field", id="add-task-complete-group"):
            yield Label("Is this task complete?")
            yield Select(
                self.OPTIONS,
                id="add-task-complete-input",
            )

        with HorizontalGroup(id="add-task-buttons"):
            yield Button("Add Task", id="add-task-button")
            yield Button("Cancel", id="add-task-cancel-button")

        yield Footer()

    class Back(Message):
        """ Message to return focus to the menu """
        ...
    class TaskAdded(Message):
        """Message to add a task to the task list"""

    def action_back(self):
        self.clear_form()
        self.post_message(self.Back())

    def focus_default(self) -> None:
        self.query_one("#add-task-name-input", Input).focus()

    def clear_form(self):
        self.query_one("#add-task-name-input", Input).clear()
        self.query_one("#add-task-description-input", TextArea).clear()
        self.query_one("#add-task-complete-input", Select).clear()

    def submit_task(self) -> None:
        task_name = self.query_one("#add-task-name-input", Input).value
        description = self.query_one("#add-task-description-input", TextArea).text
        complete = self.query_one("#add-task-complete-input", Select).value

        try:
            self.app.task_manager.add_task(task_name, description, complete)
            self.notify("Task Added Successfully. Add another!", severity="information", title="Added a Task!")
            self.post_message(self.TaskAdded())
            self.clear_form()
        except TypeError | ValueError as error:
            self.notify(f"Unable to add task: {error}", severity="error", title="Error Adding Task")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add-task-button":
            self.submit_task()
        elif event.button.id == "add-task-cancel-button":
            self.clear_form()

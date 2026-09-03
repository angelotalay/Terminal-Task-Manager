from textual.widgets import Label, TextArea, Button, Input, Select
from textual.containers import VerticalGroup, HorizontalGroup
from textual.app import ComposeResult

from task.Task import Task


class TaskForm(VerticalGroup):
    OPTIONS = [("Yes", True), ("No", False)]

    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="form-field"):
            yield Label("Enter the task name")
            yield Input(
                placeholder="Eg: Read book.",
                id="add_task_name_input",
            )
        with VerticalGroup(classes="form-field", id="add-task-description-group"):
            yield Label("Enter the task details / description")
            yield TextArea(placeholder="Eg. Finish chapter 11.", id="add_task_description_input")

        with VerticalGroup(classes="form-field", id="add-task-complete-group"):
            yield Label("Is this task complete?")
            yield Select(
                self.OPTIONS,
                id="add_task_complete_input",
            )
        with HorizontalGroup(id="add-task-buttons"):
            yield Button("Add Task", id="add_task_button")
            yield Button("Cancel", id="add_task_cancel_button")

    def clear_form(self):
        self.query_one("#add_task_name_input", Input).clear()
        self.query_one("#add_task_description_input", TextArea).clear()
        self.query_one("#add_task_complete_input", Select).clear()

    def populate(self, task: Task) -> None:
        name_input = self.query_one("#add_task_name_input", Input)
        description_input = self.query_one("#add_task_description_input", TextArea)
        select_input = self.query_one("#add_task_complete_input", Select)

        name_input.value = task.task_name
        description_input.text = task.description
        select_input.value = select_input.value

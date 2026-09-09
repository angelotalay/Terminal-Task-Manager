from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Button, Input, Label, Select, TextArea

from task.Task import Task


class TaskForm(VerticalGroup):
    OPTIONS = [("Yes", True), ("No", False)]

    def __init__(self, *, submit_label: str = "Add Task", **kwargs):
        super().__init__(**kwargs)
        self.submit_label = submit_label

    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="form_field"):
            yield Label("Enter the task name")
            yield Input(
                placeholder="Eg: Read book.",
                classes="task_name_input",
            )

        with VerticalGroup(classes="form_field task_description_group"):
            yield Label("Enter the task details / description")
            yield TextArea(
                placeholder="Eg. Finish chapter 11.",
                classes="task_description_input",
            )

        with VerticalGroup(classes="form_field task_complete_group"):
            yield Label("Is this task complete?")
            yield Select(
                self.OPTIONS,
                classes="task_complete_input",
            )

        with HorizontalGroup(classes="task_buttons"):
            yield Button(
                self.submit_label,
                classes="task_submit_button",
            )
            yield Button(
                "Cancel",
                classes="task_cancel_button",
            )

    def focus_default(self) -> None:
        self.query_one(".task_name_input", Input).focus()

    def get_values(self) -> tuple[str, str, bool]:
        task_name = self.query_one(".task_name_input", Input).value
        description = self.query_one(
            ".task_description_input", TextArea
        ).text
        complete = self.query_one(".task_complete_input", Select).value

        if not isinstance(complete, bool):
            raise ValueError("Please select whether the task is complete.")

        return task_name, description, complete

    def clear_form(self) -> None:
        self.query_one(".task_name_input", Input).clear()
        self.query_one(".task_description_input", TextArea).clear()
        self.query_one(".task_complete_input", Select).clear()

    def populate(self, task: Task) -> None:
        self.query_one(".task_name_input", Input).value = task.task_name
        self.query_one(
            ".task_description_input", TextArea
        ).text = task.description
        self.query_one(
            ".task_complete_input", Select
        ).value = task.completion_status
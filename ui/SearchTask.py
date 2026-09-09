from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Label, Footer, DataTable
from textual.containers import VerticalGroup
from textual.message import Message

from task.TaskManager import TaskManager
from constants.task import TASK_TABLE_CONFIG
from task.Task import Task
from messages import BackToMenu

# TODO: When searching for a task, the search task runs on type.
class SearchTask(Widget):
    BINDINGS = [("escape", "back", "Back To Menu")]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("Search Task")
            yield Input(id="search_input", placeholder="Search task by name or description")
            yield SearchList(id="search_list")
            yield Footer()

    class EditTask(Message):
        """ Message to go to the edit form for a particular task """
        def __init__(self, task: Task):
            super().__init__()
            self.task = task

    def action_back(self):
        self.query_one("#search_input", Input).clear()
        self.post_message(BackToMenu())

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        if not event.row_key.value:
            return

        task_id = int(event.row_key.value)
        task = self.task_manager.get_task(task_id)

        if task is not None:
            self.post_message(self.EditTask(task))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.query_one("#search_list", SearchList).focus()

    def on_input_changed(self, event: Input.Changed):
        search_target = event.value
        self.search_task(search_target)

    def focus_default(self) -> None:
        self.query_one("#search_input", Input).focus()

    def search_task(self, search_target: str):
        matched_tasks = self.task_manager.search_tasks(search_target)
        table = self.query_one(SearchList)
        if len(matched_tasks) == 0:
            return
        else:
            table.populate_table(matched_tasks)


class SearchList(DataTable):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        for column, width in zip(
                TASK_TABLE_CONFIG["columns"],
                TASK_TABLE_CONFIG["width"],
        ):
            self.add_column(column, width=width)

    def populate_table(self, tasks: list[Task]):
        self.clear()
        for task in tasks:
            task_id = task.task_id
            task_name = task.task_name
            task_description = task.description
            task_completed = task.completion_status
            self.add_row(task_id, task_name, task_description, task_completed, key=str(task_id))

from textual.app import ComposeResult
from textual.widgets import DataTable, Label, Footer
from textual.containers import VerticalGroup
from textual.message import Message

from task.TaskManager import TaskManager
from constants.task import TASK_TABLE_CONFIG
from messages import EditTask, BackToMenu


class TaskList(VerticalGroup):
    """ Widget to display a list of tasks """
    COLUMNS = ("ID", "Task", "Description", "Status")
    BINDINGS = [("escape", "back", "Back To Menu"), ("enter", "set_completion", "Mark Complete / Incomplete"),
                ("e", "edit", "Edit Task")]

    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        yield Label("Task List")
        yield DataTable(id="task_list_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        for i in range(0, len(TASK_TABLE_CONFIG["columns"])):
            table.add_column(TASK_TABLE_CONFIG["columns"][i], width=TASK_TABLE_CONFIG["width"][i])
        self.populate_table(table)

    def get_table(self) -> DataTable:
        return self.query_one("#task_list_table", DataTable)

    def focus_default(self) -> None:
        table = self.get_table()
        table.focus()

        if table.row_count > 0:
            table.move_cursor(row=0, column=0, scroll=True)

    def action_back(self):
        self.post_message(BackToMenu())

    def action_edit(self) -> None:
        table = self.get_table()

        if not table.has_focus:
            return
        if not table.is_valid_coordinate(table.cursor_coordinate):
            return

        cell_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        task_id = cell_key.row_key.value

        if task_id is None:
            return

        task = self.task_manager.get_task(int(task_id))
        if task is None:
            self.notify("The selected task cannot be found", severity="error")
        self.post_message(EditTask())

    def action_set_completion(self):
        ...

    def populate_table(self, table):
        table.clear()
        for task in self.task_manager.tasks:
            task_id = task.task_id
            task_name = task.task_name
            task_description = task.description
            task_status = "✅" if task.completion_status == True else "❌"
            table.add_row(task_id, task_name, task_description, task_status, key=str(task_id))

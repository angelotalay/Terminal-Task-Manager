from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import DataTable, Label, Footer
from textual.containers import VerticalGroup

from task.TaskManager import TaskManager


class TaskList(VerticalGroup):
    """ Widget to display a list of tasks """
    COLUMNS = ("ID", "Task", "Description", "Status")
    BINDINGS = [("q", "quit", "Quit"), ("d", "delete", "Delete"), ("c", "complete", "Mark Complete")]
    def __init__(self, task_manager: TaskManager, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = task_manager


    def compose(self) -> ComposeResult:
        yield Label("Task List")
        yield DataTable()
        yield Footer()

    def populate_table(self, table):
        for task in self.task_manager.tasks:
            task_name = task.task_name
            task_description = task.description
            task_status = task_status
            table.add_row([task_name, task_description, task_status])

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.COLUMNS)
        self.populate_table(table)







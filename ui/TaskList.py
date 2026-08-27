from textual.app import ComposeResult
from textual.widgets import DataTable, Label, Footer
from textual.containers import VerticalGroup
from textual.message import Message

from task.TaskManager import TaskManager


class TaskList(VerticalGroup):
    """ Widget to display a list of tasks """
    COLUMNS = ("ID", "Task", "Description", "Status")
    BINDINGS = [("escape", "back", "Back To Menu")]

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
        table.cell_padding = 2
        table.add_column("ID", width=6)
        table.add_column("Task", width=20)
        table.add_column("Description", width=35)
        table.add_column("Status", width=10)
        self.populate_table(table)

    class Back(Message):
        """ Message to get back to the menu """

    def action_back(self):
        self.post_message(self.Back())

    def populate_table(self, table):
        table.clear()
        for index, task in enumerate(self.task_manager.tasks):
            task_id = index + 1
            task_name = task.task_name
            task_description = task.description
            task_status = "✅" if task.completion_status == True else "❌"

            table.add_row(task_id, task_name, task_description, task_status)




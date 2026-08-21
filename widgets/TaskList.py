from textual.app import ComposeResult
from textual.widgets import DataTable, Label, Footer
from textual.containers import VerticalGroup


class TaskList(VerticalGroup):
    """ Widget to display a list of tasks """
    COLUMNS = ("ID", "Task", "Status")
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Label("Task List")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.COLUMNS)



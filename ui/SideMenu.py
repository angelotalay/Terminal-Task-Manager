from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import ListView, Label, ListItem


class SideMenu(VerticalGroup):
    """ The side menu widget that contains all options"""

    def compose(self) -> ComposeResult:
        yield Label("Menu")
        yield ListView(
            ListItem(Label("View Tasks"), id="view_tasks_option"),
            ListItem(Label("Add Task"), id="add_task_option"),
            ListItem(Label("Search Task"), id="search_tasks_option"),
            ListItem(Label("Sort Tasks"), id="sort_tasks_option"),
            ListItem(Label("Exit"), id="exit_option"),
            classes="menu-item",
        )

    def focus_menu(self) -> None:
        self.query_one(ListView).focus()

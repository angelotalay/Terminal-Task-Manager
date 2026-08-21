from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import ListView, Label, ListItem


class SideMenu(VerticalGroup):
    """ The side menu widget that contains all options"""

    def compose(self) -> ComposeResult:
        yield Label("Menu")
        yield ListView(
            ListItem(Label("Add Task"), id="add_task"),
            ListItem(Label("Mark Complete"), id="mark_complete"),
            ListItem(Label("Search Task"), id="search_task"),
            ListItem(Label("Sort Tasks"), id="sort_tasks"),
            ListItem(Label("Exit"), id="exit"),
        )

    def on_list_view_selected(self, event: ListView.Selected)->None:
        match event.item.id:
            case "exit":
                ...



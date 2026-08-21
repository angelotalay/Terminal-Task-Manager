from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from widgets.SideMenu import SideMenu
from widgets.TaskList import TaskList


class Dashboard(HorizontalGroup):
    """ The dashboard widget for the Task Manager App"""
    def compose(self) -> ComposeResult:
        yield SideMenu()
        yield TaskList()

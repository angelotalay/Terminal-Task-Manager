from textual.app import ComposeResult, Widget
from textual.containers import HorizontalGroup
from textual.widgets import ListView, ContentSwitcher

from task.TaskManager import TaskManager
from ui.SideMenu import SideMenu
from ui.TaskList import TaskList
from ui.AddTask import AddTask
from Messages import EscapeMessage

class Dashboard(Widget):
    """ The dashboard widget for the Task Manager App"""

    def __init__(self, task_manager: TaskManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_manager = task_manager

    def compose(self) -> ComposeResult:
        with HorizontalGroup(id="dashboard"):
            yield SideMenu(id="side_menu")
            with ContentSwitcher(initial="view_tasks", id="content"):
                yield TaskList(id="view_tasks", task_manager=self.task_manager)
                yield AddTask(id="add_task", task_manager=self.task_manager)


    def switch_view(self, view_id):
        switcher = self.query_one("#content", ContentSwitcher)
        switcher.current = view_id

        view = switcher.visible_content

        if view is not None and hasattr(view, "focus_default"):
            self.call_after_refresh(view.focus_default)

    def on_list_view_selected(self, event: ListView.Selected):
        selected_id = event.item.id
        match selected_id:
            case "add_task" | "view_tasks":
                self.switch_view(selected_id)
            case "exit":
                self.app.exit()

    def on_add_task_back(self, message: AddTask.Back) -> None:
        self.query_one(SideMenu).focus_menu()

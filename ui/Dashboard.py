from textual.app import ComposeResult, Widget
from textual.containers import HorizontalGroup
from textual.css.query import NoMatches
from textual.widgets import ListView, ContentSwitcher, DataTable

from task.TaskManager import TaskManager
from ui.SearchTask import SearchTask
from ui.SideMenu import SideMenu
from ui.TaskList import TaskList
from ui.AddTask import AddTask
from ui.SortTask import SortTask

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
                yield SearchTask(id="search_tasks", task_manager=self.task_manager)

    # Logic
    def switch_view(self, view_id: str, focus_default: bool = True) -> None:
        switcher = self.query_one("#content", ContentSwitcher)
        switcher.current = view_id

        if not focus_default:
            return

        view = switcher.visible_content

        if view is not None and hasattr(view, "focus_default"):
            self.call_after_refresh(view.focus_default)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected_id = event.item.id
        match selected_id:
            case "add_task_option":
                self.switch_view("add_task")
            case "view_tasks_option":
                self.switch_view("view_tasks")
            case "sort_tasks_option":
                self.switch_view("view_tasks", focus_default=False)
                try:
                    sort_task = self.query_one(SortTask)
                    sort_task.focus_default()
                except NoMatches:
                    task_list = self.query_one(TaskList)
                    task_list.mount(
                        SortTask(
                            id="sort_tasks",
                            task_manager=self.task_manager,
                        )
                    )
                    self.query_one(SortTask).focus_default()
            case "search_tasks_option":
                self.switch_view("search_tasks", focus_default=False)

            case "exit_option":
                self.app.exit()

    # Handlers
    def on_add_task_back(self, message: AddTask.Back) -> None:
        self.query_one(SideMenu).focus_menu()

    def on_add_task_task_added(self, message: AddTask.TaskAdded) -> None:
        table = self.query_one("#task_list_table", DataTable)
        self.query_one(TaskList).populate_table(table)

    def on_task_list_back(self, message: TaskList.Back) -> None:
        self.query("#sort_tasks").remove()
        self.query_one(SideMenu).focus_menu()

    def on_sort_task_sort(self, message: SortTask.Sort):
        self.task_manager.sort_tasks(message.sort_by, message.sort_order)
        table = self.query_one("#task_list_table", DataTable)
        self.query_one(TaskList).populate_table(table)
        table.focus()
    def on_search_task_back(self, message: SearchTask.Back) -> None:
        ...

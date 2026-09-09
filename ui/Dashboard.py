from textual.app import ComposeResult, Widget
from textual.containers import HorizontalGroup
from textual.css.query import NoMatches
from textual.getters import query_one
from textual.widgets import ListView, ContentSwitcher, DataTable, Input

from messages import BackToMenu
from task.TaskManager import TaskManager
from ui.EditTask import EditTask
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
                yield EditTask(id="edit_task", task_manager=self.task_manager)

    # Getters
    def get_task_list(self) -> TaskList:
        return self.query_one("#view_tasks", TaskList)

    def get_add_task(self) -> AddTask:
        return self.query_one("#add_task", AddTask)

    def get_search_task(self) -> SearchTask:
        return self.query_one("#search_tasks", SearchTask)

    def get_edit_task(self) -> EditTask:
        return self.query_one("#edit_task", EditTask)

    def get_sort_task(self) -> SortTask:
        return self.query_one("#sort_tasks", SortTask)

    def get_side_menu(self) -> SideMenu:
        return self.query_one("#side_menu", SideMenu)

    # Logic
    def switch_view(self, view_id: str, focus_default: bool = True) -> None:
        switcher = self.query_one("#content", ContentSwitcher)
        switcher.current = view_id

        if not focus_default:
            return

        view = switcher.visible_content

        if view is not None and hasattr(view, "focus_default"):
            self.call_after_refresh(view.focus_default)

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected_id = event.item.id
        match selected_id:
            case "add_task_option":
                self.switch_view("add_task")
            case "view_tasks_option":
                self.switch_view("view_tasks")
            case "sort_tasks_option":
                self.switch_view("view_tasks", focus_default=False)
                try:
                    self.get_sort_task().focus_default()
                except NoMatches:
                    await self.get_task_list().mount(SortTask(id="sort_tasks", task_manager=self.task_manager))
                    self.get_sort_task().focus_default()
            case "search_tasks_option":
                self.switch_view("search_tasks")
            case "exit_option":
                self.app.exit()

    # Handlers
    def on_add_task_task_added(self, message: AddTask.TaskAdded) -> None:
        table = self.get_task_list().query_one(DataTable)
        self.get_task_list().populate_table(table)

    async def on_back_to_menu(
            self,
            message: BackToMenu,
    ) -> None:
        try:
            sort_task = self.get_sort_task()
        except NoMatches:
            pass
        else:
            await sort_task.remove()

        self.get_side_menu().focus_menu()

    def on_edit_task(self, message: EditTask) -> None:
        selected_task = message.task
        self.get_edit_task().load_task(selected_task)
        self.switch_view("edit_task")

    def on_sort_task_sort(self, message: SortTask.Sort) -> None:
        self.task_manager.sort_tasks(message.sort_by, message.sort_order)
        table = self.get_task_list().get_table()
        self.get_task_list().populate_table(table)
        table.focus()

    def on_search_task_back(self, message: SearchTask.Back) -> None:
        self.get_side_menu().focus_menu()

    def on_edit_task_task_edited(self, message: EditTask.TaskEdited) -> None:
        self.switch_view("view_tasks")


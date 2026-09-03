from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from task.TaskValidator import TaskValidator
from ui.Dashboard import Dashboard
from task.TaskManager import TaskManager
from task.TaskValidator import TaskValidator

class TaskManagerApp(App):
    """ A Task Manager App """
    CSS_PATH = ["css/side_menu.tcss", "css/dashboard.tcss", "css/app.tcss", "css/add_task.tcss", "css/task_list.tcss", "css/search_task.tcss"]

    def __init__(self, task_manager: TaskManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = TaskValidator()
        self.task_manager = TaskManager(validator)


    def compose(self) -> ComposeResult:
        yield Header()
        yield Dashboard(task_manager=self.task_manager)



if __name__ == "__main__":
    app = TaskManagerApp(task_manager=TaskManager(validator=TaskValidator()))
    app.run()
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from widgets.Dashboard import Dashboard
class TaskManagerApp(App):
    """ A Task Manager App """
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Dashboard()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()
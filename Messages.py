from textual.message import Message

class EscapeMessage(Message):
    """ Escape key pressed message. """
    def __init__(self):
        super().__init__()
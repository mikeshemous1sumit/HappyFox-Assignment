from actions.actions import EmailActions

class DummyGmailClient:
    def __init__(self):
        self.read = False
        self.unread = False
        self.moved = False
    def mark_as_read(self, email_id: str) -> None:
        self.read = True
    def mark_as_unread(self, email_id: str) -> None:
        self.unread = True
    def move_message(self, email_id: str, label_id: str) -> None:
        self.moved = True
    def validate_label(self, label_name: str) -> str | None:
        return "INBOX" if label_name == "INBOX" else None

def test_perform_action_mark_as_read():
    client = DummyGmailClient()
    actions = EmailActions(client)
    actions.perform_action("1", {"action": "Mark as read"})
    assert client.read

def test_perform_action_mark_as_unread():
    client = DummyGmailClient()
    actions = EmailActions(client)
    actions.perform_action("1", {"action": "Mark as unread"})
    assert client.unread

def test_perform_action_move_message_valid_label():
    client = DummyGmailClient()
    actions = EmailActions(client)
    actions.perform_action("1", {"action": "Move Message", "destination": "INBOX"})
    assert client.moved

def test_perform_action_move_message_invalid_label(capfd):
    client = DummyGmailClient()
    actions = EmailActions(client)
    actions.perform_action("1", {"action": "Move Message", "destination": "NOT_A_LABEL"})
    out, _ = capfd.readouterr()
    assert "does not exist" in out
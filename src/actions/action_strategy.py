from typing import Dict
from gmail.client import GmailClient

class ActionStrategy:
    def execute(self, gmail_client: GmailClient, email_id: str, action: Dict) -> None:
        raise NotImplementedError

class MarkAsReadStrategy(ActionStrategy):
    def execute(self, gmail_client: GmailClient, email_id: str, action: Dict) -> None:
        gmail_client.mark_as_read(email_id)

class MarkAsUnreadStrategy(ActionStrategy):
    def execute(self, gmail_client: GmailClient, email_id: str, action: Dict) -> None:
        gmail_client.mark_as_unread(email_id)

class MoveMessageStrategy(ActionStrategy):
    def execute(self, gmail_client: GmailClient, email_id: str, action: Dict) -> None:
        label_name: str = action.get("destination", "")
        label_id: str | None = gmail_client.validate_label(label_name)
        if label_id:
            gmail_client.move_message(email_id, label_id)
        else:
            print(f"Warning: Label '{label_name}' does not exist. Skipping move action.")

def get_action_strategy(action_type: str) -> ActionStrategy | None:
    strategies: Dict[str, ActionStrategy] = {
        "Mark as read": MarkAsReadStrategy(),
        "Mark as unread": MarkAsUnreadStrategy(),
        "Move Message": MoveMessageStrategy(),
    }
    return strategies.get(action_type)
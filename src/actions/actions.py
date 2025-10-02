from typing import Dict
from gmail.client import GmailClient
from actions.action_strategy import get_action_strategy

class EmailActions:
    def __init__(self, gmail_client: GmailClient) -> None:
        self.gmail_client = gmail_client

    def perform_action(self, email_id: str, action: Dict) -> None:
        if isinstance(action, dict):
            action_type: str = action.get("action")
            strategy = get_action_strategy(action_type)
            if strategy:
                strategy.execute(self.gmail_client, email_id, action)
            else:
                print(f"Unknown action: {action_type}")
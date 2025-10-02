from gmail.auth import GmailAuth
from gmail.client import GmailClient
from db.database import Database
from rules.engine import RuleEngine
from utils.helpers import load_rules
from actions.actions import EmailActions
import config

def main():
    # Authenticate and get Gmail service
    auth = GmailAuth(config.GMAIL_CREDENTIALS_PATH)
    service = auth.authenticate()

    # Initialize Gmail client
    gmail_client = GmailClient(service)

    # Load emails from DB
    db = Database(config.DB_URL)
    emails = db.fetch_emails()
    db.close()

    # Load rules
    rules_data = load_rules(config.RULES_JSON_PATH)
    rules = rules_data.get('rules', [])
    rule_engine = RuleEngine(rules)

    # Process emails and get actions mapping
    actions_map = rule_engine.process_emails(emails)

    # Execute actions
    email_actions = EmailActions(gmail_client)
    for email_id, actions in actions_map.items():
        for action in actions:
            email_actions.perform_action(email_id, action)

    print("Processed emails and performed actions as per rules.")

if __name__ == "__main__":
    main()
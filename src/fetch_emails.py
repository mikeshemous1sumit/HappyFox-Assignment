from gmail.auth import GmailAuth
from gmail.client import GmailClient
from db.database import Database
import config

def main():
    # Authenticate and get Gmail service
    auth = GmailAuth(config.GMAIL_CREDENTIALS_PATH)
    service = auth.authenticate()

    # Fetch emails
    gmail_client = GmailClient(service)
    emails = gmail_client.fetch_emails()

    # Store emails in DB
    db = Database(config.DB_URL)
    for email in emails:
        db.insert_email(email)

    db.close()
    print(f"Fetched and stored {len(emails)} emails.")

if __name__ == "__main__":
    main()
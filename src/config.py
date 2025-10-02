import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_CREDENTIALS_PATH: str = os.getenv("GMAIL_CREDENTIALS_PATH", "./gmail_credentials.json")
RULES_JSON_PATH: str = os.getenv("RULES_JSON_PATH", "./rules.json")
DB_URL: str = os.getenv("DB_URL", "postgresql+psycopg2://myuser:mypassword@localhost:5432/gmail_rule_engine")
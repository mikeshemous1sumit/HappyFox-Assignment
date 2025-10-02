from typing import Dict, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Email, Base
from utils.helpers import _convert_timestamp

class Database:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_email(self, email_data: Dict) -> None:
        session = self.Session()
        email = Email(
            id=email_data.get('id'),
            from_address=email_data.get('from'),
            to_address=email_data.get('to'),
            subject=email_data.get('subject', ""),
            message=email_data.get('message', ""),
            received_date=_convert_timestamp(email_data.get('received')),
            is_read=email_data.get('is_read', False)
        )
        if not session.query(Email).filter_by(id=email.id).first():
            session.add(email)
            session.commit()
        session.close()

    def fetch_emails(self) -> List[Email]:
        session = self.Session()
        emails = session.query(Email).all()
        session.close()
        return emails

    def close(self) -> None:
        self.engine.dispose()
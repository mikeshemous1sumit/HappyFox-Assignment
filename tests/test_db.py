from db.database import Database


def test_insert_and_fetch_email():
    db = Database("sqlite:///:memory:")
    email_data = {
        'id': '123',
        'from': 'test@example.com',
        'to': 'me@example.com',
        'subject': 'Test',
        'message': 'Hello',
        'received': '1696243200000',
        'is_read': True
    }
    db.insert_email(email_data)
    emails = db.fetch_emails()
    assert len(emails) == 1
    assert emails[0].id == '123'
    db.close()
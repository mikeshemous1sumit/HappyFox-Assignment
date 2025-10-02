from gmail.client import GmailClient

class DummyService:
    def users(self):
        return self
    def labels(self):
        return self
    def list(self, userId):
        return self
    def execute(self):
        return {'labels': [{'name': 'INBOX', 'id': 'INBOX'}]}
    def messages(self):
        return self
    def get(self, userId, id):
        return self
    def fetch_emails(self, user_id='me', max_results=1):
        return [{'id': 'abc', 'payload': {'headers': [{'name': 'From', 'value': 'test@example.com'}]}, 'snippet': 'Hello', 'internalDate': '1696243200000', 'labelIds': ['INBOX']}]

def test_validate_label():
    client = GmailClient(DummyService())
    assert client.validate_label('INBOX') == 'INBOX'
    assert client.validate_label('NOT_A_LABEL') is None

def test_extract_email_data():
    client = GmailClient(DummyService())
    msg = {
        'id': 'abc',
        'payload': {'headers': [{'name': 'From', 'value': 'test@example.com'}]},
        'snippet': 'Hello',
        'internalDate': '1696243200000',
        'labelIds': ['INBOX']
    }
    email = client.extract_email_data(msg)
    assert email['id'] == 'abc'
    assert email['from'] == 'test@example.com'
    assert email['message'] == 'Hello'
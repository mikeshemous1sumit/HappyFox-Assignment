from typing import Any, Dict, List

class GmailClient:
    def __init__(self, service: Any)-> None:
        self.service = service
        self.label_map = self._fetch_labels()

    def _fetch_labels(self) -> Dict[str, str]:
        results = self.service.users().labels().list(userId='me').execute()
        return {label['name']: label['id'] for label in results.get('labels', [])}

    def validate_label(self, label_name: str) -> str | None:
        return self.label_map.get(label_name)
    
    def fetch_emails(self, user_id: str = 'me', max_results: int = 20) -> List[Dict]:
        results = self.service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            email = self.service.users().messages().get(userId=user_id, id=msg['id']).execute()
            emails.append(self.extract_email_data(email))
        return emails

    def extract_email_data(self, msg: Dict) -> Dict:
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        return {
            'id': msg['id'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'message': msg.get('snippet', ''),
            'received': msg.get('internalDate', ''),
            'is_read': 'UNREAD' not in msg.get('labelIds', [])
        }

    def mark_as_read(self, email_id: str) -> None:
        print("Marking as read in client", email_id)
        self.service.users().messages().modify(
            userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}
        ).execute()

    def mark_as_unread(self, email_id: str) -> None:
        print("Marking as unread in client", email_id)
        self.service.users().messages().modify(
            userId='me', id=email_id, body={'addLabelIds': ['UNREAD']}
        ).execute()

    def move_message(self, email_id, label: str) -> None:
        print("Moving message in client", email_id, "to label", label)
        self.service.users().messages().modify(
            userId='me', id=email_id, body={'addLabelIds': [label]}
        ).execute()
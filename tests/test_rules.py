from rules.engine import RuleEngine

class DummyEmail:
    def __init__(self):
        self.id = '1'
        self.from_address = 'apple@apple.com'
        self.subject = 'Receipt'
        self.received_date = 1696243200000

    def __getattr__(self, name):
        # Support 'from' field for RuleEngine
        if name == "from":
            return self.from_address
        raise AttributeError(name)

def test_rule_engine_all_predicate():
    rules = [{
        "conditions": [
            {"field": "From", "predicate": "Equals", "value": "apple@apple.com"},
            {"field": "Subject", "predicate": "Equals", "value": "Receipt"}
        ],
        "predicate": "All",
        "actions": [{"action": "Mark as read"}]
    }]
    engine = RuleEngine(rules)
    emails = [DummyEmail()]
    actions_map = engine.process_emails(emails)
    assert '1' in actions_map
    assert actions_map['1'][0]['action'] == "Mark as read"

def test_rule_engine_any_predicate():
    rules = [{
        "conditions": [
            {"field": "From", "predicate": "Equals", "value": "apple@apple.com"},
            {"field": "Subject", "predicate": "Equals", "value": "NotReceipt"}
        ],
        "predicate": "Any",
        "actions": [{"action": "Mark as unread"}]
    }]
    engine = RuleEngine(rules)
    emails = [DummyEmail()]
    actions_map = engine.process_emails(emails)
    assert '1' in actions_map
    assert actions_map['1'][0]['action'] == "Mark as unread"
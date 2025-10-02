from typing import Any, Dict, List
from rules.predicate_strategy import get_strategy

class RuleEngine:
    field_map = {
        "From": "from_address",
        "To": "to_address",
        "Subject": "subject",
        "Message": "message",
        "Received": "received_date",
        "Received Date/Time": "received",
    }
    def __init__(self, rules: List[Dict]) -> None:
        self.rules = rules

    def process_emails(self, emails: List[Any]) -> Dict[str, List[Dict]]:
        actions_map: Dict[str, List[Dict]] = {}
        for email in emails:
            matched_actions: List[Dict] = []
            for rule in self.rules:
                if self.evaluate_rule(rule, email):
                    matched_actions.extend(rule.get('actions', []))
            if matched_actions:
                actions_map[email.id] = matched_actions
        return actions_map

    def evaluate_rule(self, rule: Dict, email: Any) -> bool:
        conditions = rule.get('conditions', [])
        predicate = rule.get('predicate', 'All')
        results = [self.evaluate_condition(cond, email) for cond in conditions]
        if predicate == 'All':
            return all(results)
        elif predicate == 'Any':
            return any(results)
        return False

    def evaluate_condition(self, condition: Dict, email: Any) -> bool:
        field = condition['field']
        predicate = condition['predicate']
        value = condition['value']
        attr_name = self.field_map.get(field, field.lower())
        field_value = getattr(email, attr_name, "")
        strategy = get_strategy(predicate)
        if strategy:
            return strategy.evaluate(field_value, value)
        return False
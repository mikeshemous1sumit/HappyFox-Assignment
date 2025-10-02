class Rule:
    def __init__(self, field_name, predicate, value):
        self.field_name = field_name
        self.predicate = predicate
        self.value = value

class RuleSet:
    def __init__(self, rules, overall_predicate):
        self.rules = rules
        self.overall_predicate = overall_predicate

    def evaluate(self, email):
        if self.overall_predicate == "All":
            return all(self.evaluate_rule(rule, email) for rule in self.rules)
        elif self.overall_predicate == "Any":
            return any(self.evaluate_rule(rule, email) for rule in self.rules)
        return False

    def evaluate_rule(self, rule, email):
        field_value = getattr(email, rule.field_name, None)
        if rule.predicate == "Contains":
            return rule.value in field_value
        elif rule.predicate == "Does not contain":
            return rule.value not in field_value
        elif rule.predicate == "Equals":
            return field_value == rule.value
        elif rule.predicate == "Does not equal":
            return field_value != rule.value
        elif rule.field_name == "Received Date/Time":
            return self.evaluate_date_rule(rule, field_value)
        return False

    def evaluate_date_rule(self, rule, field_value):
        # Assuming field_value is a datetime object
        if rule.predicate == "Less than":
            return field_value < rule.value
        elif rule.predicate == "Greater than":
            return field_value > rule.value
        return False
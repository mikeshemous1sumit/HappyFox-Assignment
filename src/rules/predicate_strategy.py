from datetime import datetime

class PredicateStrategy:
    def to_datetime(self, value):
        if isinstance(value, datetime):
            return value
        try:
            # Try converting from milliseconds timestamp
            return datetime.fromtimestamp(int(value) / 1000)
        except Exception:
            return None

    def evaluate(self, field_value, condition_value) -> bool:
        raise NotImplementedError

class ContainsStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        return condition_value in field_value

class DoesNotContainStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        return condition_value not in field_value

class EqualsStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        # For dates, compare as timestamps
        fv = self.to_datetime(field_value)
        cv = self.to_datetime(condition_value)
        if fv and cv:
            return int(fv.timestamp()) == int(cv.timestamp())
        return field_value == condition_value

class DoesNotEqualStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        fv = self.to_datetime(field_value)
        cv = self.to_datetime(condition_value)
        if fv and cv:
            return int(fv.timestamp()) != int(cv.timestamp())
        return field_value != condition_value

class LessThanDaysStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        email_date = self.to_datetime(field_value)
        if not email_date:
            return False
        days = int(condition_value)
        return (datetime.now() - email_date).days < days

class GreaterThanDaysStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        email_date = self.to_datetime(field_value)
        if not email_date:
            return False
        days = int(condition_value)
        return (datetime.now() - email_date).days > days

class LessThanMonthsStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        email_date = self.to_datetime(field_value)
        if not email_date:
            return False
        months = int(condition_value)
        delta_months = (datetime.now().year - email_date.year) * 12 + (datetime.now().month - email_date.month)
        return delta_months < months

class GreaterThanMonthsStrategy(PredicateStrategy):
    def evaluate(self, field_value, condition_value) -> bool:
        email_date = self.to_datetime(field_value)
        if not email_date:
            return False
        months = int(condition_value)
        delta_months = (datetime.now().year - email_date.year) * 12 + (datetime.now().month - email_date.month)
        return delta_months > months

def get_strategy(predicate, field=None, unit=None) -> PredicateStrategy | None:
    strategies = {
        "Contains": ContainsStrategy(),
        "Does not Contain": DoesNotContainStrategy(),
        "Equals": EqualsStrategy(),
        "Does not equal": DoesNotEqualStrategy(),
        "Less than days": LessThanDaysStrategy(),
        "Greater than days": GreaterThanDaysStrategy(),
        "Less than months": LessThanMonthsStrategy(),
        "Greater than months": GreaterThanMonthsStrategy(),
    }
    return strategies.get(predicate)
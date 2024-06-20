# services.py (or any other suitable file)
from rules_management.models import Rule 

class RuleEvaluator:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.rules = Rule.objects.all().order_by('sequence_id')

    def evaluate(self):
        for rule in self.rules:
            if self._matches(rule):
                print(f"Match found: {rule}")
                return rule.department_id
        print("No matching rule found.")
        return None

    def _matches(self, rule):
        comparator = {
            'lt': lambda a, b: a < b,
            'lte': lambda a, b: a <= b,
            'gt': lambda a, b: a > b,
            'gte': lambda a, b: a >= b,
            'eq': lambda a, b: a == b,
        }.get(rule.condition)

        if not comparator:
            print(f"Invalid condition: {rule.condition}")
            return False

        if rule.rule_type == 'weight':
            return comparator(self.weight, rule.value)
        elif rule.rule_type == 'value':
            return comparator(self.value, rule.value)
        else:
            print(f"Invalid rule type: {rule.rule_type}")
            return False

def get_department(weight, value):
    evaluator = RuleEvaluator(weight, value)
    return evaluator.evaluate()

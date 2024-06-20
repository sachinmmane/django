# models.py
from django.db import models
from departments.models import Department

class Rule(models.Model):
    RULE_TYPES = [
        ('weight', 'Weight'),
        ('value', 'Value'),
        # Add other rule types if needed
    ]

    CONDITIONS = [
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal To'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal To'),
        ('eq', 'Equal To'),
    ]

    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    condition = models.CharField(max_length=4, choices=CONDITIONS)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    sequence_id = models.PositiveIntegerField()

    class Meta:
        ordering = ['sequence_id']

    def __str__(self):
        return f"{self.rule_type} {self.condition} {self.value} -> {self.department}"

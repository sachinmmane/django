from django.db import models
from departments.models import Department
from django.contrib.auth.models import User


# Create your models here.
class UserDepartment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_department')
    department_id = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_user')

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
class Department(models.Model):
    # Define  a name field for the Department model as a CharField with a maximum length of 255 characters
    name = models.CharField(max_length=255)
    description = models.TextField(default='')

    def __str__(self):
        # Define the string representation of the Department model to return the name of the department
        return self.name

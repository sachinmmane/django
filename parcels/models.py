from django.db import models
from departments.models import Department 

# Create your models here.
class Container(models.Model):
    container_id = models.CharField(max_length=255)
    shipping_date = models.DateTimeField()
    file = models.BinaryField()

    def __str__(self):
        return self.container_id

class Address(models.Model):
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.house_number} {self.street}, {self.city}"

class Receipient(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Parcel(models.Model):
    receipient = models.ForeignKey(Receipient, on_delete=models.PROTECT, related_name='parcels')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='parcels')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='parcel_status')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='parcel_department')
    container = models.ForeignKey(Container, on_delete=models.PROTECT, related_name='parcels')
    weight = models.FloatField()
    value = models.FloatField()

    def __str__(self):
        return f"Parcel for {self.receipient.name} in {self.container.container_id}"
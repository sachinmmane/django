from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model to be used for serialization
        model = Department
        # Define the fields to be included in the serialization
        fields = ["id", "name", "description"]
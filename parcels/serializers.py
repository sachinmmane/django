from rest_framework import serializers
from .models import Container, Address, Receipient, Parcel, Status
from departments.serializers import DepartmentSerializer 


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['container_id', 'shipping_date']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'house_number', 'postal_code', 'city']

class ReceipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipient
        fields = ['name', 'address']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']

class ParcelSerializer(serializers.ModelSerializer):
    receipient = ReceipientSerializer()
    address = AddressSerializer()
    container = ContainerSerializer()
    status = StatusSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = Parcel
        fields = ['id', 'receipient', 'address', 'weight', 'value', 'container', 'department', 'status']

    def update(self, instance, validated_data):
        status_data = validated_data.pop('status', None)
        if status_data:
            status_instance = Status.objects.get(id=status_data['id'])
            instance.status = status_instance
        instance.save()
        return instance
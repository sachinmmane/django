from django.contrib.auth.models import User, Group 
from rest_framework import serializers
from .models import UserDepartment, Department 
from departments.serializers import DepartmentSerializer

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        
    def to_internal_value(self, data):
        if isinstance(data, int):
            try:
                return Group.objects.get(id=data)
            except Group.DoesNotExist:
                raise serializers.ValidationError("Invalid group ID")
        elif isinstance(data, dict):
            return super().to_internal_value(data)
        else:
            raise serializers.ValidationError("Invalid data type for group")

class UserDepartmentSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department_id.name', read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True)
    department = serializers.SerializerMethodField()
    
    class Meta:
        model = UserDepartment
        fields = ['department_id', 'department_name', 'department']
    
    def get_department(self, obj):
        return {
            'department_name': obj.department_id.name,
            'department_id': obj.department_id.id
        }

class UserSerializer(serializers.ModelSerializer):
    user_department = UserDepartmentSerializer(many=True, required=False)
    groups = GroupSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password", "is_active",
            "first_name", "last_name", "user_permissions", "groups", "user_department"
        ]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
            "is_active": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "groups": {"required": True},
            "user_department": {"required": False}
        }

    def create(self, validated_data):
        user_permissions = validated_data.pop('user_permissions', [])
        departments_data = validated_data.pop('user_department', [])
        groups = validated_data.pop('groups', [])
        user = User.objects.create_user(**validated_data)
        user.user_permissions.set(user_permissions)
        user.groups.set(groups)

        for department_data in departments_data:
            UserDepartment.objects.create(user_id=user, department_id=department_data['department_id'])

        return user


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_department'] = [
            {
                'department_name': user_dept.department_id.name,
                'department_id': user_dept.department_id.id
            }
            for user_dept in instance.user_department.all()
        ]
        return representation
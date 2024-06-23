from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group, Permission
from departments.models import Department
from .models import UserDepartment

class GetUserDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Created a group
        self.group = Group.objects.create(name='Test Group')
        
        # Created permissions
        permission = Permission.objects.get(codename='view_user')
        self.group.permissions.add(permission)
        
        # Created a department
        self.department = Department.objects.create(name='Test Department')
        
        # Created a user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword', 
            email='testuser@example.com',
            first_name='Test', 
            last_name='User', 
            is_active=True
        )
        
        # Added user to group and set permissions
        self.user.groups.add(self.group)
        self.user.user_permissions.add(permission)
        
        # Created a user department
        self.user_department = UserDepartment.objects.create(user_id=self.user, department_id=self.department)
        
        # Authenticated the user
        self.client.force_authenticate(user=self.user)
        
        # URL for the user detail view
        self.url = reverse('get-user-detail', kwargs={'pk': self.user.pk}) 

    def test_get_user_detail(self):
        response = self.client.get(self.url)

        # Print the response content to diagnose the issue if it fails
        print(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['is_active'], self.user.is_active)
        self.assertEqual(len(response.data['groups']), 1)
        self.assertEqual(response.data['groups'][0]['name'], self.group.name)
        self.assertEqual(len(response.data['user_department']), 1)
        self.assertEqual(response.data['user_department'][0]['department_name'], self.department.name)

if __name__ == "__main__":
    import unittest
    unittest.main()

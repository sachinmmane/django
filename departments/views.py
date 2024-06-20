from django.shortcuts import render
from rest_framework import generics
from .serializers import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Department
# Create your views here.
class DepartmentListCreate(generics.ListCreateAPIView):
    # Specify the serializer class to be used
    serializer_class = DepartmentSerializer

    # Set the permission class to ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Define the queryset to be all Department objects
        return Department.objects.all()
    
    # Custom method to handle the creation of a new Department instance
    def perform_create(self, serializer):
      # If the serializer is valid, save the new instance else print the errors
        if serializer.is_valid():
            serializer.save()
        else:
            print (serializer.error)

class DepartmentUpdate(generics.UpdateAPIView):
    # Specify the serializer class to be used
    serializer_class = DepartmentSerializer
    # Set the permission class to ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Define the queryset to be all Department objects
        return Department.objects.all()

class DepartmentDelete(generics.DestroyAPIView):
    # Specify the serializer class to be used
    serializer_class = DepartmentSerializer
    # Set the permission class to ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Define the queryset to be all Department objects
        return Department.objects.all()


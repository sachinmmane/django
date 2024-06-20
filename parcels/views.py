from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Container, Address, Receipient, Parcel, Status
from user.models import UserDepartment
from departments.models import Department 
import xml.etree.ElementTree as ET
from .serializers import StatusSerializer, ParcelSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
from .rule_engine import get_department

class CheckContainerView(APIView):
    def get(self, request, container_id, format=None):
        exists = Container.objects.filter(container_id=container_id).exists()
        return Response({"exists": exists}, status=status.HTTP_200_OK)

class UploadFileView(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']
        xml_content = file.read()
        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()

        container_id = root.find('Id').text
        shipping_date = root.find('ShippingDate').text
        container = Container(container_id=container_id, shipping_date=shipping_date, file=xml_content)
        container.save()

        parcel_count = 0

        for parcel in root.find('parcels'):
            parcel_count += 1
            recipient = parcel.find('Receipient')
            name = recipient.find('Name').text

            address = recipient.find('Address')
            street = address.find('Street').text
            house_number = address.find('HouseNumber').text
            postal_code = address.find('PostalCode').text
            city = address.find('City').text

            address_obj, created = Address.objects.get_or_create(
                street=street,
                house_number=house_number,
                postal_code=postal_code,
                city=city
            )
            
            receipient_obj = Receipient(name=name, address=address_obj)
            receipient_obj.save()

            weight = float(parcel.find('Weight').text)
            value = float(parcel.find('Value').text)

            # Determine department based on weight and value
            department_id = get_department(weight, value)

            if department_id == 4:
               status_id =  2
            else:
               status_id = 4     
                
            department = Department.objects.filter(id=department_id).first()
            if not department:
                return Response({"error": f"Department with id {department_id} does not exist"},status=status.HTTP_400_BAD_REQUEST)

            status_instance = Status.objects.filter(id=status_id).first()
            if not status_instance:
                return Response({"error": "Status with id 1 does not exist"}, status=status.HTTP_400_BAD_REQUEST)  
            
            Parcel.objects.create(
                receipient=receipient_obj,
                address=address_obj,
                weight=weight,
                value=value,
                container=container,
                department=department,
                status=status_instance  # Make sure this ID exists in the Status table
            )

        return Response({"message": "File processed and saved successfully!", "parcel_count": parcel_count}, status=status.HTTP_201_CREATED)

class ParcelListView(generics.ListAPIView):
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        if "Department Employee" in user_groups:
            user_department = UserDepartment.objects.filter(user_id = user.id).first()
            if user_department:
                return Parcel.objects.filter(department_id=user_department.department_id.id)
        return Parcel.objects.all()

class StatusListCreate(generics .ListCreateAPIView):
    # Specify the serializer class to be used
    serializer_class = StatusSerializer

    # Set the permission class to ensure only authenticated users can access this view
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Define the queryset to be all Department objects
        return Status.objects.all()
    
    # Custom method to handle the creation of a new Department instance
    def perform_create(self, serializer):
      # If the serializer is valid, save the new instance else print the errors
        if serializer.is_valid():
            serializer.save()
        else:
            print (serializer.error)

class StatusUpdate(generics.UpdateAPIView):
    # Specify the serializer class to be used
    serializer_class = StatusSerializer
    # Set the permission class to ensure only authenticated users can access this view
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Define the queryset to be all Department objects
        return Status.objects.all()

class StatusDelete(generics.DestroyAPIView):
    # Specify the serializer class to be used
    serializer_class = StatusSerializer
    # Set the permission class to ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Define the queryset to be all Department objects
        return Status.objects.all()

class ParcelStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        try:
            parcel = Parcel.objects.get(pk=pk)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcel not found"}, status=status.HTTP_404_NOT_FOUND)

        status_id = request.data.get('status_id')
        if not status_id:
            return Response({"error": "Status ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_instance = Status.objects.get(pk=status_id)
        except Status.DoesNotExist:
            return Response({"error": "Status not found"}, status=status.HTTP_404_NOT_FOUND)

        parcel.status = status_instance
        parcel.save()

        return Response({"message": "Parcel status updated successfully"}, status=status.HTTP_200_OK)

class ParcelDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            parcel = Parcel.objects.get(pk=pk)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcel not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParcelSerializer(parcel)
        return Response(serializer.data, status=status.HTTP_200_OK)
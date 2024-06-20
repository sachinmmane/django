from django.urls import path
from . import views

urlpatterns = [
   path('departments/', views.DepartmentListCreate.as_view(), name='department-list'),
   path('departments/<int:pk>/', views.DepartmentUpdate.as_view(), name='department-update'),
    path('departments/delete/<int:pk>', views.DepartmentDelete.as_view(), name='delete-department'),
]      




    
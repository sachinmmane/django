from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('user.urls')),
    path('api/', include('parcels.urls')),
    path('api/', include('departments.urls')),
    path('api/', include('rules_management.urls')),

]

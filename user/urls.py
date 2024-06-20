from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user/register/', views.CreateUserView.as_view(), name='register'),
    path('user/<int:pk>/', views.GetUserDetailView.as_view(), name='get-user-detail'),
    path('users/', views.ListUserView.as_view(), name='list-users'),
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('user-groups/', views.GroupView.as_view(), name='user-groups'),
    path('user/me/', views.UserDetailView.as_view(), name='user_detail'),
]   
from django.urls import path, include
from .views import CreateRuleView, GetRuleDetailView, ListRulesView, DeleteRuleView, UpdateRuleView, UpdateRuleSequenceView

urlpatterns = [
    path('rules/create/', CreateRuleView.as_view(), name='create-rule'),
    path('rules/<int:pk>/', GetRuleDetailView.as_view(), name='get-rule-detail'),
    path('rules/', ListRulesView.as_view(), name='list-rules'),
    path('rules/delete/<int:pk>/', DeleteRuleView.as_view(), name='delete-rule'),
    path('rules/update/<int:pk>/', UpdateRuleView.as_view(), name='update-rule'),
    path('rules/update-sequence/', UpdateRuleSequenceView.as_view(), name='update-rule-sequence'),
]

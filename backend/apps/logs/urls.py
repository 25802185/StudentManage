from django.urls import path
from .views import OperationLogListView

urlpatterns = [
    path('', OperationLogListView.as_view()),
]

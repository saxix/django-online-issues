from django.urls import path

from .views import IssueAPIView

app_name = "issues"

urlpatterns = [
    path("api/issue/", IssueAPIView.as_view(), name="create"),
]

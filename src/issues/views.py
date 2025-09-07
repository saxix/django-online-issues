import json
from typing import TYPE_CHECKING, Any

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from .backends import get_backend
from .forms import IssueForm

if TYPE_CHECKING:
    from .types import AuthenticatedHttpRequest


class IssueAPIView(View):
    def get(self, request: "AuthenticatedHttpRequest", *args: Any, **kwargs: Any) -> HttpResponse:
        form = IssueForm()
        return render(request, "issues/issue_form.html", {"form": form})

    def post(self, request: "AuthenticatedHttpRequest", *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "Invalid JSON payload."}, status=400)

        form = IssueForm(data)
        if form.is_valid():
            backend = get_backend(request)
            backend.create_ticket(form.cleaned_data)  # type: ignore[arg-type]
            return JsonResponse({"success": True, "message": "Ticket created successfully!"})
        return JsonResponse({"success": False, "errors": form.errors, "message": "Please correct the errors below."})

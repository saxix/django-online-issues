import json
import logging
from typing import Any, cast

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from .backends import get_backend
from .forms import IssueForm, IssueFormCleanedData

logger = logging.getLogger(__name__)


class IssueAPIView(View):
    def get(self, request: "HttpRequest", *args: Any, **kwargs: Any) -> HttpResponse:
        backend = get_backend(request)
        form = IssueForm(backend=backend)
        return render(request, "issues/issue_form.html", {"form": form})

    def post(self, request: "HttpRequest", *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "errors": "Invalid JSON payload."}, status=400)

        backend = get_backend(request)
        form = IssueForm(data, backend=backend)
        if form.is_valid():
            try:
                cleaned_data = cast("IssueFormCleanedData", form.cleaned_data)
                backend.create_ticket(cleaned_data)
            except Exception as e:
                logger.exception(e)
                return JsonResponse({"success": False, "error": "Unexpected error."}, status=400)
            return JsonResponse({"success": True, "message": "Ticket created successfully!"})
        return JsonResponse({"success": False, "errors": form.errors, "message": "Please correct the errors below."})

from collections.abc import Iterable
from typing import Any

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import CheckMessage, Error, register
from django.utils.module_loading import import_string

from .backends._base import BaseBackend


@register("issues")
def check_issues_settings(app_configs: Iterable[AppConfig] | None, **kwargs: Any) -> list[CheckMessage]:
    errors: list[CheckMessage] = []
    override_issues_settings = getattr(settings, "ISSUES", {})

    if override_issues_settings:
        if not isinstance(override_issues_settings, dict):
            errors.append(
                Error(
                    "'ISSUES' setting must be a dictionary.",
                    id="issues.E001",
                )
            )
            return errors  # Stop here if ISSUES is not a dict

        # Check BACKEND
        backend_path = override_issues_settings.get("BACKEND", "")
        try:
            backend_class = import_string(backend_path)
            if not issubclass(backend_class, BaseBackend):
                errors.append(
                    Error(
                        f"'{backend_path}' must be a subclass of 'issues.backends._base.BaseBackend'.",
                        id="issues.E003",
                    )
                )
        except ImportError:
            errors.append(
                Error(
                    f"Could not import backend '{backend_path}'.",
                    id="issues.E004",
                )
            )

        # Check RENDERER
        renderer = override_issues_settings.get("RENDERER")
        allowed_renderers = ["html2canvas", "dom-to-image"]
        if renderer is not None and renderer not in allowed_renderers:
            errors.append(
                Error(
                    f"'{renderer}' is not a valid renderer. Must be one of {allowed_renderers} or None.",
                    id="issues.E005",
                )
            )

        # Check OPTIONS
        if "OPTIONS" in override_issues_settings and not isinstance(override_issues_settings["OPTIONS"], dict):
            errors.append(
                Error(
                    "'OPTIONS' in 'ISSUES' setting must be a dictionary.",
                    id="issues.E006",
                )
            )

    return errors

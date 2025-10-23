from collections import ChainMap
from typing import Any

from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.http import HttpRequest
from django.templatetags.static import static
from django.utils.module_loading import import_string

ISSUE_TEMPLATE = """
- User: {user}
- Url: {url}
- Version: {version}
- UserAgent: {user_agent}
- Remote IP: {remote_ip}

---
{description}

{screenshot_url}
"""
ALLOWED_RENDERERS = ["html2canvas", "dom-to-image", "html2canvas-pro"]


class IssuesConfig:
    _ANNOTATIONS: dict[str, str] = {
        "get_client_ip": "issues.utils.get_client_ip",
        "get_extra_info": "issues.utils.get_extra_info",
        "get_labels": "issues.utils.get_labels",
        "get_user": "issues.utils.get_user",
        "get_user_agent": "issues.utils.get_user_agent",
        "get_version": "issues.utils.get_version",
    }
    _DEFAULTS = {
        "BACKEND": "issues.backends.console.Backend",
        "RENDERER": "html2canvas",  # or  dom-to-image
        "ISSUE_TEMPLATE": ISSUE_TEMPLATE,
        "TYPES": ("bug", "enhancement", "feature", "suggestion"),
        "OPTIONS": {},
    }

    def __init__(self) -> None:
        self._overrides = getattr(settings, "ISSUES", {})
        ann = {"ANNOTATIONS": ChainMap(self._overrides.get("ANNOTATIONS", {}), self._ANNOTATIONS)}
        self._parsed = ChainMap(ann, self._overrides, self._DEFAULTS)
        self._cached: dict[str, Any] = {}

    def __repr__(self) -> str:
        return str(self._parsed)

    def get_renderer_script(self, suffix: str = "") -> str:
        raw_value: str | tuple[str, str] = self._parsed["RENDERER"]
        if isinstance(raw_value, str):
            return static(f"issues/{raw_value}{suffix}.js")
        if isinstance(raw_value, tuple):
            return raw_value[1]
        return ""

    def _clean_renderer(self) -> str:
        raw_value: str | tuple[str, str] = self._parsed["RENDERER"]
        if isinstance(raw_value, str | None):
            return raw_value or ""
        if isinstance(raw_value, tuple):
            return raw_value[0]
        raise ValueError(f"Unsupported type {type(raw_value)}")

    def load_annotations(self) -> None:
        self._cached["ANNOTATIONS"] = {}
        for k, v in self._parsed["ANNOTATIONS"].items():
            if k not in self._ANNOTATIONS:
                raise AttributeError(f"Misspelled or unknown annotation '{k}'")
            if isinstance(v, str) and v:
                self._cached["ANNOTATIONS"][k] = import_string(v)
            elif callable(v):
                self._cached["ANNOTATIONS"][k] = v
            else:
                raise AttributeError(f" 'IssuesConfig' object has no annotation '{k}'")

    def get_annotation(self, name: str, request: HttpRequest) -> Any:
        self.load_annotations()
        return self._cached["ANNOTATIONS"].get(name)(request)

    def __getattr__(self, name: str) -> Any:
        if name not in self._parsed:
            raise AttributeError(f" 'IssuesConfig' object has no attribute '{name}'")
        if name not in self._cached:
            if name == "RENDERER":
                self._cached[name] = self._clean_renderer()
            elif name == "BACKEND":
                self._cached[name] = import_string(self._parsed["BACKEND"])
            elif name == "ANNOTATIONS":
                self.load_annotations()
            else:
                self._cached[name] = self._parsed[name]
        return self._cached[name]


CONFIG = IssuesConfig()


@receiver(setting_changed)
def reload_issues_config(sender: Any, setting: str, **kwargs: Any) -> None:
    global CONFIG  # noqa: PLW0603
    if setting == "ISSUES":
        CONFIG = IssuesConfig()

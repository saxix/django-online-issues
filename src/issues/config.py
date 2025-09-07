from collections import ChainMap
from typing import Any

from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver
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
        "RENDERER": "html2canvas",  # or rasterizeHTML or dom-to-image
        "ISSUE_TEMPLATE": ISSUE_TEMPLATE,
        "OPTIONS": {},
    }

    def __init__(self) -> None:
        self._overrides = getattr(settings, "ISSUES", {})
        ann = {"ANNOTATIONS": ChainMap(self._overrides.get("ANNOTATIONS", {}), self._ANNOTATIONS)}
        self._parsed = ChainMap(ann, self._overrides, self._DEFAULTS)
        self._cached: dict[str, Any] = {}

    def __repr__(self) -> str:
        return str(self._parsed)

    def __getattr__(self, name: str) -> Any:
        if name not in self._parsed:
            raise AttributeError(f" 'IssuesConfig' object has no attribute '{name}'")
        if name not in self._cached:
            if name == "BACKEND":
                self._cached[name] = import_string(settings.ISSUES["BACKEND"])
            elif name == "ANNOTATIONS":
                self._cached["ANNOTATIONS"] = {}
                for k, v in self._parsed["ANNOTATIONS"].items():
                    if k not in self._ANNOTATIONS:
                        raise AttributeError(f" 'IssuesConfig' object has no annotation '{k}'")
                    if isinstance(v, str) and v:
                        self._cached["ANNOTATIONS"][k] = import_string(v)
                    elif callable(v):
                        self._cached["ANNOTATIONS"][k] = v
                    else:
                        raise AttributeError(f" 'IssuesConfig' object has no annotation '{k}'")
            else:
                self._cached[name] = self._parsed[name]
        return self._cached[name]


CONFIG = IssuesConfig()


@receiver(setting_changed)
def reload_issues_config(sender: Any, setting: str, **kwargs: Any) -> None:
    global CONFIG  # noqa: PLW0603
    if setting == "ISSUES":
        CONFIG = IssuesConfig()

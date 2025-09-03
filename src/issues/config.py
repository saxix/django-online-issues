from copy import deepcopy
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

{screenshot}
"""


class IssuesConfig:
    DEFAULTS = {
        "BACKEND": "issues.backends.console.Backend",
        "RENDERER": "html2canvas",  # or rasterizeHTML or dom-to-image
        "ISSUE_TEMPLATE": ISSUE_TEMPLATE,
        "OPTIONS": {},
        "ANNOTATIONS": {
            "get_extra_info": "issues.utils.get_extra_info",
            "get_version": "issues.utils.get_version",
            "get_user_agent": "issues.utils.get_user_agent",
            "get_labels": "issues.utils.get_labels",
        },
    }

    def __init__(self) -> None:
        self._overrides = getattr(settings, "ISSUES", {})
        self._parsed = {
            **deepcopy(self.DEFAULTS),
            **deepcopy(self._overrides),
        }
        self._parsed["BACKEND"] = import_string(self._parsed["BACKEND"])
        for k, v in self._parsed["ANNOTATIONS"].items():
            if isinstance(v, str):
                self._parsed["ANNOTATIONS"][k] = import_string(v)

    def __repr__(self) -> str:
        return str(self._parsed)

    def __getattr__(self, name: str) -> Any:
        if name in self._parsed:
            return self._parsed[name]
        raise AttributeError(f" 'IssuesConfig' object has no attribute '{name}'")


CONFIG = IssuesConfig()


@receiver(setting_changed)
def reload_issues_config(sender: Any, setting: str, **kwargs: Any) -> None:
    global CONFIG  # noqa: PLW0603
    if setting == "ISSUES":
        CONFIG = IssuesConfig()

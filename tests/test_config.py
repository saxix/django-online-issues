from copy import deepcopy
from unittest.mock import patch

import pytest
from django.conf import settings
from django.test import override_settings

from issues.config import IssuesConfig, reload_issues_config
from issues.utils import get_client_ip, get_extra_info, get_labels, get_user_agent, get_version


def test_issues_config_defaults():
    config = IssuesConfig()
    assert "User: {user}" in config.ISSUE_TEMPLATE
    assert config.OPTIONS == {}
    assert config.ANNOTATIONS["get_extra_info"] == get_extra_info
    assert config.ANNOTATIONS["get_version"] == get_version
    assert config.ANNOTATIONS["get_user_agent"] == get_user_agent
    assert config.ANNOTATIONS["get_labels"] == get_labels


@override_settings(
    ISSUES={
        "BACKEND": "issues.backends.debug.Backend",
        "ISSUE_TEMPLATE": "Custom template: {description}",
        "OPTIONS": {"KEY": "VALUE"},
        "ANNOTATIONS": {"get_extra_info": "issues.utils.get_client_ip"},
    }
)
def test_issues_config_overrides():
    config = IssuesConfig()
    assert config.ISSUE_TEMPLATE == "Custom template: {description}"
    assert config.OPTIONS == {"KEY": "VALUE"}
    assert config.ANNOTATIONS["get_extra_info"] == get_client_ip


def test_issues_config_getattr():
    config = IssuesConfig()
    with pytest.raises(AttributeError):
        assert config.NON_EXISTENT_ATTRIBUTE


@patch("issues.config.IssuesConfig")
def test_reload_issues_config(mock_config):
    # Simulate a setting change
    with override_settings(ISSUES=deepcopy(settings.ISSUES)):
        reload_issues_config(sender=None, setting="ISSUES")
        # Assert that IssuesConfig was re-instantiated
        mock_config.assert_called()


def test_issues_config_repr():
    config = IssuesConfig()
    assert isinstance(str(config), str)
    assert "BACKEND" in str(config)

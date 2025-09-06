from contextlib import nullcontext as does_not_raise

import pytest
from django.conf import settings

from issues.config import IssuesConfig
from issues.utils import get_client_ip, get_extra_info, get_labels, get_user_agent, get_version


def test_issues_config_defaults():
    config = IssuesConfig()
    assert "User: {user}" in config.ISSUE_TEMPLATE
    assert config.OPTIONS == {}
    assert config.ANNOTATIONS["get_extra_info"] == get_extra_info
    assert config.ANNOTATIONS["get_version"] == get_version
    assert config.ANNOTATIONS["get_user_agent"] == get_user_agent
    assert config.ANNOTATIONS["get_labels"] == get_labels


def test_issues_config_overrides(settings):
    settings.ISSUES = {
        "BACKEND": "issues.backends.debug.Backend",
        "ISSUE_TEMPLATE": "Custom template: {description}",
        "OPTIONS": {"KEY": "VALUE"},
        "ANNOTATIONS": {"get_extra_info": "issues.utils.get_client_ip"},
    }
    config = IssuesConfig()
    assert config.BACKEND
    assert config.ISSUE_TEMPLATE == "Custom template: {description}"
    assert config.OPTIONS == {"KEY": "VALUE"}
    assert config.ANNOTATIONS["get_extra_info"].__name__ == get_client_ip.__name__


@pytest.mark.parametrize(
    ("annotation", "expectation"),
    [
        ("issues.utils.get_client_ip", does_not_raise()),
        (get_client_ip, does_not_raise()),
        ("", pytest.raises(AttributeError)),
        (None, pytest.raises(AttributeError)),
    ],
)
def test_issues_config_override_annotations(settings, annotation, expectation):
    settings.ISSUES = {"ANNOTATIONS": {"get_extra_info": annotation}}
    config = IssuesConfig()
    with expectation:
        assert config.ANNOTATIONS["get_extra_info"].__name__ == get_client_ip.__name__


def test_issues_config_getattr():
    config = IssuesConfig()
    with pytest.raises(AttributeError):
        assert config.NON_EXISTENT_ATTRIBUTE


def test_issues_config_wrong_annotation():
    settings.ISSUES = {"ANNOTATIONS": {"wrror": "issues.utils.get_client_ip"}}
    config = IssuesConfig()
    with pytest.raises(AttributeError):
        assert config.ANNOTATIONS["get_extra_info"].__name__ == get_client_ip.__name__


#
#
# @patch("issues.config.IssuesConfig")
# def test_reload_issues_config(mock_config):
#     # Simulate a setting change
#     with override_settings(ISSUES=deepcopy(settings.ISSUES)):
#         reload_issues_config(sender=None, setting="ISSUES")
#         # Assert that IssuesConfig was re-instantiated
#         mock_config.assert_called()
#
#
def test_issues_config_repr():
    config = IssuesConfig()
    assert isinstance(str(config), str)
    assert "BACKEND" in str(config)

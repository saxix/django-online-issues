import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest

from issues.utils import (
    HttpResponseRedirectToReferrer,
    get_client_ip,
    get_extra_info,
    get_labels,
    get_user,
    get_user_agent,
    get_version,
)


def test_http_response_redirect_to_referrer_with_referer():
    request = HttpRequest()
    request.META["HTTP_REFERER"] = "/previous-page/"
    response = HttpResponseRedirectToReferrer(request)
    assert response.url == "/previous-page/"


def test_http_response_redirect_to_referrer_without_referer():
    request = HttpRequest()
    response = HttpResponseRedirectToReferrer(request)
    assert response.url == "/"


def test_get_extra_info():
    request = HttpRequest()
    data = {"key": "value"}
    assert get_extra_info(request, data) == {}


@pytest.mark.parametrize(
    ("meta", "expected_ip"),
    [
        ({"HTTP_X_ORIGINAL_FORWARDED_FOR": "192.168.1.1"}, "192.168.1.1"),
        ({"HTTP_X_FORWARDED_FOR": "192.168.1.2"}, "192.168.1.2"),
        ({"HTTP_X_REAL_IP": "192.168.1.3"}, "192.168.1.3"),
        ({"REMOTE_ADDR": "192.168.1.4"}, "192.168.1.4"),
        ({"HTTP_X_FORWARDED_FOR": "192.168.1.5, 10.0.0.1"}, "192.168.1.5"),
        ({}, ""),
    ],
)
def test_get_client_ip(meta, expected_ip):
    request = HttpRequest()
    request.META = meta
    assert get_client_ip(request) == expected_ip


def test_get_labels():
    request = HttpRequest()
    original_labels = ["bug", "feature"]
    assert get_labels(request, original_labels) == original_labels


@pytest.mark.parametrize(
    ("user_agent_string", "expected_user_agent"),
    [
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        ),
        (None, "N/A"),
    ],
)
def test_get_user_agent(user_agent_string, expected_user_agent):
    request = HttpRequest()
    if user_agent_string:
        request.META["HTTP_USER_AGENT"] = user_agent_string
    assert get_user_agent(request) == expected_user_agent


def test_get_user_authenticated():
    request = HttpRequest()
    request.user = User(email="test@example.com")
    assert get_user(request) == "test@example.com"


def test_get_user_unauthenticated():
    request = HttpRequest()
    request.user = AnonymousUser()
    assert get_user(request) == "N/A"


def test_get_version():
    request = HttpRequest()
    assert get_version(request) == "N/A"

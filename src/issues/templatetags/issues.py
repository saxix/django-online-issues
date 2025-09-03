from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def issues_tags() -> str:
    from issues.config import CONFIG

    static_url = static("/")
    url = reverse("issues:create")
    engine = CONFIG.RENDERER.lower()
    if settings.DEBUG:
        suffix = ""
    else:
        suffix = ".min"
    js_url = static(f"issues/issues{suffix}.js")
    css_url = static("issues/issues.css")

    if CONFIG.RENDERER in ["html2canvas", "dom-to-image"]:
        renderer_url = static(f"issues/{CONFIG.RENDERER}{suffix}.js")
    else:
        raise ValueError("Invalid value for RENDERER in django-issues configuration. Check your settings")

    html = f"""
<link rel="stylesheet" href="{css_url}">
<script src="{renderer_url}"></script>
<script src="{static_url}issues/axios{suffix}.js"></script>
<script id="django-issues-script" src="{js_url}" data-engine="{engine}" data-url={url}></script>
"""
    return mark_safe(html)  # noqa: S308

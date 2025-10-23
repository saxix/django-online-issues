from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def issues_tags() -> str:
    from issues.config import ALLOWED_RENDERERS, CONFIG

    url = reverse("issues:create")

    if settings.DEBUG:
        suffix = ""
    else:
        suffix = ".min"
    engine = CONFIG.RENDERER.lower() if CONFIG.RENDERER else ""  # Set engine to empty string if None
    css_url = static("issues/issues.css")
    js_url = static(f"issues/issues{suffix}.js")
    axios_url = static(f"issues/axios{suffix}.js")

    if CONFIG.RENDERER in ALLOWED_RENDERERS:
        renderer_url = CONFIG.get_renderer_script(suffix)
        renderer_url_tag = f'<script src="{renderer_url}"></script>'
    elif CONFIG.RENDERER in [None, ""]:
        renderer_url_tag = ""  # No renderer script if RENDERER is None
    else:
        raise ValueError(
            f"Invalid value '{CONFIG.RENDERER}' for RENDERER in django-issues configuration. Check your settings"
        )

    html = f"""
<link rel="stylesheet" href="{css_url}">
{renderer_url_tag}
<script src="{axios_url}"></script>
<script id="django-issues-script" src="{js_url}" data-engine="{engine}" data-url="{url}"></script>
"""
    return mark_safe(html)  # noqa: S308

from django.contrib.admin.sites import site
from django.urls import include, path
from django.views.generic import TemplateView


class SamplePageView(TemplateView):
    template_name = "sample_page.html"


urlpatterns = (
    path("issues/sample/", SamplePageView.as_view(), name="sample-page"),
    path("issues/", include("issues.urls")),
    path(r"", site.urls),
)

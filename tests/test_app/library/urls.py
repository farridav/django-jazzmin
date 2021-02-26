from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import re_path, reverse, path
from django.views.generic import RedirectView
from django.views.static import serve

try:
    from django.conf.urls import url, include
except ImportError:
    from django.conf.urls.defaults import url, include


def make_messages(request):
    messages.add_message(request, messages.INFO, "Info message")
    messages.add_message(request, messages.ERROR, "Error message")
    messages.add_message(request, messages.WARNING, "Warning message")
    messages.add_message(request, messages.SUCCESS, "Success message")

    return HttpResponseRedirect(reverse("admin:index"))


urlpatterns = [
    url(r"^$", RedirectView.as_view(pattern_name="admin:index", permanent=False)),
    url(r"admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"make_messages/", make_messages, name="make_messages"),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(path("admin/", admin.site.urls))

if settings.DEBUG:
    urlpatterns.append(
        re_path(
            r"^static/(?P<path>.*)$",
            serve,
            kwargs={"document_root": settings.STATIC_ROOT},
        )
    )

if "debug_toolbar" in settings.INSTALLED_APPS:
    try:
        import debug_toolbar

        urlpatterns.append(url(r"__debug__/", include(debug_toolbar.urls)))
    except ImportError:
        pass

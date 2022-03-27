from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin, messages
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path, reverse
from django.views.generic import RedirectView
from django.views.static import serve


def make_messages(request):
    messages.add_message(request, messages.INFO, "Info message")
    messages.add_message(request, messages.ERROR, "Error message")
    messages.add_message(request, messages.WARNING, "Warning message")
    messages.add_message(request, messages.SUCCESS, "Success message")

    return HttpResponseRedirect(reverse("admin:index"))


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="admin:index", permanent=False)),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("make_messages/", make_messages, name="make_messages"),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset"),
    path("admin/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("admin/", admin.site.urls),
)

if settings.DEBUG:
    urlpatterns.append(re_path(r"^static/(?P<path>.*)$", serve, kwargs={"document_root": settings.STATIC_ROOT}))

if "debug_toolbar" in settings.INSTALLED_APPS:
    try:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    except ImportError:
        pass

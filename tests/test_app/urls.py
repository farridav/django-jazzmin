from django.conf import settings
from django.contrib import admin
from django.urls import re_path
from django.views.static import serve

try:
    from django.conf.urls import url, include
except ImportError:
    from django.conf.urls.defaults import url, include

from . import views

urlpatterns = [
    url(r'admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'admin/', admin.site.urls),
    url(r'make_messages/', views.make_messages, name='make_messages'),
]

if settings.DEBUG:
    urlpatterns.append(
        re_path(r'^static/(?P<path>.*)$', serve, kwargs={'document_root': settings.STATIC_ROOT})
    )

if 'debug_toolbar' in settings.INSTALLED_APPS:
    try:
        import debug_toolbar

        urlpatterns.append(url(r'__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
import grocerylist
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'philomaths.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grocerylist/', include('grocerylist.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

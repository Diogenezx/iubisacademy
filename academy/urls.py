from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

import academy.core.views
import academy.cursos.views

  
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^conta/', include('academy.accounts.urls', namespace="accounts")),
    url(r'^', include('academy.core.urls', namespace="core")),
    url(r'^cursos/', include('academy.cursos.urls', namespace="cursos")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

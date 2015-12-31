from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^tf/', include('tf.urls')),
    url(r'^admin/', admin.site.urls),
]
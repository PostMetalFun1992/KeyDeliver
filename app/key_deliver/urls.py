from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('keys/', include('key_deliver_app.urls')),
]

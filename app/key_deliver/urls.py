from django.contrib import admin
from django.urls import path

from key_deliver_app.views import KeyList, KeyDetail, KeyRepayer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('keys/', KeyList.as_view()),
    path('keys/<int:pk>/', KeyDetail.as_view()),
    path('keys_repayer/', KeyRepayer.as_view()),
]

from django.contrib import admin
from django.urls import path

from key_deliver_app.views import KeyList, KeyDetail, KeyRepay


urlpatterns = [
    path('admin/', admin.site.urls),
    path('keys/', KeyList.as_view()),
    path('keys/<int:pk>/', KeyDetail.as_view()),
    path('keys_repayer/', KeyRepay.as_view()),
]

from django.urls import path

from key_deliver_app import views


urlpatterns = [
    path('', views.KeyList.as_view())
]

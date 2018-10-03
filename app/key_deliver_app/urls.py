from django.urls import path

from key_deliver_app.views import KeyList, KeyDetail


urlpatterns = [
    path('', KeyList.as_view()),
    path('<int:pk>/', KeyDetail.as_view()),
]

from django.urls import path

from account.api.views import RegisterApiView, LoginApiView

urlpatterns = [
    path('signup/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
]

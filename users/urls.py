from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
        path("register/", views.UserRegisterAPIView.as_view(), name="register"),
        path("login/", views.UserLoginAPIView.as_view(), name="login"),
]
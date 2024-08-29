from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("verify/", views.verify, name="verify"),
    path("logout/", views.signout, name="signout"),
    path("login/", views.signin, name="signin"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("profile/", views.profile, name="profile"),
    path("change_password/", views.change_password, name="change_password"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in),
    path('log-in/', views.log_in),
    path("sign-in/register/", views.register_user),
    path("log-in/login/", views.login_user),
    path("logout/", views.logout_user),
    path("<int:user_id>/account", views.view_user),
]
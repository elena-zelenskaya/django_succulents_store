from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in),
    path('log-in/', views.log_in),
    # path("register/", views.register_user),
    # path("login/", views.login_user),
    # path("logout/", views.logout_user),
    # path("<int:user_id>/", views.view_user),
]
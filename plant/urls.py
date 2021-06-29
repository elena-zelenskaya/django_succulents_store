from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('<int:plant_id>/', views.view_plant),
    # path('delete-idea/<int:idea_id>/', views.delete_idea),
    # path("<int:idea_id>/", views.view_idea),
    # path("likes/<int:idea_id>/", views.create_like),
    # path("edit/<int:idea_id>/", views.edit_idea),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('<int:plant_id>/', views.view_plant),
    path('plant-form/', views.plant_form),
    path('plant-form/plant-upload/', views.upload_plant),
    path("list/", views.all_uploaded_succulents),
    # path("likes/<int:idea_id>/", views.create_like),
    # path("edit/<int:idea_id>/", views.edit_idea),
]


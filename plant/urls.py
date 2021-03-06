from django.urls import path
from . import views

urlpatterns = [
    path('<int:plant_id>/', views.view_plant),
    path('plant-form/', views.plant_form),
    path('plant-form/plant-upload/', views.upload_plant),
    path("list/", views.all_uploaded_succulents),
    path("my-cart/", views.my_cart),
    path("my-cart/delete-cart-item/", views.delete_cart_item),
    path("add-to-cart/", views.add_to_cart),
    path("my-cart/checkout/", views.checkout),
    path("my-cart/checkout/buy/", views.buy),
    path("success/", views.success),
]


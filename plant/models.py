from django.db import models
from user.models import User

class PlantManager(models.Manager):
    def upload_validator(self, session_data, post_data):
        errors = {}
        if len(post_data["plant_name"]) < 2:
            errors["first_name_length"] = "Succulent name should be at least 2 characters"
        elif not post_data["plant_name"].isalpha():
            errors["first_name_letters"] = "Succulent name should only contain letters"
        else:
            session_data["plant_name"] = post_data["plant_name"]
        if len(post_data["description"]) < 20:
            errors["description_length"] = "Succulent description should be at least 20 characters"
        else:
            session_data["description"] = post_data["description"]
        if not post_data["price"]:
            errors["price"] = "Price is required"
        else:
            session_data["price"] = post_data["price"]
        if not post_data["quantity"]:
            errors["quantity"] = "Quantity is required"
        else:
            session_data["quantity"] = post_data["quantity"]
        return errors

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    picture = models.FileField(upload_to="plants_images", default='plants_images/default_succulent.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlantManager()

class Order(models.Model):
    plants = models.ManyToManyField(Plant, related_name = "orders")
    order_sum = models.FloatField(default=0.0)
    user = models.ForeignKey(User, related_name="user_orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

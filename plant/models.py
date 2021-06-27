from django.db import models
from user.models import User

# Create your models here.
# class Plant(models.Model):
#     name = models.CharField(max_length=45)
#     description = models.TextField()
#     price = models.FloatField()
#     picture = models.FileField(upload_to="plants_images", default='plants_images/default_succulent.jpg')
#     # orders = models.ForeignKey(Order, related_name = "users")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Order(models.Model):
#     plants = models.ManyToManyField(Plant, related_name = "orders")
#     positions = models.TextField()
#     order_sum = models.FloatField(default=0.0)
#     order_amount = models.IntegerField(default=0)
#     user = models.ForeignKey('User', related_name="user_orders", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

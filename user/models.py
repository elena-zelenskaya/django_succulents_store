from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def register_validator(self, session_data, post_data, emails_list):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(post_data["first_name"]) < 2:
            errors["first_name_length"] = "First name should be at least 2 characters"
        elif not post_data["first_name"].isalpha():
            errors["first_name_letters"] = "First name should only contain letters"
        else:
            session_data["first_name"] = post_data["first_name"]
        if len(post_data["last_name"]) < 2:
            errors["last_name_length"] = "Last name should be at least 2 characters"
        elif not post_data["last_name"].isalpha():
            errors["last_name_letters"] = "Last name should only contain letters"
        else:
            session_data["last_name"] = post_data["last_name"]
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["invalid_email"] = "Invalid email address!"
        elif post_data["email"] in emails_list:
            errors["existing_email"] = "This email already exists!"
        else:
            session_data["email"] = post_data["email"]
        if len(post_data["password"]) < 8:
            errors["password_length"] = "Password should be at least 8 characters"
        if post_data["password"] != post_data["confirm_password"]:
            errors["password_confirmation"] = "Password confirmation doesn't match the password"
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())



class AddressManager(models.Manager):
    def address_validator(self, session_data, post_data):
        errors={}
        if len(post_data["line1"]) == 0:
            errors["missing_field"] = "This field is required"
        else:
            session_data["street_address"] = post_data["street_address"]
        if len(post_data["state"]) == 0:
            errors["missing_field"] = "This field is required"
        else:
            session_data["state"] = post_data["state"]
        if len(post_data["city"]) == 0:
            errors["missing_field"] = "This field is required"
        else:
            session_data["city"] = post_data["city"]
        if len(post_data["zip"]) != 5:
            errors["zip_length"] = "Zip code should contain five numbers"
        elif not post_data["zip"].isnumeric():
            errors["zip_letters"] = "Zip code should only contain numbers"
        else:
            session_data["zip"] = post_data["zip"]
        return errors


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    profile_picture = models.FileField(upload_to="profile_pictures", default='profile_pictures/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    objects = UserManager()

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_address")
    state = models.CharField(max_length=20, default="")
    zip_code = models.IntegerField(default="")
    city = models.CharField(max_length=45, default="")
    line1 = models.TextField(max_length=100, default="")
    line2 = models.TextField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AddressManager()



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Address
import bcrypt

# Create your views here.
def sign_in(request):
    return render(request, 'registration.html')

def log_in(request):
    return render(request, 'login.html')

def all_users_emails():
    all_users_emails = []
    for user in User.objects.all():
        all_users_emails.append(user.email)
    return all_users_emails

def register_user(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.session, request.POST, all_users_emails())
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('../')
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = pw_hash)
            if "profile_picture" in request.FILES:
                profile_picture = request.FILES["profile_picture"]
                new_user.profile_picture = profile_picture
                new_user.save()
            request.session['userid'] = new_user.id
            return redirect("/")
    request.session.flush()
    return redirect("/")

def login_user(request):
    if request.method == "POST":
        email = request.POST["email_login"]
        password = request.POST["password_login"]
        if not User.objects.authenticate(email, password):
            messages.error(request, "Email and Password do not match", extra_tags='login')
            return redirect("../")
        else:
            user = User.objects.get(email=email)
            request.session["userid"] = user.id
            return redirect('/')
    request.session.flush()
    return redirect("/")

def view_user(request, user_id): 
    if not User.objects.filter(id = user_id):
        return render(request, "error.html")
    elif 'userid' not in request.session.keys():
        return render(request, "error.html")
    list_of_orders = []
    for order in User.objects.get(id = user_id).user_orders.all():
        plants = order.plants.order_by("name")
        amounts = order.amounts.split(',')
        created_at = order.created_at
        total = order.order_sum
        plant_dict = dict(zip(amounts, plants.all()))
        order_info = [created_at, total, plant_dict]
        list_of_orders.append(order_info)
    context = {
		"user": User.objects.get(id = user_id),
		"orders_list": list_of_orders,
	}
    if request.session['userid'] == user_id:
        return render(request, 'user_info.html', context)
    return render(request, "error.html")

def upload_new_profile_picture(request, user_id):
    user = User.objects.get(id = user_id)
    if "new_profile_picture" not in request.FILES:
        messages.error(request, "No File Chosen", extra_tags='no_file')
        return redirect("../")
    profile_picture = request.FILES["new_profile_picture"]
    user.profile_picture = profile_picture
    user.save()
    return redirect("../")

def delete_user(request, user_id):
    user_to_delete = User.objects.get(id = user_id)
    if request.session['userid'] == user_id:
        user_to_delete.delete()
        request.session.flush()
        return redirect("/")

def add_address(request):
    if request.method == "POST":
        errors = Address.objects.address_validator(request.session, request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='address_error')
            return redirect('../')
        user = User.objects.get(id = request.session['userid'])
        line1 = request.POST["street_address"]
        line2 = request.POST["apt"]
        city = request.POST["city"]
        state = request.POST["state"]
        zip_code = request.POST["zip"]
        new_address = Address.objects.create(user = user, line1 = line1, line2 = line2, city = city, state = state, zip_code = zip_code)
        return redirect("/succulents/my-cart/checkout/")
    return redirect('/')

def logout_user(request):
    request.session.flush()
    return redirect("/")



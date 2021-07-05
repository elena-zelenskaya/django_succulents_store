from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from .models import Plant

# Create your views here.
def home(request):
    if "userid" in request.session.keys():
        context = {
            "user": User.objects.get(id=request.session["userid"]),
            "succulents": Plant.objects.all()[:6],
            "ordered_succulents": Plant.objects.order_by("name")[:6],
        }
    else:
        context = {"succulents": Plant.objects.all()[:6], "ordered_succulents": Plant.objects.order_by("name")[:6]}
    return render(request, "index.html", context)


def view_plant(request, plant_id):
    if "userid" in request.session.keys():
        context = {
            "plant": Plant.objects.get(id=plant_id),
            "all_succulents": Plant.objects.exclude(id=plant_id),
            "user": User.objects.get(id=request.session["userid"]),
        }
    else:
        context = {
            "plant": Plant.objects.get(id=plant_id),
            "all_succulents": Plant.objects.exclude(id=plant_id),
        }
    return render(request, "plant_page.html", context)


def upload_plant(request):
    if request.method == "POST":
        errors = Plant.objects.upload_validator(request.session, request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="plants_errors")
            return redirect("../")
        else:
            name = request.POST["plant_name"]
            description = request.POST["description"]
            price = request.POST["price"]
            quantity = request.POST["quantity"]
            new_succulent = Plant.objects.create(name=name, description=description, price=price, quantity=quantity)
            if "plant_picture" in request.FILES:
                picture = request.FILES["plant_picture"]
                new_succulent.picture = picture
                new_succulent.save()
            return redirect("../../list/")
    request.session.flush()
    return redirect("/")


def plant_form(request):
    return render(request, "upload_plants.html")


def all_uploaded_succulents(request):
    context = {"succulents": Plant.objects.all()}
    return render(request, "all_succulents.html", context)


def my_cart(request):
    print(request.session["plants_in_cart"])
    if "userid" in request.session.keys():
        context = {
            "user": User.objects.get(id=request.session["userid"]),
            "plants_in_cart": request.session["plants_in_cart"],
            "total": request.session["total"],
        }
    else:
        context = {
            "plants_in_cart": [],
            "total": 0,
        }
    return render(request, "my_cart.html", context)


def add_to_cart(request):
    if not "plants_in_cart" in request.session.keys():
        request.session["plants_in_cart"] = []
    if not "total" in request.session.keys():
        request.session["total"] = 0
    if request.method == "POST":
        new_plant = {
            "plant_id": int(request.POST["plant_id"]),
            "plant_name": Plant.objects.get(id=request.POST["plant_id"]).name,
            "plant_price": Plant.objects.get(id=request.POST["plant_id"]).price,
            "plant_amount": request.POST["quantity"],
        }
        print(new_plant)
        request.session["total"] += new_plant["plant_price"] * int(new_plant["plant_amount"])
        request.session["plants_in_cart"].append(new_plant)
        return redirect("../my-cart/")


def delete_cart_item(request):
    if request.method == "POST":
        plant_id = request.POST["plant_id"]
        for plant in request.session["plants_in_cart"]:
            if plant['plant_id'] == int(plant_id):
                request.session["plants_in_cart"].remove(plant)
                request.session["total"] -= plant["plant_price"] * int(plant["plant_amount"])
                return redirect("../")
    return redirect("/")
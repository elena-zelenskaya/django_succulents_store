from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from .models import Plant, Order

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
    if "userid" in request.session.keys() and "plants_in_cart" in request.session.keys():
        context = {
            "user": User.objects.get(id=request.session["userid"]),
            "plants_in_cart": request.session["plants_in_cart"],
            "total": round(request.session["total"], 2),
        }
        return render(request, "my_cart.html", context)
    elif "userid" in request.session.keys():
        context = {
            "user": User.objects.get(id=request.session["userid"]),
        }
        return render(request, "my_cart.html", context)
    else:
        return render(request, "my_cart.html")


def add_to_cart(request):
    if not "plants_in_cart" in request.session.keys():
        request.session["plants_in_cart"] = []
    if not "total" in request.session.keys():
        request.session["total"] = 0.0
    if request.method == "POST":
        new_plant = {
            "plant_id": int(request.POST["plant_id"]),
            "plant_name": Plant.objects.get(id=request.POST["plant_id"]).name,
            "plant_price": Plant.objects.get(id=request.POST["plant_id"]).price,
            "plant_amount": request.POST["quantity"],
        }
        request.session["total"] += new_plant["plant_price"] * int(new_plant["plant_amount"])
        request.session["plants_in_cart"].append(new_plant)
        return redirect("../my-cart/")

def checkout(request):
    if "userid" in request.session.keys():
        context = {
            "user": User.objects.get(id=request.session["userid"]),
            "plants_to_buy": request.session["plants_in_cart"],
            "total": round(request.session["total"], 2),
        }
        return render(request, "checkout.html", context)
    else:
        return render(request, "error.html")

def buy(request):
    if "userid" not in request.session.keys():
        return render(request, "error.html")
    if request.method == "POST":
        user = User.objects.get(id = request.session["userid"])
        order_sum = round(request.session["total"], 2)
        plants = map(lambda plant: Plant.objects.get(id = plant['plant_id']), request.session["plants_in_cart"])
        str_amount = ''
        for plant in request.session["plants_in_cart"]:
            str_amount += plant['plant_amount'] + ','
        new_order = Order.objects.create(user = user, order_sum = order_sum, amounts = str_amount[:-1])
        new_order.plants.set(list(plants))
        del request.session['plants_in_cart']
        del request.session['total']
        return redirect("../../../success/")
    else:
        return render(request, "error.html")

def success(request):
    plants = User.objects.get(id = request.session["userid"]).user_orders.last().plants
    amounts = User.objects.get(id = request.session["userid"]).user_orders.last().amounts.split(',')
    context = {
		"user": User.objects.get(id = request.session["userid"]),
		"current_order": User.objects.get(id = request.session["userid"]).user_orders.last(),
		"plant_dict": dict(zip(amounts, plants.all())),
	}
    return render(request, "success.html", context)


def delete_cart_item(request):
    if request.method == "POST":
        plant_id = request.POST["plant_id"]
        for plant in request.session["plants_in_cart"]:
            if plant['plant_id'] == int(plant_id):
                request.session["plants_in_cart"].remove(plant)
                request.session["total"] -= plant["plant_price"] * int(plant["plant_amount"])
                if len(request.session["plants_in_cart"]) == 0:
                    del request.session["plants_in_cart"]
                    del request.session["total"]
                return redirect("../")
    return redirect("/")
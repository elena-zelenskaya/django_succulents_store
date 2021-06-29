from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from .models import Plant

# Create your views here.
def home(request):
    if 'userid' in request.session.keys():
        context = {
            'user': User.objects.get(id = request.session['userid'])
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

def view_plant(request, plant_id):
    pass

def upload_plant(request):
    if request.method == "POST":
        errors = Plant.objects.upload_validator(request.session, request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='plants_errors')
            return redirect('../')
        else:
            name = request.POST["plant_name"]
            description = request.POST["description"]
            price = request.POST["price"]
            quantity = request.POST["quantity"]
            new_succulent = Plant.objects.create(name = name, description = description, price = price, quantity = quantity)
            if "plant_picture" in request.FILES:
                picture = request.FILES["plant_picture"]
                new_succulent.picture = picture
                new_succulent.save()
            request.session.flush()
            return redirect("../../list/")
    request.session.flush()
    return redirect("/")

def plant_form(request):
    return render(request, "upload_plants.html")

def all_uploaded_succulents(request):
    context = {
		"succulents": Plant.objects.all()
	}
    return render(request, "all_succulents.html", context)
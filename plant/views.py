from django.shortcuts import render
from user.models import User

# Create your views here.
def home(request):
    if 'userid' in request.session.keys():
        context = {
            'user': User.objects.get(id = request.session['userid'])
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
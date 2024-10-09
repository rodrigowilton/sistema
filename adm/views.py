from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

@login_required
def menu_adm(request):
    return render(request, 'menu_adm.html')
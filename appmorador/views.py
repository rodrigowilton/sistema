from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def app_morador(request):
    return render(request, 'configuracao.html')
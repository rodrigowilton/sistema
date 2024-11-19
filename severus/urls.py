"""
URL configuration for severus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("app/", include("app.urls")),
    path("adm/", include("adm.urls")),
    path("apto/", include("apto.urls")),
    path("pessoas/", include("pessoas.urls")),
    path("veiculos/", include("veiculos.urls")),
    path("pets/", include("pets.urls")),
    path("contatoemergencia/", include("contatoemergencia.urls")),
    path("permissaoacesso/", include("permissaoacesso.urls")),
    path("liberacaoacesso/", include("liberacaoacesso.urls")),
    path("recados/", include("recados.urls")),
    path("areas/", include("areas.urls")),
    path("areasparalelas/", include("areasparalelas.urls")),
    path("horarioagendamento/", include("horarioagendamento.urls")),
    path("feriado/", include("feriado.urls")),
    path("agendamento/", include("agendamento.urls")),
    path("sindico/", include("sindico.urls")),
    path("funcionario/", include("funcionario.urls")),
    path("empresa/", include("empresa.urls")),
    path("servicoempresa/", include("servicoempresa.urls")),
]

"""LES_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views

app_name = "ReserveManagement"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('create/', views.create, name="create"),
    path('read/', views.ReadListView.as_view(), name="read"),
    path('read_matricula/', views.read_matricula, name="read_matricula"),
    path('read/<str:matricula>/', views.TableListView.as_view(), name="read_user_table"),
    path('update/<int:reserva_id>', views.update, name='update'),
    path('delete/<int:reserva_id>', views.delete, name='delete'),
    path('create_table/', views.createTable, name="create_table"),
    path('read_table/', views.readTable, name="read_table"),
    path('delete_table/<int:tabela_id>', views.deleteTable, name='delete_table'),
    path('update_table/<int:tabela_id>', views.updateTable, name='update_table'),
]

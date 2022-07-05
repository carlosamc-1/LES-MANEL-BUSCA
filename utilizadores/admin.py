from django.contrib import admin
from .models import Utilizador,Administrador,Cliente,Funcionario
# Register your models here.
admin.site.register(Utilizador)

admin.site.register(Administrador)

admin.site.register(Cliente)

admin.site.register(Funcionario)

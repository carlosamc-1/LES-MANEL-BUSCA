# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models import Q
from datetime import datetime,timedelta

class Utilizador(User):
    contacto = models.CharField(max_length=20)
    valido = models.CharField(max_length=255)

    def getProfiles(self):
        type = ''
        if Administrador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Administrador')
        if Cliente.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Cliente')
        if Funcionario.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Funcionario')
        return type
    
    def concat(self, type, string):
        if type == '':
            type = string
        else:
            type += ', '+string
        return type

    @property
    def firstProfile(self):
        return self.getProfiles().split(' ')[0]
    
    def getUser(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Cliente").exists():
            result = Cliente.objects.get(id=self.id)
        elif user.groups.filter(name = "Administrador").exists():
            result = Administrador.objects.get(id=self.id)
        elif user.groups.filter(name = "Funcionario").exists():
            result = Funcionario.objects.get(id=self.id)
   
        else:
            result = None
        return result   
    
    def getProfile(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Cliente").exists():
            result = "Cliente"
        elif user.groups.filter(name = "Administrador").exists():
            result = "Administrador"
        elif user.groups.filter(name = "Funcionario").exists():
            result = "Funcionario"
        else:
            result = None
        return result 

    def emailValidoUO(self,uo):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Cliente").exists():
            utilizador = Cliente.objects.get(email=self.email)
        elif user.groups.filter(name = "Administrador").exists():
            return True
        elif user.groups.filter(name = "Funcionario").exists():
            utilizador = Funcionario.objects.get(email=self.email)
        else:
            return False
        if utilizador.faculdade == uo:
            return True
        else:
            return False  

    def emailValidoCliente(self):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Administrador").exists():
            return True
        else:
            return False  
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    class Meta:
        db_table = 'Utilizador'






class Administrador(Utilizador):
    class Meta:
        db_table = 'Administrador'


class Cliente(Utilizador):
    nif = models.IntegerField(db_column='NIF', blank=True, null=True)  # Field name made lowercase.
    morada = models.CharField(db_column='Morada', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_nascimento = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de nascimento', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    class Meta:
        db_table = 'Cliente'

class Funcionario(Utilizador):
    funcao = models.CharField(db_column='Funcao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = 'Funcionario'


def list_to_queryset(model, data):
    from django.db.models.base import ModelBase
    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )
    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)





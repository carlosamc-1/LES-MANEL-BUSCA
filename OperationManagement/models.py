# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import datetime
from django.db import models



class RegistoMovimento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey('AdminManagement.Parque', models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_entrada = models.DateTimeField(default=datetime.now, db_column='Data de entrada', blank=False, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_saida = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de saida', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    provas = models.CharField(db_column='Provas', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        saida = ""
        if (self.data_de_saida != None):
            saida = self.data_de_saida
        return "Matrícula: " + str(self.matricula) + ", Entrada: " + str(self.data_de_entrada) + ", Saída: " + str(self.data_de_saida)

    class Meta:
        db_table = 'RegistoMovimento'

class Viatura(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey('PaymentManagement.Contrato', models.CASCADE, db_column='ContratoID', null=True)  # Field name made lowercase.
    registo_movimentoid = models.ForeignKey(RegistoMovimento, models.CASCADE, db_column='Registo-movimentoID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    marca = models.CharField(db_column='Marca', max_length=255, blank=True, null=True)  # Field name made lowercase.
    modelo = models.CharField(db_column='Modelo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.matricula)

    class Meta:
        db_table = 'Viatura'


class TabelaMatriculas(models.Model):
    pais = models.CharField(db_column='Pais', max_length=255)
    formato = models.CharField(db_column='Formato', max_length=255)

    def __str__(self):
        return "País: " + str(self.pais) + ", Formato: " + str(self.formato)

    class Meta:
        db_table = 'TabelaMatriculas'
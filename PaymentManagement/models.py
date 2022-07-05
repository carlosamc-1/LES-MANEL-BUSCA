# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.urls import reverse
from datetime import datetime, timezone, date, timedelta
from django.db import connection, models
import numpy as np
from dateutil.relativedelta import relativedelta


class Periodicidade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    periodicidade = models.CharField(db_column='Periodicidade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    horario = models.CharField(db_column='Horario', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Periodicidade'

class Dia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Dia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    periodicidadeid = models.ForeignKey(Periodicidade, models.CASCADE, db_column='Periodicidade', default=1)  # Field name made lowercase.

    class Meta:
        db_table = 'Dia'

class Contrato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey('AdminManagement.Parque', models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    clienteid = models.ForeignKey('utilizadores.Cliente', models.CASCADE, db_column='ClienteID', default=1)  # Field name made lowercase.
    periodicidadeid = models.ForeignKey(Periodicidade, models.CASCADE, db_column='PeriodicidadeID', default=1)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_inicio = models.DateField(auto_now=False, auto_now_add=False, db_column='Data de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_termino = models.DateField(auto_now=False, auto_now_add=False, db_column='Data de termino', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    valido = models.BooleanField(db_column='Valido', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('contrato:contrato-detail', kwargs={'id': self.id})
    
    def getParque(self):
        return 'AdminManagement.Parque'.objects.filter(id=self)

    @staticmethod
    def makeOptions():
        parques = 'AdminManagement.Parque'.objects.all()
        options=([(parque.id, parque.nome) for parque in parques])
        return options

    class Meta:
        db_table = 'Contrato'

class Pagamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True, null=True)  # Field name made lowercase.
    reservaid = models.ForeignKey('Reserva', models.CASCADE, db_column='ReservaID', blank=True, null=True)  # Field name made lowercase.
    registoid = models.ForeignKey('OperationManagement.RegistoMovimento', models.CASCADE, db_column='RegistoID', blank=True, null=True)  # Field name made lowercase.
    montante = models.FloatField(db_column='Montante')  # Field name made lowercase.
    estado_do_pagamento = models.TextField(db_column='Estado do pagamento')  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    data_de_vencimento = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de vencimento', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comprovativo = models.FileField(db_column='Comprovativo', blank=True, null=True)
    numero_cartao = models.TextField(blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Pagamento'

class Fatura(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pagamentoid = models.ForeignKey(Pagamento, models.CASCADE, db_column='PagamentoID', blank=True, null=True)  # Field name made lowercase.
    clienteid = models.ForeignKey('utilizadores.Cliente', models.CASCADE, db_column='ClienteID', blank=True, null=True)  # Field name made lowercase.
    nomeEmpresa = models.TextField(db_column='NomeEmpresa', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    moradaEmpresa = models.TextField(db_column='MoradaEmpresa', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    nifEmpresa = models.IntegerField(db_column='NIFEmpresa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Fatura'

class Reclamacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    faturaid = models.ForeignKey(Fatura, models.CASCADE, db_column='FaturaID', blank=True, null=True)  # Field name made lowercase.
    registo_movimentoid = models.ForeignKey('OperationManagement.RegistoMovimento', models.CASCADE, db_column='Registo-movimentoID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reclamacao = models.CharField(db_column='Reclamacao', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Reclamacao'


class Reserva(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey('AdminManagement.Parque', models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    viaturaid = models.ForeignKey('OperationManagement.Viatura', models.CASCADE, db_column='ViaturaID', default=1)  # Field name made lowercase.
    data_de_inicio = models.DateField(auto_now=False, auto_now_add=False, db_column='Data de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_termino = models.DateField(auto_now=False, auto_now_add=False, db_column='Data de termino', blank=True, null=True)
    hora_de_inicio = models.TimeField(db_column='Hora de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hora_de_termino = models.TimeField(db_column='Hora de termino', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    
    @staticmethod
    def makeOptions():
        if "main_reserva" in connection.introspection.table_names():
            parques = 'AdminManagement.Parque'.objects.all()
            options=([(parque.nome) for parque in parques])
            return options
        else:
            return (("1", "No Database created"),)
    
    @staticmethod
    def makeOptions1():
        if "main_reserva" in connection.introspection.table_names():
            lugar = 'AdminManagement.Lugar'.objects.all()
            options=([(lugar.nome) for l in lugar])
            return options
        else:
            return (("1", "No Database created"),)

    def makeOptions2():
        if "main_reserva" in connection.introspection.table_names():
            viatura = 'OperationManagement.Viatura'.objects.all()
            options=([(viatura.matricula) for v in viatura])
            return options
        else:
            return (("1", "No Database created"),)
    
    class Meta:
        db_table = 'Reserva'

class TabelaPrecos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey('AdminManagement.Parque', models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    reservaid = models.ForeignKey(Reserva, models.CASCADE, db_column='ReservaID', blank=True, null=True)  # Field name made lowercase.
    preco_por_hora = models.FloatField(db_column='Preco por hora')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taxa_por_hora = models.FloatField(db_column='Taxa por hora')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taxa_noturna = models.FloatField(db_column='Taxa noturna')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taxa_da_multa = models.FloatField(db_column='Taxa da multa')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_contrato_dia = models.FloatField(db_column='Preco Contrato Dia')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_contrato_diurno = models.FloatField(db_column='Preco Contrato Diurno')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_contrato_noturno = models.FloatField(db_column='Preco Contrato Noturno')  # Field name made lowercase. Field renamed to remove unsuitable characters.


    def get_absolute_url(self):
        return reverse("parque:parque-detail", kwargs={"id": self.id})

    @staticmethod
    def getDaysContrato(contrato = None, all=True):
        periodicidade = contrato.periodicidadeid
        if all:
            if periodicidade.periodicidade == "diário":
                days = contrato.data_de_termino - contrato.data_de_inicio
            else:
                week = ""
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Segunda-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Terça-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Quarta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Quinta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Sexta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Sábado").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Domingo").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                days = np.busday_count(contrato.data_de_inicio, contrato.data_de_termino, weekmask=week)
        else:
            if periodicidade.periodicidade == "diário":
                if (contrato.data_de_inicio + relativedelta(months=1)) <= contrato.data_de_termino:
                    days = (contrato.data_de_inicio + relativedelta(months=1)) - contrato.data_de_inicio
                else:
                    days = contrato.data_de_termino - contrato.data_de_inicio
                days = days.days
            else:
                week = ""
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Segunda-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Terça-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Quarta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Quinta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Sexta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Sábado").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if 'PaymentManagement.Dia'.objects.filter(periodicidadeid=periodicidade, nome="Domingo").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                days = np.busday_count(contrato.data_de_inicio, contrato.data_de_inicio + relativedelta(months=1), weekmask=week)
        
        return days

    @staticmethod
    def getHoursReserva(reserva = None):
        days = reserva.data_de_termino - reserva.data_de_inicio
        return days

    @staticmethod
    def getTime(date = None):    
        days = datetime.now() - date
        return days

    @staticmethod
    def getPrice(contrato = None, reserva = None, registo = None, all=True):
        if contrato:
            tabelaPrecos = TabelaPrecos.objects.get(parqueid = contrato.parqueid)
            periodicidade = contrato.periodicidadeid
            dias = TabelaPrecos.getDaysContrato(contrato = contrato, all=all)
            if periodicidade.horario == "24H":
                price = dias * tabelaPrecos.preco_contrato_dia
            if periodicidade.horario == "diurno":
                price = dias * tabelaPrecos.preco_contrato_diurno
            if periodicidade.horario == "noturno":
                price = dias * tabelaPrecos.preco_contrato_noturno
        elif reserva:
            tabelaPrecos = TabelaPrecos.objects.get(parqueid = reserva.parqueid)
            dias = TabelaPrecos.getHoursReserva(reserva = reserva)
            price = dias.total_seconds()/3600 * tabelaPrecos.preco_por_hora
        else:
            tabelaPrecos = TabelaPrecos.objects.get(parqueid = registo.parqueid)
            dias = TabelaPrecos.getTime(date = registo.data_de_entrada)
            price = dias.total_seconds()/3600 * tabelaPrecos.preco_por_hora
        return "{:.2f}".format(price)

    class Meta:
        db_table = 'TabelaPrecos'
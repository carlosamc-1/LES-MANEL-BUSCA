# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Parque(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True, unique=True)  # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.
    zonas = models.IntegerField(db_column='Zonas')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=50, default="Aberto")
    morada = models.CharField(db_column='Morada', max_length=255, blank=True, null=True, unique=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=60, blank=True, null=True)
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    foto = models.ImageField(upload_to='images/', db_column='Foto', blank=True, null=True)

    def get_absolute_url(self):
        return f"/AdminManagement/{self.id}/"

    @staticmethod
    def make_options():
        return (("Aberto","Aberto"),("Fechado","Fechado"),("Manutencao","Manutencao"))

    @staticmethod
    def makeOptions():
        parques = Parque.objects.all()
        options=([(parque.id, parque.nome) for parque in parques])
        return options
    
    def get_nome():
        return Parque.nome

    class Meta:
        db_table = 'Parque'

class Zona(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey('Parque', models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    numero_da_zona = models.IntegerField(db_column='Numero da zona', blank=True, null=True, unique=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lugares = models.IntegerField(db_column='Lugares')  # Field name made lowercase.
    tipo_de_zona = models.CharField(db_column='Tipo de zona', max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return f"/AdminManagement/{self.parqueid.id}/zona/{self.id}/"

    @staticmethod
    def make_options():
        return (("Zona Normal","Zona Normal"),("Zona de Reservas ou Contratos","Zona de Reservas ou Contratos"))

    class Meta:
        db_table = 'Zona'

class Lugar(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    zonaid = models.ForeignKey('Zona', models.CASCADE, db_column='ZonaID')  # Field name made lowercase.
    contratoid = models.ForeignKey('PaymentManagement.Contrato', models.CASCADE, db_column='ContratoID', null=True)  # Field name made lowercase.
    viaturaid = models.ForeignKey('OperationManagement.Viatura', models.CASCADE, db_column='ViaturaID', null=True)  # Field name made lowercase.
    reservaid = models.ForeignKey('PaymentManagement.Reserva', models.CASCADE, db_column='ReservaID', null=True)  # Field name made lowercase.
    numero_do_lugar = models.IntegerField(db_column='Numero do lugar', blank=True, null=True, unique=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado = models.CharField(db_column='Estado', max_length=255, default="Disponivel")  # Field name made lowercase.

    def get_absolute_url(self):
        return f"/AdminManagement/{1}/zona/{self.zonaid.id}/lugar/{self.id}"

    @staticmethod
    def make_options():
        return (("Disponivel","Disponivel"),("Ocupado","Ocupado"),("Manutencao","Manutencao"))

    @staticmethod
    def makeOptions():
        lugares = Lugar.objects.filter(contratoid__isnull=True).filter(reservaid__isnull=True).filter(viaturaid__isnull=True)
        options=([(lugar.id, lugar.numero_do_lugar) for lugar in lugares])
        return options

    class Meta:
        db_table = 'Lugar'
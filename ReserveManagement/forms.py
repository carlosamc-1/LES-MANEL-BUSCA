import re
from django import forms
from django.forms import ModelForm, ValidationError

from AdminManagement.models import Lugar, Parque
from OperationManagement.models import TabelaMatriculas, Viatura
from PaymentManagement.models import Reserva, TabelaPrecos
import datetime
import time

class ParqueModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nome

class LugarModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.numero_do_lugar
    
class ViaturaModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.matricula

class CreateReserve(ModelForm):
    OPTIONS_parque = Reserva.makeOptions()
    # parqueid = forms.CharField(widget=forms.Select(choices=OPTIONS_parque, attrs={'class' : 'input'}), label='Parque', required=True)
    parqueid = ParqueModelChoiceField(label="Parque", queryset=Parque.objects.all(), required=True, widget=forms.Select(attrs={'class': 'field2'}))
    data_de_inicio = forms.DateField(label="Data de Início", widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'field1'}))
    data_de_termino = forms.DateField(label="Data de Término", widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'field1'}))
    hora_de_inicio = forms.TimeField(label="Hora de Início", widget=forms.widgets.TimeInput(attrs={'type': 'time', 'class': 'field'}))
    hora_de_termino = forms.TimeField(label="Hora de Término", widget=forms.widgets.TimeInput(attrs={'type': 'time', 'class': 'field'}))
    lugar = LugarModelChoiceField(label="Lugar", queryset=Lugar.objects.filter(reservaid__isnull = True).filter(contratoid__isnull = True), required=True, widget=forms.Select(attrs={'class': 'field2'}))
    viaturaid = ViaturaModelChoiceField(label="Matrícula", queryset=Viatura.objects.all(), required=True,widget=forms.Select(attrs={'class': 'field2'}))

    class Meta:
        model = Reserva
        fields = ['parqueid', 'data_de_inicio', 'data_de_termino', 'hora_de_inicio', 'hora_de_termino', 'lugar', 'viaturaid']
    

    def clean_data_de_termino(self):
        data_inicio = self.cleaned_data.get('data_de_inicio')
        data_termino = self.cleaned_data.get('data_de_termino')
        if data_inicio < datetime.date.today():
            raise forms.ValidationError("A data precisa de ser depois de hoje")
        if data_termino < data_inicio:
            raise forms.ValidationError("A data de término tem que ser depois da data de início")
        return data_termino

    def clean_hora_de_termino(self):
        hora_inicio = self.cleaned_data.get('hora_de_inicio')
        hora_termino = self.cleaned_data.get('hora_de_termino')
        data_inicio = self.cleaned_data.get('data_de_inicio')
        data_termino = self.cleaned_data.get('data_de_termino')
        hora_atual = datetime.datetime.now().time()
        if  data_inicio == data_termino and hora_termino < hora_inicio:
            raise forms.ValidationError("A hora de término precisa ser maior que a hora de início")
        if data_inicio == datetime.date.today() and hora_inicio < hora_atual:
            raise forms.ValidationError("A hora precisa de ser maior que a atual")
        return hora_termino

class CreateTable(ModelForm):
    parqueid = ParqueModelChoiceField(label="Parque", queryset=Parque.objects.all(), required=True, widget=forms.Select(attrs={'class': 'field2'}))
    preco_por_hora = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    taxa_por_hora = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    taxa_noturna = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    taxa_da_multa = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    preco_contrato_dia = forms.FloatField(label="Preço do contrato/dia", widget=forms.NumberInput(attrs={'class': 'field1'}))
    preco_contrato_diurno = forms.FloatField(label="Preço do contrato diurno", widget=forms.NumberInput(attrs={'class': 'field1'}))
    preco_contrato_noturno = forms.FloatField(label="Preço do contrato noturno", widget=forms.NumberInput(attrs={'class': 'field1'}))

    class Meta:
        model = TabelaPrecos
        fields = ['parqueid', 'preco_por_hora', 'taxa_por_hora', 'taxa_noturna', 'taxa_da_multa', 'preco_contrato_dia', 'preco_contrato_diurno', 'preco_contrato_noturno']

    def clean_parqueid(self):
        parqueid = self.cleaned_data.get('parqueid')
        for instance in TabelaPrecos.objects.all():
            if instance.parqueid == parqueid:
                raise forms.ValidationError("Este parque já possuí uma tabela de preços. Selecione outro")
        return parqueid

    def clean_preco_por_hora(self):
        data = self.cleaned_data.get('preco_por_hora')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_taxa_por_hora(self):
        data = self.cleaned_data.get('taxa_por_hora')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_taxa_noturna(self):
        data = self.cleaned_data.get('taxa_noturna')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_taxa_da_multa(self):
        data = self.cleaned_data.get('taxa_da_multa')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data
    
    def clean_preco_contrato_dia(self):
        data = self.cleaned_data.get('preco_contrato_dia')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data
    
    def clean_preco_contrato_diurno(self):
        data = self.cleaned_data.get('preco_contrato_diurno')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_preco_contrato_noturno(self):
        data = self.cleaned_data.get('preco_contrato_noturno')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

class UpdateTable(ModelForm):
    preco_por_hora = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    taxa_por_hora = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    taxa_noturna = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    taxa_da_multa = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'field1'}))
    preco_contrato_dia = forms.FloatField(label="Preço do contrato/dia", widget=forms.NumberInput(attrs={'class': 'field1'}))
    preco_contrato_diurno = forms.FloatField(label="Preço do contrato diurno", widget=forms.NumberInput(attrs={'class': 'field1'}))
    preco_contrato_noturno = forms.FloatField(label="Preço do contrato noturno", widget=forms.NumberInput(attrs={'class': 'field1'}))

    class Meta:
        model = TabelaPrecos
        fields = ['preco_por_hora', 'taxa_por_hora', 'taxa_noturna', 'taxa_da_multa', 'preco_contrato_dia', 'preco_contrato_diurno', 'preco_contrato_noturno']

    def clean_parqueid(self):
        parqueid = self.cleaned_data.get('parqueid')
        for instance in TabelaPrecos.objects.all():
            if instance.parqueid == parqueid:
                raise forms.ValidationError("Este parque já possuí uma tabela de preços. Selecione outro")
        return parqueid

    def clean_preco_por_hora(self):
        data = self.cleaned_data.get('preco_por_hora')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_taxa_por_hora(self):
        data = self.cleaned_data.get('taxa_por_hora')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_taxa_noturna(self):
        data = self.cleaned_data.get('taxa_noturna')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_taxa_da_multa(self):
        data = self.cleaned_data.get('taxa_da_multa')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_preco_contrato_dia(self):
        data = self.cleaned_data.get('preco_contrato_dia')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data
    
    def clean_preco_contrato_diurno(self):
        data = self.cleaned_data.get('preco_contrato_diurno')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

    def clean_preco_contrato_noturno(self):
        data = self.cleaned_data.get('preco_contrato_noturno')
        if data < 0:
            raise forms.ValidationError("O valor necessita ser positivo")
        return data

class MatriculaForm(forms.Form):
    matricula = forms.CharField(widget=forms.TextInput(attrs={'class': 'field1'}))

    class Meta:
        model = Viatura
        fields = ['matricula']

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")

        v = Viatura.objects.filter(matricula=matricula).count()

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        if v == 0:
            raise forms.ValidationError("Não existe nenhuma reserva com a matrícula introduzida")

        return matricula
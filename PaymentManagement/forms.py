from django import forms

from AdminManagement.models import Lugar
from .models import Contrato, Dia, Fatura, Pagamento, Periodicidade, Reclamacao, TabelaPrecos        
import datetime
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

class ParqueModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nome

class LugarModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.numero_do_lugar

class ContratoForm(forms.ModelForm):
    CHOICES_Dias = (('Segunda-Feira', 'Segunda-Feira'),('Terça-Feira', 'Terça-Feira'), ('Quarta-Feira', 'Quarta-Feira'), ('Quinta-Feira', 'Quinta-Feira'), ('Sexta-Feira', 'Sexta-Feira'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo'))
    CHOICES_Periodicidade=(('diário', 'Todos os dias'), ('semanal', 'Escolher Dias: '))
    CHOICES_Horario=(('24H', '24H'), ('diurno', '8-20H'), ('noturno', '20-8H'))
    user=None
    OPTIONS_lugar = Lugar.makeOptions()
    periodicidade = forms.ChoiceField(choices=CHOICES_Periodicidade, widget=forms.RadioSelect(attrs={'class': 'radioF'}), required=True)
    dias = forms.MultipleChoiceField(choices=CHOICES_Dias, widget=forms.SelectMultiple(attrs={'class': 'multipleF'}), required=False)
    horario = forms.ChoiceField(choices=CHOICES_Horario, widget=forms.Select(attrs={'class': 'selectF'}), required=True)
    data_de_inicio = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'dateF'}))
    data_de_termino = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'dateF'}))
    lugar = LugarModelChoiceField(label="Lugar", queryset=Lugar.objects.filter(reservaid__isnull=True).filter(contratoid__isnull=True), required=True)
    matricula = forms.CharField(label="Matrícula", widget=forms.TextInput(attrs={'class': 'textF'}), required=True)
    class Meta:
        model = Contrato
        fields = [
            'data_de_inicio',
            'data_de_termino',
            'periodicidade',
            'dias',
            'horario',
            'lugar',
            'matricula',
        ]

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.user = kwargs.pop('current_user', None)
            self.parque = kwargs.pop('parque', None)
        super().__init__(*args, **kwargs)
        if self.instance.id is not None:
            dias = Dia.objects.filter(periodicidadeid=self.instance.periodicidadeid)
            self.fields['periodicidade'].initial = self.instance.periodicidadeid.periodicidade
           
            self.fields['horario'].initial = self.instance.periodicidadeid.horario
            days = list()
            for dia in dias:
                days.append(dia.nome)
            self.fields["dias"].initial = tuple(days)
            self.fields["lugar"].queryset = Lugar.objects.filter(reservaid__isnull=True).filter(contratoid__isnull=True)|Lugar.objects.filter(contratoid=self.instance.id)
            self.fields["lugar"].initial = Lugar.objects.filter(contratoid=self.instance.id)
	    
    def clean_data_de_inicio(self):
        data = self.cleaned_data.get('data_de_inicio')
        if data < datetime.date.today():
            raise forms.ValidationError("A data precisa de ser depois de hoje")
        return data

    def clean_dias(self):
        if self.cleaned_data.get('periodicidade') == "semanal" and (len(self.cleaned_data.get('dias')))<1:
            raise forms.ValidationError("Tem de selecionar pelo menos um dia no contrato semanal")
        return self.cleaned_data.get('dias')

    def clean_data_de_termino(self):
        data_inicio = self.cleaned_data.get('data_de_inicio')
        if data_inicio == None:
            data_inicio = datetime.date.min
        data_fim = self.cleaned_data.get('data_de_termino')
        if data_fim <= data_inicio:
            raise forms.ValidationError("A data de fim precisa de ser maior que a de inicio")
        return data_fim

    def save(self, contratoID = None):
        
        if contratoID is not None:
            newContrato = Contrato.objects.get(id=contratoID)
        else:
            newContrato = Contrato()
            newContrato.parqueid = self.parque
		
        
        newContrato.clienteid = self.user
        newPeriodicidade = Periodicidade()
        newPeriodicidade.horario = self.cleaned_data.get('horario')
        newPeriodicidade.periodicidade = self.cleaned_data.get('periodicidade')
        newPeriodicidade.save()
        if self.cleaned_data.get('periodicidade') == "semanal":
            print(self.cleaned_data.get('dias'))
            for i in self.cleaned_data.get('dias'):
                print(i)
                newDia = Dia()
                newDia.periodicidadeid = newPeriodicidade
                newDia.nome = i
                newDia.save()
        newContrato.periodicidadeid = newPeriodicidade
        newContrato.data_de_inicio = self.cleaned_data.get('data_de_inicio')
        newContrato.data_de_termino = self.cleaned_data.get('data_de_termino')
        newContrato.matricula = self.cleaned_data.get('matricula')
        newContrato.save()
        for i in self.cleaned_data.get('lugar'):
            i.contratoid = newContrato
            i.save()
        newPayment = Pagamento()
        newPayment.contratoid = newContrato
        newPayment.estado_do_pagamento = "Pendente"
        newPayment.montante = TabelaPrecos.getPrice(contrato = newContrato, all=False)
        newPayment.data_de_vencimento = self.cleaned_data.get('data_de_inicio') + datetime.timedelta(days = 7)
        newPayment.save()

class PaymentModelForm(forms.ModelForm):
    cc_number = CardNumberField(label='Número do Cartão')
    cc_expiry = CardExpiryField(label='Data de Expiração')
    cc_code = SecurityCodeField(label='CVV/CVC')
    class Meta:
        model = Pagamento
        fields = [
            'cc_number',
            'cc_expiry',
            'cc_code',
        ]

class ReclamacaoModelForm(forms.ModelForm):
    reclamacao = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'placeholder':'Escreva aqui a sua reclamação'}),
        required=True
        )
    
    class Meta:
        model = Reclamacao
        fields = [
            'reclamacao'
        ]

class PaymentProveModelForm(forms.ModelForm):
    comprovativo = forms.FileField()
    
    class Meta:
        model = Pagamento
        fields = [
            'comprovativo'
        ]

class FaturaModelForm(forms.ModelForm):
    nomeEmpresa = forms.CharField()
    moradaEmpresa = forms.CharField()
    nifEmpresa = forms.IntegerField()

    class Meta:
        model = Fatura
        fields = [
            'nomeEmpresa',
            'moradaEmpresa',
            'nifEmpresa'
        ]
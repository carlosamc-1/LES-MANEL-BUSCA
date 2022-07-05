from django import forms
from django.core.exceptions import ValidationError
import re

from django.utils import timezone

from AdminManagement.models import Lugar, Parque
from PaymentManagement.models import Reclamacao

from .models import TabelaMatriculas
from .models import RegistoMovimento, Viatura


class EntrarParqueForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]
        v = Viatura.objects.filter(matricula=matricula)

        if RegistoMovimento.objects.filter(matricula=matricula, data_de_saida=None).count() != 0:
            raise ValidationError("Matrícula já existe no parque.")

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')

        i = 0;
        length = len(t)
        for formato in t:
            i = i + 1
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)

            if pattern.match(matricula) is None and i < length:
                continue
            elif i == length and pattern.match(matricula) is None:
                raise ValidationError("Matrícula com formato incorreto.")
            else:
                break

        return matricula


class SairParqueForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]
        if RegistoMovimento.objects.filter(matricula=matricula, data_de_saida=None).count()==0:
            raise ValidationError("Não se encontra dentro do parque")

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        if not matricula:
            raise ValidationError("Matrícula não existe.")

        t = TabelaMatriculas.objects.values_list('formato')

        i = 0;
        length = len(t)
        for formato in t:
            i = i + 1
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)

            if pattern.match(matricula) is None and i < length:
                continue
            elif i == length and pattern.match(matricula) is None:
                raise ValidationError("Matrícula com formato incorreto.")
            else:
                break

        return matricula

class AssociarLugarForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all(), widget=forms.Select)

    def __init__(self, zona, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lugar"].queryset = Lugar.objects.filter(zonaid=zona, estado="Disponível")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')

        i = 0;
        length = len(t)
        for formato in t:
            i = i + 1
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)

            if pattern.match(matricula) is None and i < length:
                continue
            elif i == length and pattern.match(matricula) is None:
                raise ValidationError("Matrícula com formato incorreto.")
            else:
                break

        return matricula

    def clean_lugar(self):
        lugar = self.cleaned_data["lugar"]

        return lugar


class DesassociarLugarForm(forms.Form):
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all(), widget=forms.Select)

    def __init__(self, zona, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lugar"].queryset = Lugar.objects.filter(zonaid=zona, estado="Ocupado")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')

        i = 0;
        length = len(t)
        for formato in t:
            i = i + 1
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)

            if pattern.match(matricula) is None and i < length:
                continue
            elif i == length and pattern.match(matricula) is None:
                raise ValidationError("Matrícula com formato incorreto.")
            else:
                break

        return matricula

    def clean_lugar(self):
        lugar = self.cleaned_data["lugar"]

        return lugar

class ReclamacaoForm(forms.Form):
    reclamacao = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'size': '100', 'placeholder':'Escreva aqui a sua reclamação'}),
        required=True, label="Reclamação"
        )
    registo = forms.ModelChoiceField(queryset=RegistoMovimento.objects.all(), widget=forms.Select)

    def __init__(self, fatura, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = fatura.pagamentoid
        r = p.registoid
        self.fields["registo"].queryset = RegistoMovimento.objects.filter(matricula=r.matricula)

    def clean_reclamacao(self):
        reclamacao = self.cleaned_data["reclamacao"]

        return reclamacao

    def clean_registo(self):
        registo = self.cleaned_data["registo"]

        return registo


class RegistoMovimentoModelForm(forms.ModelForm):
    matricula = forms.CharField(max_length=120, required=True, label="Matrícula")
    data_de_entrada = forms.DateTimeField(required=True, label="Data de entrada")
    data_de_saida = forms.DateTimeField(required=False, label="Data de saída")
    provas = forms.CharField(max_length=120, required=False)

    def __init__(self, registo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["matricula"].initial = registo.matricula
        self.fields["data_de_entrada"].initial = registo.data_de_entrada
        self.fields["data_de_saida"].initial = registo.data_de_saida
        self.fields["provas"].initial = registo.provas

    class Meta:
        model = RegistoMovimento
        fields = [
            'matricula',
            'data_de_entrada',
            'data_de_saida',
            'provas']

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')

        i = 0;
        length = len(t)
        for formato in t:
            i = i + 1
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)

            if pattern.match(matricula) is None and i < length:
                continue
            elif i == length and pattern.match(matricula) is None:
                raise ValidationError("Matrícula com formato incorreto.")
            else:
                break

        return matricula

    def clean_data_de_entrada(self):
        data_de_entrada = self.cleaned_data["data_de_entrada"]

        return data_de_entrada

    def clean_data_de_saida(self):
        data_de_saida = self.cleaned_data["data_de_saida"]
        data_de_entrada = self.cleaned_data["data_de_entrada"]

        if data_de_saida < data_de_entrada:
            raise ValidationError("Data de saída é inferior à data de entrada.")

        return data_de_saida

    def clean_provas(self):
        provas = self.cleaned_data["provas"]

        return provas
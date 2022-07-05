from django import forms
from .models import Parque, Zona, Lugar

class ParqueModelFormCreate(forms.ModelForm):
    nome = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'field'}),
        required=True
        )
    capacidade = forms.IntegerField(
        min_value=10,
        initial=10,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        required=True
        )
    zonas = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        required=True
        )
    morada = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'field'}),
        required=True
        )
    cidade = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'field'}),
        required=True
        )
    codigo_postal = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        required=True
        )
    foto = forms.ImageField(
        required=True
    )

    class Meta:
        model = Parque
        fields = [
            'nome',
            'capacidade',
            'zonas',
            'morada',
            'cidade',
            'codigo_postal',
            'foto'
        ]

    def clean_morada(self):
        morada = self.cleaned_data.get("morada")

        if ("Rua" in morada):
            return morada
        elif ("rua" in morada):
            return morada
        elif ("Avenida" in morada):
            return morada
        elif ("avenida" in morada):
            return morada
        elif ("estrada" in morada):
            return morada
        elif ("Estrada" in morada):
            return morada
        elif ("mansão" in morada):
            return morada
        elif ("Mansão" in morada):
            return morada
        elif ("urbanização" in morada):
            return morada
        elif ("Urbanização" in morada):
            return morada
        else:
            raise forms.ValidationError("A morada é inválida.")

    def clean_cidade(self):
        cidade = self.cleaned_data.get("cidade")
        print(cidade)

        if ((cidade=="Aveiro")):
            return cidade
        
        elif ((cidade=="Beja")):
            return cidade
        
        elif ((cidade=="Braga")):
            return cidade

        elif ((cidade=="Bragança")):
            return cidade

        elif ((cidade=="Castelo Branco")):
            return cidade
        
        elif ((cidade=="Coimbra")):
            return cidade
        
        elif ((cidade=="Évora")):
            return cidade
        
        elif ((cidade=="Faro")):
            return cidade

        elif ((cidade=="Guarda")):
            return cidade

        elif ((cidade=="Leiria")):
            return cidade

        elif ((cidade=="Lisboa")):
            return cidade

        elif ((cidade=="Portalegre")):
            return cidade

        elif ((cidade=="Porto")):
            return cidade

        elif ((cidade=="Santarém")):
            return cidade

        elif ((cidade=="Setúbal")):
            return cidade

        elif ((cidade=="Viana do Castelo")):
            return cidade

        elif ((cidade=="Vila Real")):
            return cidade

        elif ((cidade=="Viseu")):
            return cidade

        else:
            raise forms.ValidationError("Insira um dos 16 distritos de Portugal Continental.")

    def clean_codigo_postal(self):
        cidade = self.cleaned_data.get("cidade")
        codigo_postal = self.cleaned_data.get("codigo_postal")

        if ((cidade=="Aveiro") and (codigo_postal != 3800)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Aveiro. Quereria dizer 3800?")
        
        elif ((cidade=="Beja") and (codigo_postal != 7800)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Beja. Quereria dizer 7800?")
        
        elif ((cidade=="Braga") and (codigo_postal != 4700)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Braga. Quereria dizer 4700?")
        
        elif ((cidade=="Bragança") and (codigo_postal != 5300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Bragança. Quereria dizer 5300?")

        elif ((cidade=="Castelo Branco") and (codigo_postal != 6000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Castelo Branco. Quereria dizer 6000?")
        
        elif ((cidade=="Coimbra") and (codigo_postal != 3000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Coimbra. Quereria dizer 3000?")
        
        elif ((cidade=="Évora") and (codigo_postal != 7000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Évora. Quereria dizer 7000?")
        
        elif ((cidade=="Faro") and (codigo_postal != 8000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Faro. Quereria dizer 8000?")

        elif ((cidade=="Guarda") and (codigo_postal != 6300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Guarda. Quereria dizer 6300?")

        elif ((cidade=="Leiria") and (codigo_postal != 2400)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Leiria. Quereria dizer 2400?")

        elif ((cidade=="Lisboa") and (codigo_postal<1000 or codigo_postal>1900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Lisboa. Quereria dizer 1000 a 1900?")

        elif ((cidade=="Portalegre") and (codigo_postal != 7300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Portalegre. Quereria dizer 7300?")

        elif ((cidade=="Porto") and (codigo_postal<4000 or codigo_postal>4300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade do Porto. Quereria dizer 4000 a 4300?")

        elif ((cidade=="Santarém") and (codigo_postal != 2000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Santarém. Quereria dizer 2000?")

        elif ((cidade=="Setúbal") and (codigo_postal != 2900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Setúbal. Quereria dizer 2900?")

        elif ((cidade=="Viana do Castelo") and (codigo_postal != 4900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Viana do Castelo. Quereria dizer 4900?")

        elif ((cidade=="Vila Real") and (codigo_postal != 5000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Vila Real. Quereria dizer 5000?")

        elif ((cidade=="Viseu") and (codigo_postal != 3500)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Viseu. Quereria dizer 3500?")

        else:
            return codigo_postal

class ParqueModelForm(forms.ModelForm):
    nome = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'field'}),
        required=True
        )
    capacidade = forms.IntegerField(
        min_value=10,
        initial=10,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        required=True
        )
    zonas = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        required=True
        )
    estado = forms.ChoiceField(
        choices=Parque.make_options(),
        widget=forms.Select(attrs={'class':'field2'}),
        required=True
        )
    morada = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'field'}),
        required=True
        )
    cidade = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'field'}),
        required=True
        )
    codigo_postal = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        required=True
        )
    foto = forms.ImageField(
        required=True
    )

    class Meta:
        model = Parque
        fields = [
            'nome',
            'capacidade',
            'zonas',
            'estado',
            'morada',
            'cidade',
            'codigo_postal',
            'foto'
        ]

    def clean_morada(self):
        morada = self.cleaned_data.get("morada")

        if ("Rua" in morada):
            return morada
        elif ("rua" in morada):
            return morada
        elif ("Avenida" in morada):
            return morada
        elif ("avenida" in morada):
            return morada
        elif ("estrada" in morada):
            return morada
        elif ("Estrada" in morada):
            return morada
        elif ("mansão" in morada):
            return morada
        elif ("Mansão" in morada):
            return morada
        elif ("urbanização" in morada):
            return morada
        elif ("Urbanização" in morada):
            return morada
        else:
            raise forms.ValidationError("A morada é inválida.")

    def clean_cidade(self):
        cidade = self.cleaned_data.get("cidade")
        print(cidade)

        if ((cidade=="Aveiro")):
            return cidade
        
        elif ((cidade=="Beja")):
            return cidade
        
        elif ((cidade=="Braga")):
            return cidade

        elif ((cidade=="Bragança")):
            return cidade

        elif ((cidade=="Castelo Branco")):
            return cidade
        
        elif ((cidade=="Coimbra")):
            return cidade
        
        elif ((cidade=="Évora")):
            return cidade
        
        elif ((cidade=="Faro")):
            return cidade

        elif ((cidade=="Guarda")):
            return cidade

        elif ((cidade=="Leiria")):
            return cidade

        elif ((cidade=="Lisboa")):
            return cidade

        elif ((cidade=="Portalegre")):
            return cidade

        elif ((cidade=="Porto")):
            return cidade

        elif ((cidade=="Santarém")):
            return cidade

        elif ((cidade=="Setúbal")):
            return cidade

        elif ((cidade=="Viana do Castelo")):
            return cidade

        elif ((cidade=="Vila Real")):
            return cidade

        elif ((cidade=="Viseu")):
            return cidade

        else:
            raise forms.ValidationError("Insira um dos 16 distritos de Portugal Continental.")

    def clean_codigo_postal(self):
        cidade = self.cleaned_data.get("cidade")
        codigo_postal = self.cleaned_data.get("codigo_postal")

        if ((cidade=="Aveiro") and (codigo_postal != 3800)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Aveiro. Quereria dizer 3800?")
        
        elif ((cidade=="Beja") and (codigo_postal != 7800)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Beja. Quereria dizer 7800?")
        
        elif ((cidade=="Braga") and (codigo_postal != 4700)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Braga. Quereria dizer 4700?")
        
        elif ((cidade=="Bragança") and (codigo_postal != 5300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Bragança. Quereria dizer 5300?")

        elif ((cidade=="Castelo Branco") and (codigo_postal != 6000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Castelo Branco. Quereria dizer 6000?")
        
        elif ((cidade=="Coimbra") and (codigo_postal != 3000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Coimbra. Quereria dizer 3000?")
        
        elif ((cidade=="Évora") and (codigo_postal != 7000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Évora. Quereria dizer 7000?")
        
        elif ((cidade=="Faro") and (codigo_postal != 8000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Faro. Quereria dizer 8000?")

        elif ((cidade=="Guarda") and (codigo_postal != 6300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Guarda. Quereria dizer 6300?")

        elif ((cidade=="Leiria") and (codigo_postal != 2400)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Leiria. Quereria dizer 2400?")

        elif ((cidade=="Lisboa") and (codigo_postal<1000 or codigo_postal>1900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Lisboa. Quereria dizer 1000 a 1900?")

        elif ((cidade=="Portalegre") and (codigo_postal != 7300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Portalegre. Quereria dizer 7300?")

        elif ((cidade=="Porto") and (codigo_postal<4000 or codigo_postal>4300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade do Porto. Quereria dizer 4000 a 4300?")

        elif ((cidade=="Santarém") and (codigo_postal != 2000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Santarém. Quereria dizer 2000?")

        elif ((cidade=="Setúbal") and (codigo_postal != 2900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Setúbal. Quereria dizer 2900?")

        elif ((cidade=="Viana do Castelo") and (codigo_postal != 4900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Viana do Castelo. Quereria dizer 4900?")

        elif ((cidade=="Vila Real") and (codigo_postal != 5000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Vila Real. Quereria dizer 5000?")

        elif ((cidade=="Viseu") and (codigo_postal != 3500)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Viseu. Quereria dizer 3500?")

        else:
            return codigo_postal



class ZonaModelForm(forms.ModelForm):
    numero_da_zona = forms.IntegerField(
        required=True,
        initial=1,
        widget=forms.TextInput(attrs={'class': 'field1'}),
        min_value=1,
        )
    lugares = forms.IntegerField(
        required=True,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        min_value=1,
        )
    tipo_de_zona = forms.ChoiceField(
        choices=Zona.make_options(),
        widget=forms.Select(attrs={'class':'field2'}),
        required=True
        )

    class Meta:
        model = Zona
        fields = [
            'numero_da_zona',
            'lugares',
            'tipo_de_zona'
        ]



class LugarModelForm(forms.ModelForm):
    numero_do_lugar = forms.IntegerField(
        required=True,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        min_value=1,
        )
    estado = forms.ChoiceField(
        choices=Lugar.make_options(),
        widget=forms.Select(attrs={'class':'field2'}),
        required=True
        )

    class Meta:
        model = Lugar
        fields = [
            'numero_do_lugar',
            'estado'
        ]

class LugarModelFormCreate(forms.ModelForm):
    numero_do_lugar = forms.IntegerField(
        required=True,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'field1'}),
        min_value=1,
        )

    class Meta:
        model = Lugar
        fields = [
            'numero_do_lugar',
        ]

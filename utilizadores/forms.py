from django.forms import ModelForm
from .models import Cliente, Funcionario, Utilizador, Administrador
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.forms import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordResetForm

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        return email



USER_CHOICES = (
    ("Utilizador", "Todos os Utilizadores"),
    ("Cliente", "Clientes"),
    ("Funcionario", "Funcionários"),

)

ESTADOS = (
    ("", "Todos os Estados"),
    ("T", "Confirmado"),
    ("F", "Pendente"),
    ("R", "Rejeitado"),
)




class UtilizadorFiltro(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES,
        widget=Select(),
        required=False,
    )

    filtro_estado = ChoiceField(
        choices=ESTADOS,
        widget=Select(),
        required=False,
    )


class ClienteRegisterForm(UserCreationForm):

    class Meta:
        model = Cliente
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'contacto', 'nif', 'morada', 'data_de_nascimento')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])


class AdministradorRegisterForm(UserCreationForm):

    class Meta:
        model = Administrador
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'contacto')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])

class FuncionarioRegisterForm(UserCreationForm):

    class Meta:
        model = Funcionario
        fields = ('username', 'password1', 'password2', 'email',
                  'first_name', 'last_name', 'contacto', 'funcao')

    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        erros = []
        if email == "" or first_name=="" or last_name=="" or username==None:
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

        if username and User.objects.filter(username=username).exists():
            erros.append(forms.ValidationError(f'O username já existe'))

        
        if password1==None or password2==None:
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            if password1==None:
                raise forms.ValidationError(f'Todos os campos são obrigatórios!')
            else:
                erros.append(forms.ValidationError(f'As palavras-passe não correspondem'))


        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(f'O email já existe')
        elif email==None:
            erros.append(forms.ValidationError(f'O email é inválido'))

        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])



class LoginForm(AuthenticationForm):
    username=CharField(widget=TextInput(attrs={'class':'input','style':''}), label="Nome de Utilizador", max_length=255, required=False)
    password=CharField(widget=PasswordInput(attrs={'class':'input1','style':''}), label= 'Senha', max_length=255, required=False)



class AlterarPasswordForm(PasswordChangeForm):
    old_password=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label="Senha Antiga", max_length=255, required=False)
    new_password1=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label="Senha Nova", max_length=255, required=False)
    new_password2=CharField(widget=PasswordInput(attrs={'class':'input','style':''}), label="Confirmação da Senha Nova", max_length=255, required=False)

class RecuperarPasswordForm(Form):
    email=CharField(widget=EmailInput(attrs={'class':'input','style':''}), label="Email", max_length=255, required=False)




class ClienteAlterarPerfilForm(ModelForm):

    class Meta:
        model = Cliente
        fields = ('email',
                  'first_name', 'last_name', 'contacto', 'nif', 'morada', 'data_de_nascimento')

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        erros = []
        if email == "" or first_name=="" or last_name=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')
        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])


class AdministradorAlterarPerfilForm(ModelForm):

    class Meta:
        model = Administrador
        fields = ('email',
                  'first_name', 'last_name', 'contacto')

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        erros = []
        if email == "" or first_name=="" or last_name=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')
        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])

class FuncionarioAlterarPerfilForm(ModelForm):

    class Meta:
        model = Funcionario
        fields = ('email',
                  'first_name', 'last_name', 'contacto', 'funcao')

    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        contacto = self.cleaned_data.get('contacto')
        erros = []
        if email == "" or first_name=="" or last_name=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')
        
        if contacto==None:
            erros.append(forms.ValidationError(f'Preencha corretamente o contacto'))    
        if len(erros)>0:
            raise ValidationError([erros])
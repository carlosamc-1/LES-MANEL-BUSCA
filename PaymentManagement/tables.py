import django_tables2 as django_tables
from .models import Contrato, Fatura
from django.utils.html import format_html
from django.urls import reverse


class ContratosTable(django_tables.Table):
    #Se aparecer um traco meter empty_values
    parque = django_tables.Column(accessor="parque", verbose_name="Parque", empty_values=())
    data_de_inicio = django_tables.Column('Data de Início')
    data_de_termino = django_tables.Column('Data de Término')
    periodicidade = django_tables.Column('Periodicidade' ,empty_values=())
    validade = django_tables.Column('Validade' ,empty_values=())
    # ver = django_tables.LinkColumn('contrato:contrato-detail', text='View', args=['record.id'])
    acoes = django_tables.TemplateColumn(verbose_name='Ações', template_name='acoes.html')

    class Meta:
        model = Contrato
        # sequence = ('nome', 'email', 'contacto', 'tipo', 'valido', 'acoes')
        fields = ('parque', 'data_de_inicio', 'data_de_termino', 'periodicidade', 'validade', 'acoes')
    
    def render_parque(self, record):
        return record.parqueid.nome
    
    def render_periodicidade(self, record):
        return record.periodicidadeid.periodicidade
    
    def render_validade(self, record):
        if record.valido:
            return "Válido"
        else:
            return "Inválido"

class FaturasTable(django_tables.Table):
    #Se aparecer um traco meter empty_values
    # ver = django_tables.LinkColumn('contrato:contrato-detail', text='View', args=['record.id'])
    nomeEmpresa = django_tables.Column('Nome da Empresa')
    moradaEmpresa = django_tables.Column('Morada da Empresa')

    class Meta:
        model = Fatura
        # sequence = ('nome', 'email', 'contacto', 'tipo', 'valido', 'acoes')
        fields = ('id','nomeEmpresa', 'moradaEmpresa')

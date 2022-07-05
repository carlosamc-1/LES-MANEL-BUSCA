import django_tables2 as tables
from django.utils.html import format_html
from django_tables2.utils import A
from django.urls import reverse
from PaymentManagement.models import Reserva, TabelaPrecos

class ReservaTable(tables.Table):
    parque = tables.Column(accessor="parque", verbose_name="Parque", empty_values=())
    matricula = tables.Column(accessor="matricula", verbose_name="Matrícula", empty_values=())
    Editar = tables.LinkColumn('ReserveManagement:update', text='Editar', args=[A('id')])
    Apagar = tables.LinkColumn('ReserveManagement:delete', text='Apagar', args=[A('id')])
    class Meta:
        model = Reserva
        fields = ('parque', 'matricula', 'data_de_inicio', 'data_de_termino', 'hora_de_inicio', 'hora_de_termino')

    def render_parque(self, record):
        return record.parqueid.nome

    def render_matricula(self, record):
        return record.viaturaid.matricula

class TabelaTable(tables.Table):
    parque = tables.Column(accessor="parque", verbose_name="Parque", empty_values=())
    Editar = tables.LinkColumn('ReserveManagement:update_table', text='Editar', args=[A('id')])
    Apagar = tables.LinkColumn('ReserveManagement:delete_table', text='Apagar', args=[A('id')])

    class Meta:
        model = TabelaPrecos
        fields = ('parque', 'preco_por_hora', 'taxa_por_hora', 'taxa_noturna', 'taxa_da_multa', 'preco_contrato_dia', 'preco_contrato_diurno', 'preco_contrato_noturno')

    def render_parque(self, record):
        return record.parqueid.nome
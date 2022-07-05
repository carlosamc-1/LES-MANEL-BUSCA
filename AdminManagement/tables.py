import django_tables2 as tables
from django_tables2.utils import A
from .models import Parque, Zona, Lugar

class ParqueTable(tables.Table):
#     _ = tables.LinkColumn('AdminManagement:parque-detail', text='Ver Mais', args=[A('id')])
#     class Meta:
#         model = Parque
#         fields = ("nome", "capacidade", "zonas", "estado", "morada", "cidade", "codigo_postal" )

# class ZonaTable(tables.Table):
#     _ = tables.TemplateColumn(template_name="table_zona.html")
#     class Meta:
#         model = Zona
#         fields = ("numero_da_zona", "lugares", "tipo_de_zona")

# class LugarTable(tables.Table):
#     _ = tables.TemplateColumn(template_name="table_lugar.html")
#     class Meta:
#         model = Lugar
#         fields = ("numero_do_lugar", "estado")

    Info = tables.LinkColumn('AdminManagement:parque-detail', text='Ver Mais', args=[A('id')])
    class Meta:
        model = Parque
        fields = ("nome", "capacidade", "zonas", "estado", "morada", "cidade", "codigo_postal" )

class ZonaTable(tables.Table):
    Info = tables.TemplateColumn(template_name="table_zona.html")
    class Meta:
        model = Zona
        fields = ("numero_da_zona", "lugares", "tipo_de_zona")

class LugarTable(tables.Table):
    Info = tables.TemplateColumn(template_name="table_lugar.html")
    class Meta:
        model = Lugar
        fields = ("numero_do_lugar", "estado")
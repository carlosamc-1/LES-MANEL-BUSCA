import django_filters
from .models import Contrato, Fatura
from django.db.models import Q

get_valido_choices = [
    ('True', 'Confirmado'),
    ('False', 'Por confirmar'),
    ('Rejeitado', 'Rejeitado'),
]


def filter_nome(queryset, name, value):
    for term in value.split():
        queryset = queryset.filter(Q(first_name__icontains=term)
                                   | Q(last_name__icontains=term))
    return queryset


class ContratosFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(method=filter_nome)
    valido = django_filters.MultipleChoiceFilter(choices=get_valido_choices)

    class Meta:
        model = Contrato
        fields = '__all__'

class FaturasFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(method=filter_nome)
    valido = django_filters.MultipleChoiceFilter(choices=get_valido_choices)

    class Meta:
        model = Fatura
        fields = '__all__'

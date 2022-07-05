from email import message
from pickle import NONE
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse


from .models import *
from .forms import *
from .tables import *
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters.views import FilterView
from .filters import ReservaFilter

def homepage(request):
    return render(request, "main/homepage.html", {"reservas": Reserva.objects.all})

def create(request):
    if request.POST:
        form = CreateReserve(request.POST)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = CreateReserve()


    return render(request, "main/create.html", {"form": form})

class ReadListView(SingleTableView):
    model = Reserva
    table_class = ReservaTable
    template_name = 'main/read.html'

    def read(request):
        table = ReservaTable(Reserva.objects.all())
        return render(request, 'main/read.html', {'table': table})

def read_matricula(request):
    if request.method == "POST": 
        form = MatriculaForm(request.POST)  
        if form.is_valid():
            return redirect("ReserveManagement:read_user_table", matricula = form.cleaned_data.get("matricula"))
    else:
        form = MatriculaForm()

    return render(request, "main/read_user.html", context={"form": form})        

class TableListView(SingleTableMixin, FilterView):
    table_class = ReservaTable
    template_name = 'main/read.html'
    filterset_class = ReservaFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        context[self.get_context_table_name(table)] = table
        return context
    
    def get_table_data(self):       
        ola = self.kwargs['matricula']
        if ola == None:
            messages.error(self.request, 'Esta reserva ainda se encontra ativa')
        else:
            try:
                matricula=Viatura.objects.get(matricula=ola)
            except:
                matricula=None
            reserva = Reserva.objects.filter(viaturaid=matricula)
        return reserva
    

def delete(request, reserva_id):
    reserva = Reserva.objects.get(pk=reserva_id)
    data = reserva.data_de_inicio
    if request.method == "POST":
        if request.method == "POST" and data < datetime.date.today():
            reserva.delete()
            return redirect("homepage")
        else:
            messages.error(request, 'Esta reserva ainda se encontra ativa')
    
    return render(request, "main/delete.html", {'reserva': reserva})

def update(request, reserva_id):
    reserva = Reserva.objects.get(pk=reserva_id)
    form = CreateReserve(request.POST or None, instance=reserva)
    if form.is_valid():
        form.save()
        return redirect("homepage")
    return render(request, 'main/update.html', {'reserva': reserva, 'form':form})

def createTable(request):
    if request.POST:
        form = CreateTable(request.POST)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = CreateTable()

    return render(request, "main/create_table.html", {"form": form})

def readTable(request):
    tabelas = TabelaPrecos.objects.all()
    table = TabelaTable(TabelaPrecos.objects.all())
    return render(request, 'main/read_table.html', {'tabelas': tabelas, 'table': table})

def deleteTable(request, tabela_id):
    tabela = TabelaPrecos.objects.get(pk=tabela_id)
    if request.method == "POST":
        tabela.delete()
        return redirect("homepage")
    return render(request, "main/delete_table.html", {'tabela': tabela})

def updateTable(request, tabela_id):
    tabela = TabelaPrecos.objects.get(pk=tabela_id)
    form = UpdateTable(request.POST or None, instance=tabela)
    if form.is_valid():
        form.save()
        return redirect("../read_table")
    return render(request, 'main/update_table.html', {'tabela': tabela, 'form':form})





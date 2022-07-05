import datetime
import random
import string
from django.urls import reverse
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import SingleTableMixin, SingleTableView
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage

from AdminManagement.models import Lugar, Parque
from OperationManagement.models import RegistoMovimento
from utilizadores.models import Cliente
from .models import Reserva, TabelaPrecos
from django.contrib.auth import *
from .models import Contrato, Dia, Fatura, Pagamento, Reclamacao
from .forms import ContratoForm, FaturaModelForm, PaymentModelForm, ReclamacaoModelForm
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, 
    TemplateView, 
    View,
    )

from .tables import ContratosTable, FaturasTable
from django_filters.views import FilterView
from .filters import ContratosFilter, FaturasFilter
from django.db.models import F
from django.template import loader

#LISTAR OS CONTRATOS
class ContratoListView(SingleTableMixin, FilterView):
    table_class = ContratosTable
    template_name = 'contratos.html'
    filterset_class = ContratosFilter
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
        if self.request.user.is_staff == 1:
            contratos=Contrato.objects.all()
        else:
            try:
                cliente=Cliente.objects.get(pk=get_user(self.request))
            except:
                cliente=None
            contratos=Contrato.objects.filter(clienteid=cliente)
        return contratos

        
    
#CONSULTAR CONTRATO
def contrato_detail_view(request, id):
    contrato=Contrato.objects.get(id=id)
    lugar=Lugar.objects.get(contratoid=contrato)
    dias=Dia.objects.filter(periodicidadeid=contrato.periodicidadeid)
    template = loader.get_template('detail.html')
    context ={
        'contrato': contrato,
        'lugar':lugar,
        'dias':dias,
    }
    return HttpResponse(template.render(context, request))

#APAGAR CONTRATO
def contrato_delete_view(request, id):
    contrato=Contrato.objects.get(id=id)
    lugar = Lugar.objects.get(contratoid=contrato)
    if request.POST:
        contrato.delete()
        oldLugar = lugar
        oldLugar.contratoid=None
        oldLugar.save()
        return redirect('../../')
    template = loader.get_template('delete_confirmation.html')
    context ={
        "contrato": contrato,
    }
    return HttpResponse(template.render(context, request))

#LISTAR PARQUES
def contrato_parque_view(request):
    parques = Parque.objects.all()
    template = loader.get_template('parque.html')
    context ={
        'parques': parques,
    }
    return HttpResponse(template.render(context, request))

#CRIAR CONTRATO
def contrato_create_view(request, id):
    if request.method=='POST':
        form = ContratoForm(request.POST, current_user=Cliente.objects.get(utilizador_ptr_id=request.user.id), parque=Parque.objects.get(id=id))
        if form.is_valid():
            form.save()
            contrato = Contrato.objects.latest("id")
            pagamento = Pagamento.objects.get(contratoid=contrato.id)
            return redirect(reverse('PaymentManagement:contrato-pay-options', kwargs={ 'id': contrato.id, 'payid': pagamento.id}))
    else:
        form = ContratoForm(current_user=Cliente.objects.get(utilizador_ptr_id=request.user.id))
    context ={
        'form': form,
        'user': request.user,
    }
    return render(request, "create.html", context)

#EDITAR CONTRATO
def contrato_update_view(request, id):
    obj=get_object_or_404(Contrato, id=id)
    form = ContratoForm(request.POST or None, current_user=Cliente.objects.get(id=1), instance=obj)
    if form.is_valid():
        form.save(id)
        contrato = Contrato.objects.latest("id")
        return redirect(reverse('PaymentManagement:contrato-pay', kwargs={ 'id': contrato.id }))
    context ={
        'form': form,
    }
    return render(request, "create.html", context)


#APROVAR CONTRATO
def contrato_validate_aprove_view(request, id):
    contrato=Contrato.objects.get(id=id)
    contrato.valido = True
    contrato.save()
    return redirect('../../..')

#DESAPROVAR CONTRATO
def contrato_validate_desaprove_view(request, id):
    contrato=Contrato.objects.get(id=id)
    contrato.valido = False
    contrato.save()
    return redirect('../../..')


#CONSULTAR PAGAMENTOS
class payment_view(ListView):
    template_name = 'pagamentos.html'
    queryset = Pagamento.objects.all()
    faturas = Fatura.objects.values_list("pagamentoid", flat=True)

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset, "faturas": self.faturas}
        return render(request, self.template_name, context)

#PAGAMENTO EFETUADO COM SUCESSO
class SuccessView(TemplateView):
    template_name = "success.html"


#PAGAMENTO CANCELADO
class CancelView(TemplateView):
    template_name = "cancel.html"

class FaturaListView(SingleTableMixin, FilterView):
    table_class = FaturasTable
    template_name = 'fatura_list.html'
    filterset_class = FaturasFilter
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
        if self.request.user.is_staff == 1:
            faturas= Fatura.objects.all()
        else:
            try:
                cliente = Fatura.objects.get(pk=get_user(self.request))
            except:
                cliente=None
            faturas = Fatura.objects.filter(clienteid=cliente)
        return faturas

class FaturaDeleteView(DeleteView):
    template_name = 'fatura_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Fatura, id=id_)

    def get_success_url(self):
        return '../../'

#CONSULTAR CONTRATO
def fatura_detail_view(request, id):
    fatura=Fatura.objects.get(id=id)
    if fatura.pagamentoid.contratoid is not None and fatura.pagamentoid.estado_do_pagamento=="Pago":
        faturarecibo=False
        recibo=fatura
        fatura=False
    elif fatura.pagamentoid.contratoid is not None:
        faturarecibo=False
        recibo=False
        fatura=fatura
    else:
        faturarecibo=fatura
        recibo=False
        fatura=False

    template = loader.get_template('fatura_detail.html')
    context ={
        'fatura': fatura,
        'faturarecibo': faturarecibo,
        'recibo': recibo,
    }
    return HttpResponse(template.render(context, request))

class ReclamacaoListView(View):
    template_name = 'reclamacao_list.html'
    queryset = Reclamacao.objects.all()

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset}
        return render(request, self.template_name, context)

class ReclamacaoCreateView(CreateView):
    template_name = 'reclamacao_create.html'
    form_class = ReclamacaoModelForm
    model = Reclamacao

    def form_valid(self, form):
        reclamacao = form.save(commit=False)
        reclamacao.faturaid = Fatura.objects.get(id=self.kwargs["id"])
        reclamacao.save()
        return redirect("../../")

    def get_success_url(self):
        return '../'

def payment_prove_create_view(request, id):
    if request.method == "POST":
        pagamento = Pagamento.objects.get(id=id)
        # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
                # save attached file
    
                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                file = fs.save(request_file.name, request_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)
                pagamento.comprovativo = request_file
                pagamento.save()
    
    return render(request, "payment_prove.html")

def payment_create_view(request, id, payid):
    contrato = Contrato.objects.get(id = id)
    price = TabelaPrecos.getPrice(contrato = contrato, all=False)
    if request.method=='POST':
        form = PaymentModelForm(request.POST)
        
        payment = Pagamento.objects.get(id = payid)
        if form.is_valid():
            payment.estado_do_pagamento = "Pago"
            payment.montante = price
            payment.save()
            return redirect('../')
    else:
        form = PaymentModelForm()
        contrato = Contrato.objects.get(id = id)
    context ={
        'form': form,
        'price': price,
    }
    return render(request, "payment.html", context)

# def contrato_payment_create_view():


def payment_create_view_reference(request, id, payid):
    S = 9  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    randomNum = ''.join(random.choices(string.digits, k = S))    
    reference = ' '.join([randomNum[i:i+3] for i in range(0, len(randomNum), 3)])
    entidade = 11111
    pagamento=Pagamento.objects.get(id = payid)
    template = loader.get_template('reference.html')
    context ={
        'referencia': reference,
        'entidade':entidade,
        'montante':pagamento.montante,
    }
    return HttpResponse(template.render(context, request))

def reserva_payment_create_view(request, id):
    reserva = Reserva.objects.get(id = id)
    payment = Pagamento.objects.get(reservaid=reserva)
    if request.method=='POST':
        form = PaymentModelForm(request.POST)   
        if form.is_valid():
            payment.data_de_vencimento = datetime.datetime.now()
            payment.estado_do_pagamento = "Pago"
            payment.save()
            registo = RegistoMovimento.objects.get(id = reserva.viaturaid.registo_movimentoid.id)
            registo.data_de_saida = datetime.datetime.now()
            registo.save()
            fatura = Fatura()
            fatura.clienteid = Cliente.objects.get(id=request.user.id)
            fatura.pagamentoid = payment
            fatura.save()
            return redirect("PaymentManagement:fatura-detail", id=fatura.id)
    else:
        form = PaymentModelForm()

    
    context ={
        'form': form,
        'price': payment.montante,
    }
    return render(request, "payment.html", context)

def registo_payment_create_view(request, id):
    registo = RegistoMovimento.objects.get(id = id)
    payment = Pagamento.objects.get(registoid=registo)
    if request.method=='POST':
        form = PaymentModelForm(request.POST)
        if form.is_valid():
            payment.data_de_vencimento = datetime.datetime.now()
            payment.estado_do_pagamento = "Pago"
            payment.save()
            registo.data_de_saida = datetime.datetime.now()
            registo.save()
            fatura = Fatura()
            fatura.pagamentoid = payment
            fatura.save()
            return redirect("PaymentManagement:fatura-detail", id=fatura.id)
    else:
        form = PaymentModelForm()

    
    context ={
        'form': form,
        'price': payment.montante,
    }
    return render(request, "payment.html", context)

class OptionsView(TemplateView):
    template_name = "options.html"

def payment_options_view(request, id, payid):
    template = loader.get_template('pay_options.html')
    context ={
        'id': id,
        'payid': payid,
    }
    return HttpResponse(template.render(context, request))


def emit_fatura_view(request, id):
    payment=Pagamento.objects.get(id=id)
    newFatura = Fatura()
    newFatura.nomeEmpresa = "Parques Lda."
    newFatura.moradaEmpresa = "Faro"
    newFatura.nifEmpresa = 987654321
    newFatura.clienteid = Cliente.objects.get(id=1)
    newFatura.pagamentoid = payment
    newFatura.save()
    return redirect('../../')

class ProcessFaturaView(UpdateView):
    template_name = 'fatura_create.html'
    form_class = FaturaModelForm
    queryset = Fatura.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Fatura, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return '../../'
import random

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View

from AdminManagement.models import Lugar, Parque, Zona
from PaymentManagement.models import Fatura, Reclamacao, Pagamento, Contrato, Reserva, TabelaPrecos
from .forms import AssociarLugarForm, DesassociarLugarForm, EntrarParqueForm, ReclamacaoForm, RegistoMovimentoModelForm, SairParqueForm

from .models import RegistoMovimento, Viatura


# Create your views here.

def entrar_parque(request):
    return render(request=request,
                  template_name="main/entrar_parque.html",
                  context={"parques": Parque.objects.all()})


def entrar_parque_form(request, parque_id):
    parques = Parque.objects.get(pk=parque_id)
    if request.method == "POST":
        form = EntrarParqueForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Entrou no parque com sucesso.")
            r = RegistoMovimento(data_de_entrada=timezone.now(), matricula=form.cleaned_data.get("matricula"), parqueid=parques)
            r.save()
            if Viatura.objects.filter(matricula=form.cleaned_data.get("matricula")).count() == 0:
                v = Viatura(registo_movimentoid=r, matricula=form.cleaned_data.get("matricula"))
                v.save()

            return redirect("homepage")
    else:
        form = EntrarParqueForm

    return render(request,
                  "main/entrar_parque_form.html",
                  context={"form": form, "parques": parques})


def index(request, parque_id):
    parque= Parque.objects.get(pk=parque_id)
    zonas = Zona.objects.filter(parqueid=parque)
    lugares = Lugar.objects.all()
    faturas = Fatura.objects.all()
    reclamacoes = Reclamacao.objects.all()

    return render(request=request,
                  template_name="main/index.html",
                  context={"parque": parque, "zonas": zonas, "lugares": lugares, "faturas": faturas, "reclamacoes": reclamacoes})


# Ver isto melhor
def sair_parque_form(request, parque_id):
    parques = Parque.objects.get(pk=parque_id)
    if request.method == "POST":
        form = SairParqueForm(request.POST)
        if form.is_valid():
            viatura = Viatura.objects.get(matricula=form.cleaned_data.get("matricula"))
            contrato = Contrato.objects.filter(matricula=form.cleaned_data.get("matricula"))
            try:
                reserva = Reserva.objects.get(viaturaid=viatura)
            except:
                reserva=None
            r = RegistoMovimento.objects.get(matricula=form.cleaned_data.get("matricula"), data_de_saida=None)
            if contrato.exists():
                if r is not None:
                    r.data_de_saida = timezone.now()
                    r.save()
                return redirect("OperationManagement:entrar_parque")
            elif reserva != None:
                pagamento = Pagamento()
                pagamento.reservaid = reserva
                pagamento.estado_do_pagamento = "Pendente"
                pagamento.montante = TabelaPrecos.getPrice(reserva = reserva, all=False)
                pagamento.save()
                return redirect("PaymentManagement:reserva-pay", id=reserva.id)
            else:
                pagamento = Pagamento()
                pagamento.registoid = viatura.registo_movimentoid
                pagamento.estado_do_pagamento = "Pendente"
                pagamento.montante = TabelaPrecos.getPrice(registo = r, all=False)
                pagamento.save()
                return redirect("PaymentManagement:registo-pay", id=viatura.registo_movimentoid.id)
            
    else:
        form = SairParqueForm

    return render(request,
                  "main/sair_parque_form.html",
                  context={"form": form, "parques": parques})


def ver_lugares(request, parque_id, zona_id):
    parque = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(parqueid=parque, numero_da_zona=zona_id)
    lugares = Lugar.objects.filter(zonaid=zona)

    return render(request,
                  "main/ver_lugares.html",
                  context={"parque": parque, "zona": zona, "lugares": lugares})

def ocupar_lugar(request, parque_id, zona_id, lugar_id):
    parque = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(parqueid=parque, numero_da_zona=zona_id)
    lugares = Lugar.objects.none()
    lugares |= Lugar.objects.filter(zonaid=zona)

    lugares_disponiveis = lugares.filter(estado="Disponivel")
    if not lugares_disponiveis:
        messages.error(request, f"Não existem lugares disponíveis no parque.")
        return redirect("OperationManagement:index", parque_id=parque_id)

    lugar = Lugar.objects.get(numero_do_lugar=lugar_id)
    lugar.estado = "Ocupado"
    lugar.save()

    messages.success(request, f"Ocupou o lugar no parque.")

    return redirect("OperationManagement:ver_lugares", parque_id=parque_id, zona_id=zona_id)


def liberar_lugar(request, parque_id, zona_id, lugar_id):
    parque = Parque.objects.get(pk=parque_id)
    zonas = Zona.objects.filter(parqueid=parque)
    lugares = Lugar.objects.none()
    for zona in zonas:
        lugares |= Lugar.objects.filter(zonaid=zona)

    lugares_ocupados = lugares.filter(estado="Ocupado")
    if not lugares_ocupados:
        messages.error(request, f"Não existem lugares ocupados no parque.")
        return redirect("OperationManagement:index", parque_id=parque_id)

    lugar = Lugar.objects.get(numero_do_lugar=lugar_id)
    lugar.estado = "Disponivel"
    lugar.save()

    messages.success(request, f"Liberou o lugar no parque.")

    return redirect("OperationManagement:ver_lugares", parque_id=parque_id, zona_id=zona_id)


def associar_lugar(request, parque_id, zona_id):
    parques = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(numero_da_zona=zona_id)
    if request.method == "POST":
        form = AssociarLugarForm(zona, request.POST)
        if form.is_valid():

            messages.success(request, f"Associou o lugar com sucesso.")
            l = form.cleaned_data.get("lugar")
            m = form.cleaned_data.get("matricula")
            v = Viatura.objects.get(matricula=m)
            l.viaturaid = v
            l.save()

            return redirect("OperationManagement:index", parque_id=parque_id)
    else:
        form = AssociarLugarForm(zona)

    return render(request,
                  "main/associar_lugar.html",
                  context={"form": form, "parques": parques})


def desassociar_lugar(request, parque_id, zona_id):
    parques = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(numero_da_zona=zona_id)
    if request.method == "POST":
        form = DesassociarLugarForm(zona, request.POST)
        if form.is_valid():
            messages.success(request, f"Desassociou o lugar com sucesso.")

            l = form.cleaned_data.get("lugar")
            l.viaturaid = None
            l.save()

            return redirect("OperationManagement:index", parque_id=parque_id)
    else:
        form = DesassociarLugarForm(zona)

    return render(request,
                  "main/desassociar_lugar.html",
                  context={"form": form, "parques": parques})


def reclamar_fatura(request, parque_id, fatura_id):
    parques = Parque.objects.get(pk=parque_id)
    fatura = Fatura.objects.get(id=fatura_id)

    if request.method == "POST":
        form = ReclamacaoForm(fatura, request.POST)
        if form.is_valid():
            messages.success(request, f"Fez a reclamação com sucesso.")

            rec = Reclamacao(faturaid=fatura)
            rec.reclamacao = form.cleaned_data.get("reclamacao")
            rec.registo_movimentoid = form.cleaned_data.get("registo")
            rec.save()

            return redirect("OperationManagement:index", parque_id=parque_id)
    else:
        form = ReclamacaoForm(fatura)

    return render(request=request,
                  template_name="main/reclamar_fatura.html",
                  context={"form": form, "parques": parques, "fatura": fatura})


def processar_reclamacao(request, parque_id, reclamacao_id):
    parques = Parque.objects.get(pk=parque_id)
    reclamacao = Reclamacao.objects.get(id=reclamacao_id)
    registo = reclamacao.registo_movimentoid
    v = Viatura.objects.get(matricula=registo.matricula)
    fatura = reclamacao.faturaid

    if request.method == 'POST':
        form = RegistoMovimentoModelForm(registo, request.POST)
        if form.is_valid():

                # fatura.delete()
                registo.matricula = form.cleaned_data.get("matricula")
                v.matricula = form.cleaned_data.get("matricula")
                registo.data_de_entrada = form.cleaned_data.get("data_de_entrada")
                registo.data_de_saida = form.cleaned_data.get("data_de_saida")
                registo.provas = form.cleaned_data.get("provas")
                registo.save()

                # Criar nova fatura com dados novos de movimento

                return redirect('OperationManagement:index', parque_id=parque_id)
    else:
        form = RegistoMovimentoModelForm(registo)

    return render(request=request,
              template_name="main/processar_reclamacao.html",
              context={"parques": parques, "form": form, "reclamacao": reclamacao})

def sair_parque(request):
    return render(request=request,
                  template_name="main/sair_parque.html",
                  context={"parques": Parque.objects.all()})


def operar_parque(request):
    return render(request=request,
                  template_name="main/operar_parque.html",
                  context={"parques": Parque.objects.all()})

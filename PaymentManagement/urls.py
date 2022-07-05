from django.urls import path, include
from . import models, views

app_name = "PaymentManagement"
urlpatterns = [
    #GESTAO DE CONTRATOS
    path('', views.OptionsView.as_view(), name='options'), #consultar contratos
    path('contrato/', views.ContratoListView.as_view(), name='contrato-list'), #consultar contratos
    path('contrato/<int:id>/', views.contrato_detail_view, name="contrato-detail"), #vista detalhada de um contrato
    path('contrato/criar/', views.contrato_parque_view, name="contrato-parque"), #Escolher parque para criar contrato
    path('contrato/criar/<int:id>', views.contrato_create_view, name="contrato-create"), #dados para criar contrato
    path('contrato/<int:id>/editar/', views.contrato_update_view, name="contrato-update"), #editar o contrato
    path('contrato/<int:id>/apagar/', views.contrato_delete_view, name="contrato-delete"), #cancelar o contrato
    path('contrato/<int:id>/validar/aprovar/', views.contrato_validate_aprove_view, name="contrato-validate-aprove"), #validar o contrato (aprovar)
    path('contrato/<int:id>/validar/cancelar/', views.contrato_validate_desaprove_view, name="contrato-validate-desaprove"), #validar o contrato (cancelar)

    #GESTAO DE FATURACAO
    path('reserva/<int:id>/pagar/', views.reserva_payment_create_view, name="reserva-pay"), #efetuar pagamento reserva
    path('registo/<int:id>/pagar/', views.registo_payment_create_view, name="registo-pay"), #efetuar pagamento registo
    # path('contrato/<int:id>/pagar/', views.contrato_payment_create_view, name="contrato-pay"), #efetuar pagamento registo
    path('contrato/<int:id>/pagar/<int:payid>/', views.payment_options_view, name="contrato-pay-options"), #dados de pagamento para contrato
    path('contrato/<int:id>/pagar/<int:payid>/cartao', views.payment_create_view, name="contrato-pay-card"), #dados de pagamento para contrato
    path('contrato/<int:id>/pagar/<int:payid>/referencia', views.payment_create_view_reference, name="contrato-pay-reference"), #dados de pagamento para contrato
    path('fatura/', views.FaturaListView.as_view(), name="fatura"), #consultar faturas
    path('fatura/<int:id>/', views.fatura_detail_view, name="fatura-detail"), #consultar faturas
    path('pagamento/<int:id>/emitir/', views.emit_fatura_view, name="fatura-emit"), #emitir fatura
    path('pagamento/', views.payment_view.as_view(), name="payment"), #consultar pagamentos
    path('pagamento/<int:id>/comprovar/', views.payment_prove_create_view, name="payment-prove"), #comprovar pagamento
    path('reclamacao/', views.ReclamacaoListView.as_view(), name='reclamacao-list'), #consultar reclamacoes
    path('fatura/<int:id>/reclamar/', views.ReclamacaoCreateView.as_view(), name="fatura-reclam"), #reclamar fatura
    path('fatura/<int:id>/cancelar/', views.FaturaDeleteView.as_view(), name="fatura-cancel"), #cancelar fatura
    path('fatura/<int:id>/processar/', views.ProcessFaturaView.as_view(), name="fatura-process"), #processar fatura
]

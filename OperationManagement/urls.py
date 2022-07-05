from django.urls import path

from . import views

app_name = "OperationManagement"

urlpatterns = [
    path("", views.entrar_parque, name="entrar_parque"),
    path("entrar_parque_form/<int:parque_id>/", views.entrar_parque_form, name="entrar_parque_form"),
    path("index/<int:parque_id>/", views.index, name="index"),
    path("sair_parque_form/<int:parque_id>/", views.sair_parque_form, name="sair_parque_form"),
    path("ocupar_lugar/<int:parque_id>/<int:zona_id>/<int:lugar_id>/", views.ocupar_lugar, name="ocupar_lugar"),
    path("liberar_lugar/<int:parque_id>/<int:zona_id>/<int:lugar_id>/", views.liberar_lugar, name="liberar_lugar"),
    path("associar_lugar/<int:parque_id>/<int:zona_id>/", views.associar_lugar, name="associar_lugar"),
    path("desassociar_lugar/<int:parque_id>/<int:zona_id>/", views.desassociar_lugar, name="desassociar_lugar"),
    path("ver_lugares/<int:parque_id>/<int:zona_id>/", views.ver_lugares, name="ver_lugares"),
    path("operar_parque/", views.operar_parque, name="operar_parque"),
    path("sair_parque/", views.sair_parque, name="sair_parque"),

    path("reclamar_fatura/<int:parque_id>/<int:fatura_id>/", views.reclamar_fatura, name="reclamar_fatura"),
    path("processar_reclamacao/<int:parque_id>/<int:reclamacao_id>", views.processar_reclamacao, name="processar_reclamacao"),

]
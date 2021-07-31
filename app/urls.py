from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    # # # # # # # # # # # # SYSTEMS URL # # # # # # # # # # # # #

    path('doisg', views.doisg, name='doisg'),
    path('umts', views.umts, name='umts'),
    path('lte', views.lte, name='lte'),
    path('cincoG', views.cincoG, name='cincoG'),
    path('wifi', views.wifi, name='wifi'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # PROPAGACAO ESPACO LIVRE # # # # # # # # # # # #

    path('espaco_livre', views.espaco_livre, name='espaco_livre'),

    path('calculadora_potencia_recebida',
        views.calculadora_potencia_recebida,
        name="calculadora_potencia_recebida"),

    path('calculadora_atenuacao_espaço_livre',
        views.calculadora_atenuacao_espaço_livre,
        name="calculadora_atenuacao_espaço_livre"),

    path('calculadora_potencia_recebida_reflexao',
        views.calculadora_potencia_recebida_reflexao,
        name="calculadora_potencia_recebida_reflexao"),

    path('grafico_a0_espaco_livre',
        views.grafico_a0_espaco_livre,
        name="grafico_a0_espaco_livre"),

    path('grafico_pr_espaco_livre',
        views.grafico_pr_espaco_livre,
        name="grafico_pr_espaco_livre"),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # PROPAGACAO OKUMURA-HATA # # # # # # # # # # # #

    path('okumurahata', views.okumurahata, name='okumurahata'),

    path('okumura_hata_calculadora_meio_urbano_pequena',
        views.okumura_hata_calculadora_meio_urbano_pequena,
        name="okumura_hata_calculadora_meio_urbano_pequena"),

    path('okumura_hata_calculadora_meio_urbano_grande',
        views.okumura_hata_calculadora_meio_urbano_grande,
        name="okumura_hata_calculadora_meio_urbano_grande"),

    path('okumura_hata_calculadora_meio_suburbano',
        views.okumura_hata_calculadora_meio_suburbano,
        name="okumura_hata_calculadora_meio_suburbano"),

    path('okumura_hata_calculadora_meio_rural',
        views.okumura_hata_calculadora_meio_rural,
        name="okumura_hata_calculadora_meio_rural"),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # PROPAGACAO WALFISCH-IKEGAMI # # # # # # # # # #

    path('walfischikegami', views.walfischikegami, name='walfischikegami'),

    path('walfisch_ikegami_media', views.walfisch_ikegami_media, name='walfisch_ikegami_media'),

    path('walfisch_ikegami_metropolitana', views.walfisch_ikegami_metropolitana, name='walfisch_ikegami_media'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # #  INTERFERENCIA CO-CANAL # # # # # # # # # # #

    path('interferencia_cocanal', views.interferencia_cocanal, name='interferencia_cocanal'),

    path('calculadora_interferencia_cocanal', views.calculadora_interferencia_cocanal, name='calculadora_interferencia_cocanal'),

    path('calculadora_interferencia_cocanal_trisetorial', views.calculadora_interferencia_cocanal_trisetorial, name='calculadora_interferencia_cocanal_trisetorial'),

    path('calculadora_cluster_minima', views.calculadora_cluster_minima, name='calculadora_cluster_minima'),

    path('grafico_interferencia_cocanal', views.grafico_interferencia_cocanal, name='grafico_interferencia_cocanal'),



    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # # # # # # # # #  TRAFEGO E SERVICOS # # # # # # # # # # #

    path('trafego', views.trafego, name='trafego'),

    path('calculadora_probabilidade_bloqueio', views.calculadora_probabilidade_bloqueio, name='calculadora_probabilidade_bloqueio'),

    path('calculadora_numero_canais', views.calculadora_numero_canais, name='calculadora_numero_canais'),

    path('calculadora_de_trafego_oferecido', views.calculadora_de_trafego_oferecido, name='calculadora_de_trafego_oferecido'),

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




]

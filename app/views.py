from django.shortcuts import render
from django.http import HttpResponse

#from django.http import HttpResponse
from django.template import loader
from math import log10
from matplotlib import pyplot as plt

import base64
from io import BytesIO

from .functions import *

def index(request):
    #return HttpResponse("INDEX")
    return render(request, "index.html")

# # # # # # # # # # # # # # # # # # # # # # # # # #

### SISTEMAS ###
def doisg(request):
    #return HttpResponse("GSM")
    return render(request,"sistemas/gsm.html")

def umts(request):
    #return HttpResponse("UMTS")
    return render(request,"sistemas/umts.html")

def lte(request):
    #return HttpResponse("LTE")
    return render(request,"sistemas/lte.html")

def cincoG(request):
    #return HttpResponse("5G")
    return render(request,"sistemas/cincog.html")

def wifi(request):
    #return HttpResponse("WIFI")
    return render(request,"sistemas/wifi.html")

# # # # # # # # # # # # # # # # # # # # # # # # # #

### ESPACO LIVRE ###
def espaco_livre(request):
    #return HttpResponse("freeSpace")
    return render(request,"espaco_livre/espaco_livre.html")

def calculadora_potencia_recebida(request):

    try:

        potencia_emitida = float(request.POST['pe'])
        ganho_emissor = float(request.POST['ge'])
        ganho_recetor = float(request.POST['gr'])
        frequencia = float(request.POST['f'])
        distancia = float(request.POST['d'])

        atenuacao_0 = round(32.44 + 20*log10(distancia) + 20*log10(frequencia),2)
        potencia_recebida = round(potencia_emitida + ganho_emissor + ganho_recetor - atenuacao_0,2)

        return render(request,"espaco_livre/calculadora_potencia_recebida.html",
            {
                "potencia_emitida": formatar(potencia_emitida),
                "ganho_emissor": formatar(ganho_emissor),
                "ganho_recetor": formatar(ganho_recetor),
                "frequencia": formatar(frequencia),
                "distancia": formatar(distancia),
                "atenuacao_0": formatar(atenuacao_0),
                "potencia_recebida": formatar(potencia_recebida),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"espaco_livre/calculadora_potencia_recebida.html",{"erro": True})

def calculadora_potencia_recebida_reflexao(request):

    try:

        potencia_emitida = float(request.POST['pe'])
        ganho_emissor = float(request.POST['ge'])
        ganho_recetor = float(request.POST['gr'])
        distancia = float(request.POST['d'])
        he = float(request.POST['he'])
        hr = float(request.POST['hr'])
        n = float(request.POST['n'])

        potencia_recebida = round(-120 + potencia_emitida + ganho_emissor + ganho_recetor + 20 * log10(he) + 20 * log10(hr) - (n * 10) * log10(distancia) , 2)

        return render(request,"espaco_livre/calculadora_potencia_recebida_reflexao.html",
            {
                "potencia_emitida": formatar(potencia_emitida),
                "ganho_emissor": formatar(ganho_emissor),
                "ganho_recetor": formatar(ganho_recetor),
                "hr": formatar(hr),
                "he": formatar(he),
                "distancia": formatar(distancia),
                "potencia_recebida": formatar(potencia_recebida),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"espaco_livre/calculadora_potencia_recebida.html",{"erro": True})

def calculadora_atenuacao_espaço_livre(request):

    try:

        frequencia = float(request.POST['f'])
        distancia = float(request.POST['d'])

        atenuacao_0 = round(get_atenuacao_espaco_livre(distancia,frequencia),2)

        return render(request,"espaco_livre/calculadora_atenuacao_espaço_livre.html",
            {
                "frequencia": formatar(frequencia),
                "distancia": formatar(distancia),
                "atenuacao_0": formatar(atenuacao_0),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"espaco_livre/calculadora_atenuacao_espaço_livre.html",{"erro": True})

def grafico_a0_espaco_livre(request):

    try:

        frequencia = float(request.POST['f'])

        distancias = []
        it = 0

        while(it <= 100):
            distancias.append(it)
            it += 1

        atenuacoes = []

        for d in distancias:
            if(d == 0):
                atenuacoes.append(0)
            else:
                atenuacoes.append(
                    round(
                        get_atenuacao_espaco_livre(
                            d,
                            frequencia,
                        ),2
                    )
                )

        plt.plot(distancias, atenuacoes)
        plt.xlabel("Distância [km]")
        plt.ylabel("Atenuação [dB]")
        #plt.axhline(y=potencia_recebida, xmax=100, color='r', linestyle='-')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        plt.close()
        buffer.close()


        #abc += distancias.length()

        return render(request,"espaco_livre/grafico_a0_espaco_livre.html",
            {
                "frequencia": formatar(frequencia),
                'graph':graph,
                "erro": False
            })
    except ValueError:
        #Handle the exception
        return render(request,"espaco_livre/grafico_a0_espaco_livre.html",{"erro": True})

def grafico_pr_espaco_livre(request):

    try:

        potencia_emitida = float(request.POST['pe'])
        potencia_recebida = float(request.POST['pr'])
        ganho_emissor = float(request.POST['ge'])
        ganho_recetor = float(request.POST['gr'])
        frequencia = float(request.POST['f'])

        d_max = distancia_maxima(
                    potencia_recebida,
                    potencia_emitida,
                    frequencia,
                    ganho_emissor,
                    ganho_recetor
                )

        distancias = []
        it = 0

        while(it <= 100):
            distancias.append(it)
            it += 1

        potencias_recebidas = []

        for d in distancias:
            if(d == 0):
                potencias_recebidas.append(0)
            else:
                potencias_recebidas.append(
                    round(
                        get_potencia_recetor(
                            potencia_emitida,
                            ganho_emissor,
                            ganho_recetor,
                            frequencia,
                            d
                        ),2
                    )
                )

        plt.plot(distancias, potencias_recebidas)
        plt.axhline(y=potencia_recebida, xmax=100, color='r', linestyle='-')
        plt.xlabel("Distância [km]")
        plt.ylabel("Potência recebida [dB]")

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        plt.close()
        buffer.close()


        #abc += distancias.length()

        return render(request,"espaco_livre/grafico_espaco_livre.html",
            {
                "potencia_emitida": formatar(potencia_emitida),
                "ganho_emissor":formatar(ganho_emissor),
                "ganho_recetor": formatar(ganho_recetor),
                "frequencia":formatar(frequencia),
                "potencia_recebida":formatar(potencia_recebida),
                "d_max":formatar(round(d_max,2)),
                'graph':graph,
                "erro": False
            })
    except ValueError:
        #Handle the exception
        return render(request,"espaco_livre/grafico_espaco_livre.html",{"erro": True})

# # # # # # # # # # # # # # # # # # # # # # # # # #

### OKUMURA-HATA ###
def okumurahata(request):
    #return HttpResponse("okumurahata")
    return render(request,"okumura_hata/okumura_hata.html")

def okumura_hata_calculadora_meio_urbano_pequena(request):
    #return HttpResponse("okumurahata_pequena")
    try:
        hbe = float(request.POST['hbe'])
        hm = float(request.POST['hm'])
        frequencia = float(request.POST['f'])
        distancia = float(request.POST['d'])

        if (validar_okumura_hata(frequencia, distancia, hbe, hm)):

            coeficiente_correcao = 0.8 + (1.1 * log10(frequencia) - 0.7) * hm - 1.56 * log10(frequencia)
            print("CH1 = ")
            print(coeficiente_correcao)

            atenuacao = 69.55 + 26.16 * log10(frequencia) - 13.82 * log10(hbe) - coeficiente_correcao + (44.9 - 6.55 * log10(hbe)) * log10(distancia)

            atenuacao = round(atenuacao,2)

            return render(request,"okumura_hata/okumura_hata_calculadora_meio_urbano_pequena.html",
            {
                "atenuacao": formatar(atenuacao),
                "hbe": formatar(hbe),
                "hm": formatar(hm),
                "frequencia": formatar(frequencia),
                "distancia": formatar(distancia),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"okumura_hata/okumura_hata_calculadora_meio_urbano_pequena.html",
        {
            "erro": True,
            "msg": 'Erro! Valores inválidos para o modelo de Okumura-Hata.'
        })

def okumura_hata_calculadora_meio_urbano_grande(request):
    #return HttpResponse("okumurahata_urbana")
    try:
        hbe = float(request.POST['hbe'])
        hm = float(request.POST['hm'])
        frequencia = float(request.POST['f'])
        distancia = float(request.POST['d'])

        if (validar_okumura_hata(frequencia, distancia, hbe, hm)):

            if (frequencia >= 150 and frequencia <= 200):
                coeficiente_correcao = 8.29 * ((log10(1.54 * hm))**2) - 1.1

            else:
                coeficiente_correcao = 3.2 * ((log10(11.75 * hm))**2) - 4.97

            atenuacao = 69.55 + 26.16 * log10(frequencia) - 13.82 * log10(hbe) - coeficiente_correcao + (44.9 - 6.55 * log10(hbe)) * log10(distancia)

            atenuacao = round(atenuacao,2)

            return render(request,"okumura_hata/okumura_hata_calculadora_meio_urbano_grande.html",
            {
                "atenuacao": formatar(atenuacao),
                "hbe": formatar(hbe),
                "hm": formatar(hm),
                "frequencia": formatar(frequencia),
                "distancia": formatar(distancia),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"okumura_hata/okumura_hata_calculadora_meio_urbano_grande.html",
        {
            "erro": True,
            "msg": 'Erro! Valores inválidos para o modelo de Okumura-Hata.'
        })

def okumura_hata_calculadora_meio_suburbano(request):
    #return HttpResponse("okumurahata_sub_urbana")

    try:
        hbe = float(request.POST['hbe'])
        hm = float(request.POST['hm'])
        frequencia = float(request.POST['f'])
        distancia = float(request.POST['d'])

        if (validar_okumura_hata(frequencia, distancia, hbe, hm)):

            coeficiente_correcao = 0.8 + (1.1 * log10(frequencia) - 0.7) * hm - 1.56 * log10(frequencia)

            atenuacao = 69.55 + 26.16 * log10(frequencia) - 13.82 * log10(hbe) - coeficiente_correcao + (44.9 - 6.55 * log10(hbe)) * log10(distancia)

            atenuacao = atenuacao - 2 * ((log10(frequencia/28))**2) - 5.4

            atenuacao = round(atenuacao,2)

            return render(request,"okumura_hata/okumura_hata_calculadora_meio_suburbano.html",
            {
                "atenuacao": formatar(atenuacao),
                "hbe": formatar(hbe),
                "hm": formatar(hm),
                "frequencia": formatar(frequencia),
                "distancia": formatar(distancia),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"okumura_hata/okumura_hata_calculadora_meio_suburbano.html",
        {
            "erro": True,
            "msg": 'Erro! Valores inválidos para o modelo de Okumura-Hata.'
        })

def okumura_hata_calculadora_meio_rural(request):
    #return HttpResponse("okumurahata_pequena")
    try:
        hbe = round(float(request.POST['hbe']), 2)
        hm = round(float(request.POST['hm']), 2)
        frequencia = round(float(request.POST['f']), 2)
        distancia = round(float(request.POST['d']), 2)

        if (validar_okumura_hata(frequencia, distancia, hbe, hm)):

            coeficiente_correcao = 0

            if (frequencia >= 150 and frequencia <= 200):

                coeficiente_correcao = 8.29 * ((log10(1.54 * hm))**2) - 1.1

            else:
                coeficiente_correcao = 3.2 * ((log10(11.75 * hm))**2) - 4.97

            atenuacao = 69.55 + 26.16 * log10(frequencia) - 13.82 * log10(hbe) - coeficiente_correcao + (44.9 - 6.55 * log10(hbe)) * log10(distancia)

            atenuacao = atenuacao - 4.78 * ((log10(frequencia))**2) + 18.33 * log10(frequencia) - 40.94

            atenuacao = round(atenuacao,2)

            return render(request,"okumura_hata/okumura_hata_calculadora_meio_rural.html",
            {
                "atenuacao":atenuacao,
                "hbe":hbe,
                "hm":hm,
                "frequencia":frequencia,
                "distancia":distancia,
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"okumura_hata/okumura_hata_calculadora_meio_rural.html",
        {
            "erro": True,
            "msg": 'Erro! Valores inválidos para o modelo de Okumura-Hata.'
        })

# # # # # # # # # # # # # # # # # # # # # # # # # #

### WALFISCH-IKEGAMI ###
def walfischikegami(request):
    #return HttpResponse("okumurahata")
    return render(request,"walfisch_ikegami/walfisch_ikegami.html")

def walfisch_ikegami_media(request):
    #return HttpResponse("walfisch_ikegami_media")

    try:

        frequencia = float(request.POST['f'])
        andares = float(request.POST['a'])
        hbe = float(request.POST['hbe'])
        dist_edificios = float(request.POST['d'])
        distancia = float(request.POST['dist'])
        hm = float(request.POST['hm'])
        angulo = float(request.POST['angulo'])

        if (angulo == 0):
            atenuacao = 42.6 + 26 * log10(distancia) + 20 * log10(frequencia)

        else:
            kf = (frequencia/925 - 1) * 0.7 - 4

            altura_edificio = 3 * andares

            Lmsd = get_Lmsd(hbe, hm, altura_edificio, dist_edificios, frequencia, distancia, kf)

            Lori = get_Lori(angulo)

            Lrts = get_Ltrs(dist_edificios, frequencia, altura_edificio, hm, Lori)

            atenuacao = 32.4 + 20*log10(distancia) + 20*log10(frequencia) + Lrts + Lmsd

        atenuacao = round(atenuacao,2)

        return render(request,"walfisch_ikegami/walfisch_ikegami_media.html",
        {
            "atenuacao": formatar(atenuacao),
            "hbe": formatar(hbe),
            "hm": formatar(hm),
            "angulo": formatar(angulo),
            "dist_edificios": formatar(dist_edificios),
            "frequencia": formatar(frequencia),
            "distancia": formatar(distancia),
            "erro": False
        })

    except ValueError:
        #Handle the exception
        return render(request,"walfisch_ikegami/walfisch_ikegami_media.html",
        {
            "erro": True,
            "msg": 'Erro! Valores inválidos para o modelo de Walfisch - Ikegami.'
        })

def walfisch_ikegami_metropolitana(request):
    #return HttpResponse("walfisch_ikegami_metropolitana")

    try:

        frequencia = float(request.POST['f'])
        andares = float(request.POST['a'])
        hbe = float(request.POST['hbe'])
        dist_edificios = float(request.POST['d'])
        distancia = float(request.POST['dist'])
        hm = float(request.POST['hm'])
        angulo = float(request.POST['angulo'])

        if (angulo == 0):
            atenuacao = 42.6 + 26 * log10(distancia) + 20 * log10(frequencia)

        else:
            print(1)
            kf = (frequencia/925 - 1) * 1.5 - 4

            altura_edificio = 3 * andares

            Lmsd = get_Lmsd(hbe, hm, altura_edificio, dist_edificios, frequencia, distancia, kf)

            Lori = get_Lori(angulo)

            Lrts = get_Ltrs(dist_edificios, frequencia, altura_edificio, hm, Lori)

            atenuacao = 32.4 + 20*log10(distancia) + 20*log10(frequencia) + Lrts + Lmsd

        atenuacao = round(atenuacao,2)

        return render(request,"walfisch_ikegami/walfisch_ikegami_metropolitana.html",
        {
            "atenuacao": formatar(atenuacao),
            "hbe": formatar(hbe),
            "hm": formatar(hm),
            "angulo": formatar(angulo),
            "dist_edificios": formatar(dist_edificios),
            "frequencia": formatar(frequencia),
            "distancia": formatar(distancia),
            "erro": False
        })

    except ValueError:
        #Handle the exception
        return render(request,"walfisch_ikegami/walfisch_ikegami_metropolitana.html",
        {
            "erro": True,
            "msg": 'Erro! Valores inválidos para o modelo de Walfisch - Ikegami.'
        })

# # # # # # # # # # # # # # # # # # # # # # # # # #

### INTERFERERNCIA CO-CANAL ###
def interferencia_cocanal(request):
    #return HttpResponse("interferencia_cocanal")
    return render(request,"interferencia_cocanal/interferencia_cocanal.html")

def calculadora_interferencia_cocanal(request):
    try:

        n = float(request.POST['n'])
        ncp = float(request.POST['ncp'])

        interferencia = get_interferencia_cocanal(n,ncp)

        return render(request,"interferencia_cocanal/calculadora_interferencia_cocanal.html",
            {
                "interferencia": formatar(round(interferencia,2)),
                "ncp": formatar(round(ncp,2)),
                "n": formatar(round(n,2)),
                "rcc": formatar(round(sqrt(3*ncp),2)),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"interferencia_cocanal/calculadora_interferencia_cocanal.html",{"erro": True})

def calculadora_interferencia_cocanal_trisetorial(request):
    try:

        n = float(request.POST['n'])
        ncp = float(request.POST['ncp'])

        interferencia = get_interferencia_cocanal_trisectorial(n,ncp)

        return render(request,"interferencia_cocanal/calculadora_interferencia_cocanal_trisetorial.html",
            {
                "interferencia": formatar(round(interferencia,2)),
                "ncp": formatar(round(ncp,2)),
                "n":  formatar(round(n,2)),
                "rcc": formatar(round(sqrt(3*ncp),2)),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"interferencia_cocanal/calculadora_interferencia_cocanal_trisetorial.html",{"erro": True})

def calculadora_cluster_minima(request):
    try:
        interferencia = float(request.POST['c_i'])
        coeficiente_atenuacao = float(request.POST['n'])

        rcc = (6 * interferencia) ** (1/coeficiente_atenuacao)

        cluster_minima = (rcc**2)/3

        return render(request,"interferencia_cocanal/calculadora_cluster_minima.html",
            {
                "cluster_minima": formatar(round(cluster_minima,2)),
                "cluster_minima_round": formatar(round(cluster_minima)),
                "interferencia": formatar(round(interferencia,2)),
                "coeficiente_atenuacao": formatar(round(coeficiente_atenuacao,2)),
                "rcc": formatar(rcc),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"interferencia_cocanal/calculadora_cluster_minima.html",{"erro": True})

def grafico_interferencia_cocanal(request):
    try:

        interferencia_limite = float(request.POST['c_i'])

        lista_ncp = [3, 4, 7, 12, 13, 19]
        lista_n = [2, 3.3, 4]


        for n in lista_n[::-1]:
            lista_ci = []
            for ncp in lista_ncp:
                lista_ci.append(get_interferencia_cocanal(n, ncp))

            plt.bar(lista_ncp, lista_ci)
            plt.xlabel("Tamanho do cluster")
            plt.ylabel("C/I [dB]")
            plt.axhline(y=interferencia_limite, xmax=100, color='b', linestyle='-')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        plt.close()
        buffer.close()

        return render(request,"interferencia_cocanal/grafico_interferencia_cocanal.html",
            {
                "graph":graph,
                "interferencia_limite": formatar(interferencia_limite),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"interferencia_cocanal/grafico_interferencia_cocanal.html",{"erro": True})

# # # # # # # # # # # # # # # # # # # # # # # # # #

### TRAFEGO ###
def trafego(request):
    #return HttpResponse("trafego")
    return render(request,"trafego/trafego.html")

def calculadora_probabilidade_bloqueio(request):
    try:
        trafego = float(request.POST['trafego'])
        canais = float(request.POST['canais'])

        probabilidade = get_probabilidade_de_bloqueio(trafego,canais)

        return render(request,"trafego/calculadora_probabilidade_bloqueio.html",
            {
                "trafego": formatar(round(trafego,2)),
                "canais": formatar(round(canais,2)),
                "probabilidade": formatar(round(probabilidade,2)),
                "percentagem": formatar(round(probabilidade * 100,2)),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"trafego/calculadora_probabilidade_bloqueio.html",{"erro": True})

def calculadora_numero_canais(request):
    try:
        probabilidade = float(request.POST['pb'])
        trafego = float(request.POST['trafego'])

        canais = get_numero_de_canais(probabilidade,trafego)

        return render(request,"trafego/calculadora_numero_canais.html",
            {
                "trafego": formatar(trafego),
                "canais": formatar(canais),
                "probabilidade": formatar(probabilidade),
                "percentagem": formatar(probabilidade * 100),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"trafego/calculadora_de_trafego_oferecido.html",{"erro": True})

def calculadora_de_trafego_oferecido(request):
    try:
        probabilidade = float(request.POST['pb'])
        canais = float(request.POST['canais'])

        trafego = get_trafego_oferecido(probabilidade,canais)

        return render(request,"trafego/calculadora_de_trafego_oferecido.html",
            {
                "trafego": formatar(round(trafego,2)),
                "canais": formatar(round(canais,2)),
                "probabilidade": formatar(round(probabilidade,2)),
                "percentagem": formatar(round(probabilidade * 100,2)),
                "erro": False
            })

    except ValueError:
        #Handle the exception
        return render(request,"trafego/calculadora_de_trafego_oferecido.html",{"erro": True})

# # # # # # # # # # # # # # # # # # # # # # # # # #

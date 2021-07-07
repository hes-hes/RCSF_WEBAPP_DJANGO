from math import log10
from math import sqrt
from math import factorial


def distancia_maxima(
    potencia_recetor,
    potencia_emissor,
    frequencia,
    ganho_emissor,
    ganho_recetor):

    params = potencia_emissor + ganho_emissor + ganho_recetor - 32.44 - 20*log10(frequencia) - potencia_recetor
    
    return 10 ** (params/20)

def get_atenuacao_espaco_livre(distancia, frequencia):
    return round(32.44 + 20*log10(distancia) + 20*log10(frequencia),2) 

def get_potencia_recetor(
    potencia_emissor,
    ganho_emissor, 
    ganho_recetor, 
    frequencia, 
    distancia):

    potencia_recetor = potencia_emissor + ganho_emissor + ganho_recetor - 32.44 - 20*log10(distancia) - 20*log10(frequencia)
    
    return potencia_recetor

def validar_okumura_hata(frequencia, distancia, hbe, hm):
    if(
        (frequencia >= 150 and frequencia <= 1500) or
        (distancia >= 1 and distancia <= 20) or
        (hbe >= 30 and hbe <= 200) or
        (hm >= 1 and hm <= 10)
    ):
        return True
    
    return False

def validar_walfisch_ikegami(frequencia, distancia, hb, hm):
    if(
        (frequencia >= 800 and frequencia <= 2000) or
        (distancia >= 0.02 and distancia <= 5) or
        (hbe >= 4 and hbe <= 5) or
        (hm >= 1 and hm <= 3)
    ):
        return True
    
    return False

def get_Lmsd(hbe, hm, altura_edificio, dist_edificios, frequencia, distancia, kf):

    if(hbe > altura_edificio):
        print(11)
        kd = 18
        ka = 54
        Lbsh = -18 * log10(1 + (hbe - altura_edificio))

    elif(hbe <= altura_edificio):
        print(111)
        kd = 18 - 15 * ((hbe - altura_edificio)/(altura_edificio - hm))
        
        if (distancia >= 0.5):
            ka = 54 - 0.8*(hbe - altura_edificio)
        else:
            ka = 54 - 0.8*(hbe - altura_edificio)*(distancia/0.5)

    Lbsh = 0
    return Lbsh + ka + kd * log10(distancia) + kf * log10(frequencia) - 9 * log10(dist_edificios)

def get_Lori(angulo):
    if(angulo < 35 and angulo >= 0):
        return -10 + 0.354 * angulo
        
    if(angulo < 55 and angulo >= 35):  
        return 2.5 + 0.075 * (angulo - 35)

    elif(angulo < 90 and angulo >= 55): 
        return 4 + 0.114 * (angulo - 55)

def get_Ltrs(dist_edificios, frequencia, altura_edificio, hm, Lori):
    return -16.9 - 10 * log10(dist_edificios/2) + 10 * log10(frequencia) + 20 * log10(altura_edificio - hm) + Lori

def get_interferencia_cocanal(n,ncp):
    return 10 * log10((sqrt(3*ncp) ** n) / 6)

def get_interferencia_cocanal_trisectorial(n,ncp):
    rcc = sqrt(3 * ncp)
    return 10 * log10(1 / (rcc**(-n) + (rcc + 1/sqrt(2))**(-n)))

def get_probabilidade_de_bloqueio(trafego,canais):
    n = 0
    somatorio = 0

    while (n <= canais):
        somatorio += (trafego ** n)/factorial(n)
        n += 1
        
    return ((trafego ** canais)/factorial(canais))/somatorio

def get_trafego_oferecido(probabilidade_limite, canais):
    probailidade_obtida = -1
    trafego_teste = 0
    trafego = 0

    while(1):
        trafego_teste += 1
        probabilidade_teste = get_probabilidade_de_bloqueio(trafego_teste, canais)
        #print(p_corrente)
            
        if (probabilidade_teste > probailidade_obtida and 
            probabilidade_teste < probabilidade_limite):
            probailidade_obtida = probabilidade_teste
            trafego = trafego_teste
        else:
            return trafego
    
def get_numero_de_canais(probabilidade_limite, trafego):
    canais = 0 

    while(1):
        p = get_probabilidade_de_bloqueio(trafego, canais)
                        
        if(p > probabilidade_limite):
            canais += 1
        else:
            return canais

def formatar(val):
    if (val % 1 == 0):
        return int(val)
    
    return val
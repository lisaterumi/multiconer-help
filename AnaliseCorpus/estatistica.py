# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

#https://en.wikipedia.org/wiki/Data_analysis#Initial_data_analysis

def media(X):
    return sum(X)/len(X)


def variancia(X):
    M = media(X)
    return sum([(x-M)**2 for x in X])/len(X)
    
    
def desvio_padrao(X):
    return variancia(X)**0.5
    
    
def intervalo_confianca(X,confianca = 95): #em porcentagem
    from scipy import stats
    t = stats.t.ppf(1-(1-(confianca/100))/2, len(X)-1)
    intervalo_inferior = media(X)-t*desvio_padrao(X)/(len(X)**0.5)
    intervalo_superior = media(X)+t*desvio_padrao(X)/(len(X)**0.5)
    return intervalo_inferior,intervalo_superior
    
    
def quantidade_de_amostras_necessarias_para_intervalo_de_confianca(X,confianca =95,intervalo=1):
    from scipy import stats
    t = stats.t.ppf(1-(1-(confianca/100))/2, len(X)-1)
    return ((2*t*desvio_padrao(X))/(intervalo))**2    
    
    
arredonda_para_cima = lambda x : round(x+.5)


def quantil(X,Q):
    if Q > 1 or Q < 0:
        raise ValueError('Numero do Quantil Invalido!')
    Posicao = Q*len(X)
    if Posicao > int(Posicao):
        Posicao = arredonda_para_cima(Posicao)
    else:
        Posicao = int(Posicao)
    X = sorted(X)
    if len(X)%2 == 0: #par
        x1 = X[Posicao-1]
        x2 = X[Posicao]
        x = (x1+x2)/2
    else:
        x = X[Posicao-1]
    return {'Posição': Posicao,'Posição na Lista': Posicao-1,'x': x}

def mediana(X):
    return quantil(X,0.5)

def quartil(X,Q=2):
    if Q > 3 or Q < 1:
        raise ValueError('Numero do Quartil Invalido!')
    return quantil(X,0.25*int(Q))

def decil(X,D=5):
    if D > 10 or D < 1:
        raise ValueError('Numero do Decil Invalido!')
    return quantil(X,0.1*int(D))

def percentil(X,P=50):
    if P > 100 or P < 1:
        raise ValueError('Numero do Percentil Invalido!')
    return quantil(X,0.01*int(P))


def intervalo_confianca_variancia(X,confianca = 95): #em porcentagem
    from scipy.stats.distributions import chi2
    x1 = chi2.ppf(1-(1-(confianca/100))/2, df=(len(X)-1))
    x2 = chi2.ppf((1-(confianca/100))/2, df=(len(X)-1))
    intervalo_inferior = ((len(X)-1)*variancia(X))/x1
    intervalo_superior = ((len(X)-1)*variancia(X))/x2
    return intervalo_inferior,intervalo_superior


def intervalo_confianca_desvio_padrao(X,confianca = 95): #em porcentagem
    A,B = intervalo_confianca_variancia(X,confianca)
    return A**0.5,B**0.5


def covariancia(X,Y):
    if len(X) != len(Y):
        raise ValueError('Tamanho dos Dados Diferentes!')
    return (sum([X[i]*Y[i] for i in range(len(X))])-((sum(X)*sum(Y))/len(X)))/len(X)


def correlacao(X,Y):
    if len(X) != len(Y):
        raise ValueError('Tamanho dos Dados Diferentes!')
    return covariancia(X,Y)/(desvio_padrao(X)*desvio_padrao(Y))


def existe_correlacao_significante(X,Y,significancia=5):
    cor = correlacao(X,Y)
    T  = (cor)/(((1-(cor**2))/(len(X)-2))**0.5)
    t = stats.t.ppf(1-(1-((100-significancia)/100))/2, len(X)-2)
    if T > t:
        return True #Existe uma correlação significante
    else:
        return False #NAO existe uma correlação significante







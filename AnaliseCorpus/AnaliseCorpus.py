#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getQuantidadeSentencas(dados, verbose = False):
    quantidade = len(dados)
    
    if verbose == True:
        print("O Corpus possui", quantidade, "sentencas.")
        
    return quantidade



def getQuantidadeTokens(dados, verbose = False):
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    quantidade = 0
    for sent in sentences:
        quantidade += len(sent)
            
    if verbose == True:
        print("O Corpus possui", quantidade, "tokens.")
        
    return quantidade

def getQuantidadeUniqueTokens(dados, verbose = False):
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    tokensvistos = set()
    for sent in sentences:
        for token in sent:
            tokensvistos.add(token)
        
    quantidade = len(list(tokensvistos))
        
    if verbose == True:
        print("O Corpus possui", quantidade, "tokens unicos.")
        
    return quantidade

def getQuantidadeEntidades(dados, verbose = False): #total and for each type
    import AbreCorpus as AbreSemClinBr
    entities = AbreSemClinBr.getEntitiesOnly(dados)
    quantidadeTotal = 0
    entidadesDict = dict()
    for entitySent in entities:
        for entity in entitySent:
            if type(entity) == list:
                if entity != ["O"]:
                    for e in entity:
                        quantidadeTotal+=1
                        try:
                            entidadesDict[e] += 1
                        except:
                            entidadesDict[e] = 1                   
                        try:
                            entidadesDict[e[2:]] += 1
                        except:
                            entidadesDict[e[2:]] = 1
            else:
                if entity != "O":
                    quantidadeTotal+=1
                    try:
                        entidadesDict[entity] += 1
                    except:
                        entidadesDict[entity] = 1
                    try:
                        entidadesDict[entity[2:]] += 1
                    except:
                        entidadesDict[entity[2:]] = 1
                        
    if verbose == True:
        print("O Corpus possui", quantidadeTotal, "entidades.")
        for entidadeAtual,quantidadeAtual in entidadesDict.items():
            if entidadeAtual[1] != "-":
                print("A entidade", entidadeAtual,"aparece", quantidadeAtual, "vezes.")
        for entidadeAtual,quantidadeAtual in entidadesDict.items():
            if entidadeAtual[1] == "-":
                print("A etiqueta", entidadeAtual,"aparece", quantidadeAtual, "vezes.")
        
    return quantidadeTotal,entidadesDict



def getQuantidadeUniqueTokensAnotados(dados, verbose = False):
    entidadesDict = dict()
    tokensAnotados = set()
    quantidadeTotal = 0
    for sent in dados:
        for token in sent:
            entity = token[1]
            if type(entity) == list:
                if entity != ["O"]:
                    tokensAnotados.add(token[0])
                    quantidadeTotal+=1
                    for e in entity:
                        try:
                            entidadesDict[e].add(token[0])
                        except:
                            entidadesDict[e] = set()
                            entidadesDict[e].add(token[0])
                        try:
                            entidadesDict[e[2:]].add(token[0])
                        except:
                            entidadesDict[e[2:]] = set()    
                            entidadesDict[e[2:]].add(token[0])
                            
            else:
                if entity != "O":
                    tokensAnotados.add(token[0])
                    quantidadeTotal+=1
                    try:
                        entidadesDict[entity].add(token[0])
                    except:
                        entidadesDict[entity] = set()    
                        entidadesDict[entity].add(token[0])
                    try:
                        entidadesDict[entity[2:]].add(token[0])
                    except:
                        entidadesDict[entity[2:]] = set()    
                        entidadesDict[entity[2:]].add(token[0])
    
    
    entidadesQuantityDict = dict()
    quantidadeTokensUnicosAnotados = len(list(tokensAnotados))
    for entidadeAtual,UniqueTokens in entidadesDict.items():
        entidadesQuantityDict[entidadeAtual] = len(list(UniqueTokens))
    
    if verbose == True:
        print("O Corpus possui", quantidadeTotal, "tokens anotados.")
        print("O Corpus possui", quantidadeTokensUnicosAnotados, "tokens unicos anotados.")
        
        for entidadeAtual,quantidadeAtual in entidadesQuantityDict.items():
            if entidadeAtual[1] != "-":
                print("O Corpus possui", quantidadeAtual, "tokens unicos anotados com a entidade",entidadeAtual,".")
        for entidadeAtual,quantidadeAtual in entidadesQuantityDict.items():
            if entidadeAtual[1] == "-":
                print("O Corpus possui", quantidadeAtual, "tokens unicos anotados com a tag",entidadeAtual,".")
                

    return quantidadeTotal,quantidadeTokensUnicosAnotados,entidadesQuantityDict




def getQuantidadeUniqueTokenPairs(dados, verbose = False):
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    tokenPairvistos = set()
    for sent in sentences:
        for i in range(len(sent)-1):
            try:
                tokenPairvistos.add((sent[i],sent[i+1]))
            except:
                pass
    quantidade = len(list(tokenPairvistos))
        
    if verbose == True:
        print("O Corpus possui", quantidade, "pares de token unicos.")
        
    return quantidade



def getQuantidadeUniqueTokenNgrans(dados, verbose = False, quantidade = 3):
    if quantidade < 3:
        print("Quantidade muito pequena")
        return 0
        
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    tokenPairvistos = set()
    for sent in sentences:
        for i in range(len(sent)+1-quantidade):
            ngrama = []
            for k in range(quantidade):
                ngrama.append(sent[i+k])
                
            try:
                tokenPairvistos.add(tuple(ngrama))
            except:
                pass
                    
    quantidadeNgrans = len(list(tokenPairvistos))
        
    if verbose == True:
        print("O Corpus possui", quantidadeNgrans, "N grams unicos de tamanho",quantidade,".")
        
    return quantidadeNgrans







import matplotlib.pyplot as plt

def plot2Lists(l1,l2,title = "",ylabel = "", xlabel = ""):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.plot(l1,l2)
    plt.show()


#word_rank = [1,2,3,4]
#word_frequency = [10,6,3,2]
#plot2Lists(word_rank,word_frequency)
#plot2Lists(word_rank,word_frequency,title = "Word Frequencies",ylabel = "Total Number of Occurrences", xlabel = "Unique Words")






def getSentenceCharacterQuantityDistribution(dados, verbose = False): #just the distribution
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    sizeFrequencyDict = dict()
    for sent in sentences:
        inteira = ""
        for t in sent:
            inteira+=t+" "
        
        size = len(inteira)-1
        try:
            sizeFrequencyDict[size] += 1 
        except:
            sizeFrequencyDict[size] = 1 
            
    sizeFrequency = [(k,v) for k, v in sizeFrequencyDict.items()]
    sizeFrequency.sort(key=lambda x: x[0])
    
    
    word_rank,word_frequency = zip(*sizeFrequency)
    
    if verbose == True:
        plot2Lists(word_rank,word_frequency,title = "Sentence Character Quantity Distribution",ylabel = "Total Number of Occurrences", xlabel = "Sentence Character Quantity")

    return sizeFrequency




def getSentenceTokenQuantityDistribution(dados, verbose = False):  #just the distribution
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    sizeFrequencyDict = dict()
    for sent in sentences:
        size = len(sent)
        try:
            sizeFrequencyDict[size] += 1 
        except:
            sizeFrequencyDict[size] = 1 
            
    sizeFrequency = [(k,v) for k, v in sizeFrequencyDict.items()]
    sizeFrequency.sort(key=lambda x: x[0])
    
    
    word_rank,word_frequency = zip(*sizeFrequency)
    
    if verbose == True:
        plot2Lists(word_rank,word_frequency,title = "Sentence Token Quantity Distribution",ylabel = "Total Number of Occurrences", xlabel = "Sentence Token Quantity")

    return sizeFrequency



def getTokenCharacterQuantityDistribution(dados, verbose = False): #total and for each entity

    sizeFrequencyDict = dict()
    
    sizeFrequencyDictEntidades = dict()
    
    for sent in dados:
        for TE in sent:
            token = TE[0]
            entidades = TE[1]            
            size = len(token)
            try:
                sizeFrequencyDict[size] += 1 
            except:
                sizeFrequencyDict[size] = 1 
            
            
            if entidades[0] != "O":
                
                if type(entidades) == list:
                    for e in entidades:
                        ent = e[2:]
                        try:
                            sizeFrequencyDictEntidades[ent][size] += 1
                        except:
                            try:
                                sizeFrequencyDictEntidades[ent][size] = 1
                            except:
                                sizeFrequencyDictEntidades[ent] = dict()            
                else:
                    ent = entidades[2:]
                    try:
                        sizeFrequencyDictEntidades[ent][size] += 1
                    except:
                        try:
                            sizeFrequencyDictEntidades[ent][size] = 1
                        except:
                            sizeFrequencyDictEntidades[ent] = dict()
    
            
            
    sizeFrequency = [(k,v) for k, v in sizeFrequencyDict.items()]
    sizeFrequency.sort(key=lambda x: x[0])
        
    
    sizeFrequencyEntities = [(ent,[(k,v) for k, v in dat.items()]) for ent,dat in sizeFrequencyDictEntidades.items()]
    for i in range(len(sizeFrequencyEntities)):
        sizeFrequencyEntities[i][1].sort(key=lambda x: x[0])
    
    
    if verbose == True:
        word_rank,word_frequency = zip(*sizeFrequency)
        plot2Lists(word_rank,word_frequency,title = "Token Character Quantity Distribution",ylabel = "Total Number of Occurrences", xlabel = "Token Character Quantity")

        for entidafreq in sizeFrequencyEntities:
            entidade = entidafreq[0]
            freq = entidafreq[1]
            print("Token Character Quantity for the entity:",entidade,".")
            try:
                word_rank,word_frequency = zip(*freq)
                plot2Lists(word_rank,word_frequency,title = "Token Character Quantity Distribution for:"+entidade,ylabel = "Total Number of Occurrences", xlabel = "Token Character Quantity")
            except:
                print("ERROR, maybe the entity has very low occurrences")
    

    return sizeFrequency,sizeFrequencyEntities






def getUniqueTokenFrequencyDistribution(dados, verbose = False, top = 20): #Top 20 words and overview without label / total and for each entity
    if top < 1:
        print("top muito pequeno")
        return None
    elif type(top) != int:
        print("top precisa ser um inteiro")
        return None

    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    tokensvistos = dict()
    for sent in sentences:
        for token in sent: 
            try:
                tokensvistos[token] += 1
            except:
                tokensvistos[token] = 1
        
    tokenFrequency = [(k,v) for k, v in tokensvistos.items()]
    tokenFrequency.sort(key=lambda x: x[1],reverse = True)
     
     
     
    tokensvistosEntidades = dict()
    
    for sent in dados:
        for TE in sent:
            token = TE[0]
            entidades = TE[1]            
            
            if entidades[0] != "O":
                
                if type(entidades) == list:
                    for e in entidades:
                        ent = e[2:]
                        try:
                            tokensvistosEntidades[ent][token] += 1
                        except:
                            try:
                                tokensvistosEntidades[ent][token] = 1
                            except:
                                tokensvistosEntidades[ent] = dict()            
                else:
                    ent = entidades[2:]
                    try:
                        tokensvistosEntidades[ent][token] += 1
                    except:
                        try:
                            tokensvistosEntidades[ent][token] = 1
                        except:
                            tokensvistosEntidades[ent] = dict()
    
            
    TokenFrequencyEntities = [(ent,[(k,v) for k, v in dat.items()]) for ent,dat in tokensvistosEntidades.items()]
    for i in range(len(TokenFrequencyEntities)):
        TokenFrequencyEntities[i][1].sort(key=lambda x: x[1],reverse=True)


     
     
    if verbose == True:
        words,word_frequency = zip(*tokenFrequency)
        print("The",top,"most used Tokens in the corpus are:",words[:top])
        plot2Lists([x for x in range(top)],word_frequency[:top],title = "TOP "+str(top)+" Unique Token Frequency Distribution",ylabel = "Total Number of Occurrences", xlabel = "Unique Token")
        plot2Lists([x for x in range(len(word_frequency))],word_frequency,title = "Unique Token Frequency Distribution",ylabel = "Total Number of Occurrences", xlabel = "Unique Token")

        for entidafreq in TokenFrequencyEntities:
            entidade = entidafreq[0]
            freq = entidafreq[1]
            try:
                word_rank,word_frequency = zip(*freq)
                print("The",top,"most used Tokens for the entity:",entidade,"are:",word_rank[:top])
                plot2Lists([x for x in range(top)],word_frequency[:top],title = "TOP "+str(top)+" Unique Token Frequency Distribution: "+entidade,ylabel = "Total Number of Occurrences", xlabel = "Unique Token")
                plot2Lists([x for x in range(len(word_frequency))],word_frequency,title = "Unique Token Frequency Distribution: "+entidade,ylabel = "Total Number of Occurrences", xlabel = "Unique Token")
            except:
                print("ERROR, maybe the entity has very low occurrences")        
        
        
    return tokenFrequency,TokenFrequencyEntities






def getQuantidadeUniqueTokenPairsDistribution(dados, verbose = False, top = 20):
    if top < 1:
        print("top muito pequeno")
        return None
    elif type(top) != int:
        print("top precisa ser um inteiro")
        return None
        
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    tokensvistos = dict()
    for sent in sentences:
        for i in range(len(sent)-1):
            token1 = sent[i]
            token2 = sent[i+1]
        
            try:
                tokensvistos[(token1,token2)] += 1
            except:
                tokensvistos[(token1,token2)] = 1
        
    tokenFrequency = [(k,v) for k, v in tokensvistos.items()]
    tokenFrequency.sort(key=lambda x: x[1],reverse = True)


    if verbose == True:
        words,word_frequency = zip(*tokenFrequency)
        print("The",top,"most used Tokens Pairs in the corpus are:",words[:top])
        plot2Lists([x for x in range(top)],word_frequency[:top],title = "TOP "+str(top)+" Unique Token Pair Frequency Distribution",ylabel = "Total Number of Occurrences", xlabel = "Unique Token Pair")
        plot2Lists([x for x in range(len(word_frequency))],word_frequency,title = "Unique Token Pair Frequency Distribution",ylabel = "Total Number of Occurrences", xlabel = "Unique Token Pair")


    return tokenFrequency









def getQuantidadeUniqueTokenNgransDistribution(dados, verbose = False, quantidade = 3, top = 20):
    if top < 1:
        print("top muito pequeno")
        return None
    elif type(top) != int:
        print("top precisa ser um inteiro")
        return None
        
    if quantidade < 3:
        print("quantidade muito pequena")
        return None
        
        
    import AbreCorpus as AbreSemClinBr
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    tokensvistos = dict()
    for sent in sentences:
        for i in range(len(sent)+1-quantidade):
            ngrama = []
            for k in range(quantidade):
                ngrama.append(sent[i+k])
        
            try:
                tokensvistos[tuple(ngrama)] += 1
            except:
                tokensvistos[tuple(ngrama)] = 1
        
    tokenFrequency = [(k,v) for k, v in tokensvistos.items()]
    tokenFrequency.sort(key=lambda x: x[1],reverse = True)


    if verbose == True:
        words,word_frequency = zip(*tokenFrequency)
        print("The",top,"most used Tokens Ngram of size",quantidade,"in the corpus are:",words[:top])
        plot2Lists([x for x in range(top)],word_frequency[:top],title = "TOP "+str(top)+" Unique Token Ngram Frequency Distribution",ylabel = "Total Number of Occurrences", xlabel = "Unique Token Ngram")
        plot2Lists([x for x in range(len(word_frequency))],word_frequency,title = "Unique Token Ngram Frequency Distribution",ylabel = "Total Number of Occurrences", xlabel = "Unique Token Ngram")


    return tokenFrequency






def plotPie(percentage,labels):
    fig1, ax1 = plt.subplots()
    ax1.pie(percentage, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()







def getEntityDistributionEntidades(dados, verbose = False):

    _,entidadesDict = getQuantidadeEntidades(dados, verbose = False)
    entitydistributionDict = dict()
    
    for ent,qtd in entidadesDict.items():
        if ent[1] != "-":
            entitydistributionDict[ent] = qtd
        
    EntityDistribution = [(k,v) for k, v in entitydistributionDict.items()]
    EntityDistribution.sort(key=lambda x: x[1],reverse = True)
    
    labels,percentage = zip(*EntityDistribution)
    if verbose == True:
        print("A distribuição entre as entidades numericamente é:",EntityDistribution)
        print("A distribuição entre as entidades em porcentagem é:",list(zip(labels,[p/sum(percentage) for p in percentage])))
        plotPie([p/sum(percentage) for p in percentage],labels)
        plot2Lists([lk for lk in range(len(percentage))],[p/sum(percentage) for p in percentage],title = "Entity Distribution",ylabel = "Percentage", xlabel = "Entities")
    
    return EntityDistribution,list(zip(labels,[p/sum(percentage) for p in percentage]))
    
    
    
    
    
    
    
def getTagDistributionEntidades(dados, verbose = False):

    _,entidadesDict = getQuantidadeEntidades(dados, verbose = False)
    entityTAGdistributionDict = dict()
    
    for ent,qtd in entidadesDict.items():
        if ent[1] == "-":
            try:
                entityTAGdistributionDict[ent[2:]][ent] = qtd/entidadesDict[ent[2:]]
            except:
                entityTAGdistributionDict[ent[2:]] = dict()
                entityTAGdistributionDict[ent[2:]][ent] = qtd/entidadesDict[ent[2:]]
    
    
    EntityTAGDistribution = [(ent,[(k,v) for k, v in dat.items()]) for ent,dat in entityTAGdistributionDict.items()]
    for i in range(len(EntityTAGDistribution)):
        EntityTAGDistribution[i][1].sort(key=lambda x: x[1],reverse=True)
    
    
    if verbose == True:
        for e in EntityTAGDistribution:
            nome = e[0]
            print("A distribuição das tags da entidade",nome,":")
            for tagPerc in e[1]:
                print("A tag",tagPerc[0],"corresponde",tagPerc[1],"%.")

            labels,percentage = zip(*e[1])
            plotPie(percentage,labels)
    
    return EntityTAGDistribution
    
    
    
def getVocabularyDensity(dados, verbose = False): 

    total = getQuantidadeTokens(dados, verbose = False)
    unique = getQuantidadeUniqueTokens(dados, verbose = False)
            
    vocabularyDensity = unique / total
            
    if verbose == True:
        print("Vocabulary Density = number of unique words / number of words ")
        print("The higher, the better")
        print("A densidade do vocabulario é de:",vocabularyDensity)
        
    return vocabularyDensity




def getEntityDensity(dados, verbose = False):

    quantidadeTotal = 0
    quantidadeEntityTotal = 0
    vocabularioComEntidade = []
    
    for entitySent in dados:
        for TokenEntity in entitySent:
            token = TokenEntity[0]
            entity = TokenEntity[1]
            if type(entity) == list:
                if entity != ["O"]:
                    quantidadeEntityTotal+=1
                    if token not in vocabularioComEntidade:
                        vocabularioComEntidade.append(token)
                else:
                    quantidadeTotal+=1               

            else:
                if entity != "O":
                    quantidadeEntityTotal+=1    
                    if token not in vocabularioComEntidade:
                        vocabularioComEntidade.append(token)
                else:     
                    quantidadeTotal+=1
                        
                        
                        
    taxa = quantidadeEntityTotal/(quantidadeTotal+quantidadeEntityTotal)                    
    taxaTokenTaggeado = len(vocabularioComEntidade)/ getQuantidadeUniqueTokens(dados, verbose = False)
            
            
    if verbose == True:
        print(taxa,"% dos tokens são entidades.")
        print(taxaTokenTaggeado,"% dos tokens unicos foram anotados por uma entidade pelo menos uma vez.")

       
    return taxa,taxaTokenTaggeado





def getTokenPositioningFrequency(dados, verbose = False):
    import AbreCorpus as AbreSemClinBr
    import estatistica
    sentences = AbreSemClinBr.getSentencesOnly(dados)
    uniqueTokenPositionDict = dict()
    for i in range(len(sentences)):
        sent = sentences[i]
        for token in sent:
            try:
                uniqueTokenPositionDict[token].append(i)
            except:
                uniqueTokenPositionDict[token] = [i]


    medias = []
    variancias = []
    desviosPadroes = []

    for token, positions in uniqueTokenPositionDict.items():
        medias.append(estatistica.media(positions))
        variancias.append(estatistica.variancia(positions))
        desviosPadroes.append(estatistica.desvio_padrao(positions))

    
    mediaFinalmedias = estatistica.media(medias)
    mediaFinalvariancias = estatistica.media(variancias)
    mediaFinaldesviosPadroes = estatistica.media(desviosPadroes)

    desviosPadroesFinalmedias = estatistica.desvio_padrao(medias)
    desviosPadroesFinalvariancias = estatistica.desvio_padrao(variancias)
    desviosPadroesFinaldesviosPadroes = estatistica.desvio_padrao(desviosPadroes)

# the vector is like this dict[uniqueToken] = ["positions of the sentence it appeared",153,316,754,2333]
#than we can calculate variance etc....

    if verbose == True:
        print("A media da media das posições é:",mediaFinalmedias)
        print("A media da variancia das posições é:",mediaFinalvariancias)
        print("A media do desvio padrão das posições é:",mediaFinaldesviosPadroes)

        print("O desvio padrão da media das posições é:",desviosPadroesFinalmedias)
        print("O desvio padrão da variancia das posições é:",desviosPadroesFinalvariancias)
        print("O desvio padrão do desvio padrão das das posições é:",desviosPadroesFinaldesviosPadroes)

    return mediaFinalmedias,mediaFinalvariancias,mediaFinaldesviosPadroes,desviosPadroesFinalmedias,desviosPadroesFinalvariancias,desviosPadroesFinaldesviosPadroes

















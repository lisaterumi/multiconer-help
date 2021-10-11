# coding: utf-8
import xml.dom.minidom
import os

# IOB1: Tag B-XXXX is the beginning of a named entity of category XXXX that immediately
#follows another named entity of category XXXX

# IOB2: Tag B-XXXX is used at the start of every named entity.

# IOE1: Tag E-XXXX is used to mark the last token of a named entity immediately preceding
#another named entity of category XXXX

# IOE2: Tag E-XXXX is used at the end of every named entity.

# BIOES or IOBES: Tag S-XXXX is used to represent a named entity with a single token.
#Named entities longer than one token always start with B-XXXX and end with E-XXXX


def openSemClinBrXMLfile(XMLfileName, tag = "IOBES"): #GET DATA IN IOBES or BIOES FORMAT
    doc = xml.dom.minidom.parse(XMLfileName);
    
    annotation = doc.getElementsByTagName("annotation")
    XMLanotacoes = []
    for ent in annotation:
        XMLanotacoes.append((ent.getAttribute("tag"),ent.getAttribute("start"),ent.getAttribute("end"),ent.getAttribute("text")))
    
    token = doc.getElementsByTagName("token")
    XMLtokens = []
    for tok in token:
        XMLtokens.append((tok.getAttribute("sentorder"),tok.getAttribute("begin"),tok.getAttribute("end"),tok.getAttribute("text")))
    
    sentence = doc.getElementsByTagName("sentence")
    XMLsentencas = []
    for sent in sentence:
        XMLsentencas.append((sent.getAttribute("order"),sent.getAttribute("text")))
    
    
    ALMOSTdados = []
    
    POSICAOanotacaoPAROU = 0
    POSICAOnextSENT = 0
    
    for sent in XMLsentencas:
        
        sentenca = []
        
        for i in range(len(XMLtokens[POSICAOnextSENT:])):
            tok = XMLtokens[POSICAOnextSENT+i]
            if int(tok[0]) > int(sent[0]):
                POSICAOnextSENT = POSICAOnextSENT+i
                break
               
            encontrou = False
            
            for j in range(len(XMLanotacoes[POSICAOanotacaoPAROU:])):

                ano = XMLanotacoes[POSICAOanotacaoPAROU+j]
                if int(ano[1]) > int(tok[1]):
                    POSICAOanotacaoPAROU = POSICAOanotacaoPAROU+j
                    break
                
                if ano[1] == tok[1] and ano[2] == tok[2] and ano[3] == tok[3]: #É um token unico
                    sentenca.append((ano[3],"S",ano[0]))
                    encontrou = True
                    break
                elif tok[1] >= ano[1] and tok[2] <= ano[2] and tok[3] in ano[3]:
                    sentenca.append((tok[3],"A",ano[0]))
                    encontrou = True
                    break
            
            if not encontrou:        
                sentenca.append((tok[3],"O","O"))

        ALMOSTdados.append(sentenca)  
              
            
            
    dados = []
    for sent in ALMOSTdados:
        sentenca = []
        for i in range(len(sent)):
            toke = sent[i]
            
            if toke[1] == "S":
                ent = toke[2].split("|")
                entidades = ["S-"+e for e in ent]
                sentenca.append((toke[0],list(set(entidades))))
                
            elif toke[1] == "A":
                ent = toke[2].split("|")
                entidades = []
                for e in ent:
                    if i == 0 or sent[i-1][1] != "A" or sent[i-1][2] != toke[2]: #nao é a mesma entidade  
                        entidades.append("B-"+e)
                    elif i == len(sent)-1 or sent[i+1][1] != "A" or sent[i+1][2] != toke[2]:
                        entidades.append("E-"+e)
                    else:
                        entidades.append("I-"+e)
                        
                sentenca.append((toke[0],list(set(entidades))))
                #sentenca.append((toke[0],entidades))
                
                
            else:
                sentenca.append((toke[0],["O"]))
                
        if sentenca != []:
            dados.append(sentenca)
        
    if tag == "IOBES" or tag == "BIOES":
        return dados
    elif tag == "IOB" or tag == "IOB1":
        return converteDadosFromIOBES(dados,"IOB1")
    elif tag == "IOB2":
        return converteDadosFromIOBES(dados,"IOB2")
    elif tag == "IOE" or tag == "IOE1":
        return converteDadosFromIOBES(dados,"IOE1")
    elif tag == "IOE2":
        return converteDadosFromIOBES(dados,"IOE2")
    elif tag == "IO":
        return converteDadosFromIOBES(dados,"IO")
    else:
        print("tags disponiveis: IO,(IOB1 or IOB),IOB2,(IOE1 or IOE),IOE2,(IOBES or BIOES)")
        
        
        
        
        
def converteDadosFromIOBES(dados,tag):
    if tag == "IO":
        print("Atencao, a tag IO nao consegue ser convertida para IOB1 e IOE1, alem de ser parcial com as outras tags")

    NEWdados = []
    for sent in dados:
        NEWsent = []
        for i in range(len(sent)):
            token = sent[i]
            if token[1][0] == "O":
                NEWsent.append(token)
            else:
                
                if type(token[1]) == list:
                    TagsAtuais = token[1]
                elif type(token[1]) == str:
                    TagsAtuais = [token[1]]
                else:
                    print("Input em formato errado!")
                    
                entidades = []
                for ent in TagsAtuais:
                    
                    if ent[0] == "S":
                        if tag == "IOB1" or tag == "IOB":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOB2":
                            entidades.append("B"+ent[1:])
                        elif tag == "IOE1" or tag == "IOE":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOE2":
                            entidades.append("E"+ent[1:])
                        elif tag == "IO":
                            entidades.append("I"+ent[1:])
                            
                    elif ent[0] == "B":
                        if tag == "IOB1" or tag == "IOB":
                            if i == 0 or ent[1:] not in [f[1:] for f in sent[i-1][1]]:
                                entidades.append("I"+ent[1:])
                            else:
                                entidades.append("B"+ent[1:])
                        elif tag == "IOB2":
                            entidades.append("B"+ent[1:])
                        elif tag == "IOE1" or tag == "IOE":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOE2":
                            entidades.append("I"+ent[1:])
                        elif tag == "IO":
                            entidades.append("I"+ent[1:])
                            
                    elif ent[0] == "I":
                        if tag == "IOB1" or tag == "IOB":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOB2":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOE1" or tag == "IOE":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOE2":
                            entidades.append("I"+ent[1:])
                        elif tag == "IO":
                            entidades.append("I"+ent[1:])
                            
                    elif ent[0] == "E":
                        if tag == "IOB1" or tag == "IOB":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOB2":
                            entidades.append("I"+ent[1:])
                        elif tag == "IOE1" or tag == "IOE":
                            if i == len(sent)-1 or ent[1:] not in [f[1:] for f in sent[i+1][1]]:
                                entidades.append("I"+ent[1:])
                            else:
                                entidades.append("E"+ent[1:])
                        elif tag == "IOE2":
                            entidades.append("E"+ent[1:])
                        elif tag == "IO":
                            entidades.append("I"+ent[1:])
                            
                if type(token[1]) == list:
                    NEWsent.append((token[0],entidades))
                elif type(token[1]) == str:
                    NEWsent.append((token[0],entidades[0]))
                else:
                    print("Input em formato errado!")
                
        NEWdados.append(NEWsent)
    return NEWdados




def converteDadosToIOBES(dados,tag):
    if tag == "IO":
        print("Atencao, a tag IO nao consegue ser convertida para IOB1 e IOE1, alem de ser parcial com as outras tags")

    NEWdados = []
    for sent in dados:
        NEWsent = []
        for i in range(len(sent)):
            token = sent[i]
            if token[1][0] == "O":
                NEWsent.append(token)
            else:
                
                if type(token[1]) == list:
                    TagsAtuais = token[1]
                elif type(token[1]) == str:
                    TagsAtuais = [token[1]]
                else:
                    print("Input em formato errado!")
                    
                entidades = []
                for ent in TagsAtuais:
                                                        
                    if tag == "IOB1" or tag == "IOB":
                        if ent[0] == "B":
                            if i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]:
                                entidades.append("S"+ent[1:])
                            else:
                                entidades.append("B"+ent[1:])
                                
                        if ent[0] == "I":
                            if (i == 0 or ("I"+ent[1:] not in [f for f in sent[i-1][1]] and "B"+ent[1:] not in [f for f in sent[i-1][1]])) and (i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]):
                                entidades.append("S"+ent[1:])
                            elif i == 0 or ("I"+ent[1:] not in [f for f in sent[i-1][1]] and "B"+ent[1:] not in [f for f in sent[i-1][1]]):
                                entidades.append("B"+ent[1:])
                            elif i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]:
                                entidades.append("E"+ent[1:])
                            else:
                                entidades.append("I"+ent[1:])
                            
                    elif tag == "IOB2":
                        if ent[0] == "B":
                            if i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]:
                                entidades.append("S"+ent[1:])
                            else:
                                entidades.append("B"+ent[1:])
                                
                        if ent[0] == "I":
                            if i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]:
                                entidades.append("E"+ent[1:])
                            else:
                                entidades.append("I"+ent[1:])
                                
                    elif tag == "IOE1" or tag == "IOE":
                        if ent[0] == "E":
                            if i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]:
                                entidades.append("S"+ent[1:])
                            else:
                                entidades.append("E"+ent[1:])
                                
                        if ent[0] == "I":
                            if (i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]) and (i == len(sent)-1 or ("I"+ent[1:] not in [f for f in sent[i+1][1]] and "B"+ent[1:] not in [f for f in sent[i+1][1]])):
                                entidades.append("S"+ent[1:])
                            elif i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]:
                                entidades.append("B"+ent[1:])
                            elif i == len(sent)-1 or ("I"+ent[1:] not in [f for f in sent[i+1][1]] and "B"+ent[1:] not in [f for f in sent[i+1][1]]):
                                entidades.append("E"+ent[1:])
                            else:
                                entidades.append("I"+ent[1:])                        
                        
                    elif tag == "IOE2":
                        if ent[0] == "E":
                            if i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]:
                                entidades.append("S"+ent[1:])
                            else:
                                entidades.append("E"+ent[1:])
                                
                        if ent[0] == "I":
                            if i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]:
                                entidades.append("B"+ent[1:])
                            else:
                                entidades.append("I"+ent[1:])

                    elif tag == "IO":
                        if (i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]) and (i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]):
                            entidades.append("S"+ent[1:])
                        elif i == 0 or "I"+ent[1:] not in [f for f in sent[i-1][1]]:
                            entidades.append("B"+ent[1:])
                        elif i == len(sent)-1 or "I"+ent[1:] not in [f for f in sent[i+1][1]]:
                            entidades.append("E"+ent[1:])
                        else:
                            entidades.append("I"+ent[1:])                               
                            
                if type(token[1]) == list:
                    NEWsent.append((token[0],entidades))
                elif type(token[1]) == str:
                    NEWsent.append((token[0],entidades[0]))
                else:
                    print("Input em formato errado!")
                
        NEWdados.append(NEWsent)
    return NEWdados





def converteDados(dados,tagDesejada,tagAtual = None):
    if tagAtual == None:
        tagAtual = getRepresentacao(dados)
    
    if tagAtual == tagDesejada:
        return dados

    if tagAtual == "IOBES" or tagAtual == "BIOES":
        NEWdados = converteDadosFromIOBES(dados,tagDesejada)
    else:
        if tagDesejada == "IOBES" or tagDesejada == "BIOES":
            NEWdados = converteDadosToIOBES(dados,tagAtual)
        else:
            dadosTemp = converteDadosToIOBES(dados,tagAtual)
            NEWdados = converteDadosFromIOBES(dadosTemp,tagDesejada)
        
    return NEWdados



def openAllSemClinBrFiles(path, tag = "IOBES"):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.xml' in file:
                files.append(os.path.join(r, file))
    
    dados = []
    for f in files:
        dados.extend(openSemClinBrXMLfile(f,tag = tag))
    
    return dados




def getSpecificEntities(dados,entidades):     
    if type(entidades) != list:
        entidades = [entidades]
    NEWdados = []
    for sent in dados:
        NEWsentenca = []
        for token in sent:
            entidadesPresentes = []
            encontrou = False
            for ent in token[1]:
                if ent[2:] in entidades:
                    encontrou = True
                    if len(entidades) == 1:
                        entidadesPresentes = ent
                        break
                    else:
                        entidadesPresentes.append(ent)
                        
            if not encontrou:
                if len(entidades) == 1:
                    entidadesPresentes = "O"
                else:
                    entidadesPresentes.append("O")                    
                    
            NEWsentenca.append((token[0],entidadesPresentes))
        NEWdados.append(NEWsentenca)
    return NEWdados




def getSentencesOnly(dados):
    newDados = []
    for sent in dados:
        try:
            newDados.append(list(list(zip(*sent))[0]))
        except:
            pass
    return newDados

def getEntitiesOnly(dados):
    newDados = []
    for sent in dados:
        try:
            newDados.append(list(list(zip(*sent))[1]))
        except:
            pass
            
    return newDados




def getRepresentacao(dados):
    entities = getEntitiesOnly(dados)
    representacoes = set()
    
    for sententity in entities:
        for entity in sententity:
            if type(entity) == list:
                for e in entity:
                    representacoes.add(e[0])
            else:
                representacoes.add(entity[0])


    representacoes = list(representacoes)
    if "S" in representacoes or "U" in representacoes or len(representacoes) > 3:
        return "IOBES"
    elif "B" in representacoes:
        for sententity in entities:
            for a in range(len(sententity)):
                entity = sententity[a]
                if type(entity) == list:
                    for e in entity:
                        if e[0] == "B":
                            if a == 0:
                                return "IOB2"
                            elif e[2:] not in [pl[2:] for pl in sententity[a-1]]:
                                return "IOB2"
                            else:
                                return "IOB1"
                else:
                    if entity[0] == "B":
                        if a == 0:
                            return "IOB2"
                        elif entity[2:] not in [pl[2:] for pl in sententity[a-1]]:
                            return "IOB2"
                        else:
                            return "IOB1"
                
        return "IOB1"  
    elif "E" in representacoes:
        for sententity in entities:
            for a in range(len(sententity)):
                entity = sententity[a]
                if type(entity) == list:
                    for e in entity:
                        if e[0] == "E":
                            if a == len(sententity)-1:
                                return "IOE2"
                            elif e[2:] not in [pl[2:] for pl in sententity[a+1]]:
                                return "IOE2"
                            else:
                                return "IOE1"
                else:
                    if entity[0] == "E":
                        if a == len(sententity)-1:
                            return "IOE2"
                        elif entity[2:] not in [pl[2:] for pl in sententity[a+1]]:
                            return "IOE2"
                        else:
                            return "IOE1"
                
        return "IOE1"  
    else:
        return "IO"




def makeEntityGroup(dados,groupName,Entities):
    if type(Entities) != list:
        Entities = [Entities]


    newDadosAux = []
    for sent in dados:
        newSent = []
        for token in sent:
            if type(token[1]) == list:
                entid = []
                encontrou = False
                for e in token[1]:
                    if e[2:] not in Entities:
                        entid.append(e)
                    elif encontrou == False:
                        entid.append(groupName)
                        #entid.append(e[:2]+groupName)
                        encontrou = True
            else:
                if token[1][2:] in Entities:
                    #entid = token[1][:2]+groupName
                    entid = groupName
                else:
                    entid = token[1]
            
            newSent.append((token[0],entid))
        newDadosAux.append(newSent)
      
      
    newDados = []
    for sent in newDadosAux:
        newSent = []
        for i in range(len(sent)):
            token = sent[i]
            if type(token[1]) == list:
                entid = []
                for e in token[1]:
                    if e == groupName:
                      
                        if (i == 0 or groupName not in sent[i-1][1]) and (i == len(sent)-1 or groupName not in  sent[i+1][1]):
                            entid.append("S-"+e)
                        elif (i == 0 or groupName not in sent[i-1][1]):
                            entid.append("B-"+e)
                        elif (i == len(sent)-1 or groupName not in  sent[i+1][1]):
                            entid.append("E-"+e)
                        else:
                            entid.append("I-"+e)
                      
                    else:
                        entid.append(e)
                
            else:
                if token[1] == groupName:
                    if (i == 0 or sent[i-1][1] != groupName) and (i == len(sent)-1 or sent[i+1][1] != groupName):
                        entid = "S-"+token[1]
                    elif (i == 0 or sent[i-1][1] != groupName):
                        entid = "B-"+token[1]
                    elif (i == len(sent)-1 or sent[i+1][1] != groupName):
                        entid = "E-"+token[1]
                    else:
                        entid = "I-"+token[1]

                else:
                    entid = token[1]            
            
            newSent.append((token[0],entid))
        newDados.append(newSent)            
            
    repres = getRepresentacao(dados)
    if repres != "IOBES":
        newDados = converteDadosFromIOBES(newDados,repres)

    return newDados




def getSentencesThatHaveAnEspecificEntity(dados, entidade, verbose = False):
    newDados = []
    for sent in dados:
        newSent = []
        for token in sent:
            if token[1][0] != "O":
                if type(token[1]) == list:
                    if entidade in [t[2:] for t in token[1]]:
                        newDados.append(sent)
                        break
        
                else:
                    if entidade == token[1][2:]:
                        newDados.append(sent)
                        break
        
    if verbose == True:
        print("Sentencas com a Entidade:",entidade)
        for sent in newDados:
            print(sent)
                
    return newDados




def getEntitiesUsed(dados):
    entidades = set()
    for sent in dados:
        for tokEnt in sent:
            if tokEnt[1][0] != "O":
                if type(tokEnt[1]) == list:
                    for e in tokEnt[1]:
                        entidades.add(e[2:])
                else:
                    entidades.add(tokEnt[1][2:])
    return list(entidades)

def getEntitiesTagsUsed(dados):
    entidades = set()
    for sent in dados:
        for tokEnt in sent:
            if tokEnt[1][0] != "O":
                if type(tokEnt[1]) == list:
                    for e in tokEnt[1]:
                        entidades.add(e)
                else:
                    entidades.add(tokEnt[1])
    return list(entidades)
    




def getUniqueTokensForEntityType(dados,entityName):
    uniqueTokens = set()
    for sent in dados:
        for tokEnt in sent:
            if tokEnt[1][0] != "O":
                if type(tokEnt[1]) == list:
                    for e in tokEnt[1]:
                        if e[2:] == entityName:
                            uniqueTokens.add(tokEnt[0])
                else:
                    if tokEnt[1][2:] == entityName:
                        uniqueTokens.add(tokEnt[0])
    return list(uniqueTokens)    




def removespace(string):
    ns = ""
    for s in string:
        if s != " ":
            ns+=s
    return ns

def strip_accents(text):
    import unicodedata

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

def saveAsFlairNERCorpusFile(dados,filename):
    with open(filename,"w") as f:
        for sent in dados:
            for tokEnt in sent:
                tok = tokEnt[0]
                ent = tokEnt[1]
                tok = removespace(tok)
                ent = removespace(ent)
                tok = strip_accents(tok)
                ent = strip_accents(ent)
                
                f.write(tok + " " + ent + "\n")
            f.write("\n")
    
        f.close()
    print("Deu Certo?")







def saveAsTrainDevTestFlairNERCorpusFiles(dados,filename1,filename2,filename3,percent1,percent2):
    tamanho = len(dados)
    p1 = int((tamanho/100)*percent1)
    p2 = int((tamanho/100)*percent2)

    saveAsFlairNERCorpusFile(dados[:p1],filename1)
    saveAsFlairNERCorpusFile(dados[p1:p2],filename2)
    saveAsFlairNERCorpusFile(dados[p2:],filename3)










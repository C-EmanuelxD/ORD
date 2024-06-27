import io
valor_alto = "~"
valor_baixo = ""

numEOF = 0

def inicialize(numListas: int):
    anteriores = []
    nomes = []
    listas = []
    for i in range(numListas):
        anteriores.append(valor_baixo)
        nomes.append(valor_baixo)
        listas.append(None)
    
    for i in range(numListas):
        nomearq = i
        descritor = open(nomearq,"r")
        listas.append(descritor)
    saida = open("saida.txt","w")
    existem_mais_nomes = True
    return anteriores,nomes,listas,saida,existem_mais_nomes

def finalize(listas: list[io.TextIOWrapper], saida: io.TextIOWrapper, numListas: int):
    for i in range(numListas):
        listas[i].close()
    saida.close()

def leia_nome(lista: io.TextIOWrapper, nome_ant: str, existem_mais_nomes: bool, numListas: int)
    nome = lista.readline()

    if nome == "":
        nome = "~"
        numEOF += 1
        if numEOF == numListas:
            existem_mais_nomes = False
    else:
        if nome <= nome_ant:
            raise("Erro de sequencia")
    nome_ant = nome
    return nome,nome_ant,existem_mais_nomes




def kwaymerge(numListas: int)
    anteriores, nomes, listas, saida, existem_mais_nomes = inicialize()
    for i in range(numListas):
        nomes.append(valor_baixo)
    
    for i in range(numListas):
        leia_nome(listas[i],anteriores[i],existem_mais_nomes,numListas)

    while existem_mais_nomes:
        menor = 0
        for i in range(numListas):
            if nomes[i] < nomes[menor]:
                menor = i
        saida.write(nomes[menor])
        leia_nome(listas[menor],anteriores[menor]])

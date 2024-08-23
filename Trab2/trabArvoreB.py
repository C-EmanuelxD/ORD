import sys
import struct as st
import os

#big endian e inteiro de 4 bytes: >I
#big endian e inteiro de 2 bytes: >i
#little endian e inteiro de 4 bytes: <I
#little endian e inteiro de 2 bytes: <i

Ordem = 5
tamReg = (12*Ordem)-4 #Calculo do tamanho dos registros que serão escritos no arquivo btree - Usaod também para calculo do rrn
arqArv = 'btree.dat'
arqGam = 'games.dat'

class paginaArvore:
    def __init__(self) -> None:
        self.numChaves:int = 0 #Coloca o número de chaves atualmente contido na página
        self.chaves:int = [-1]*(Ordem-1) #Insere nulo para criar o vetor das chaves da página
        self.offsetsFilhos:int = [-1]*(Ordem-1) #Insere nulo para criar o vetor dos offsets das chaves da pagina
        self.filhos:int = [-1]*(Ordem) #Insere nulo para criar o vetor que referenciaa os filhos das respectivas chaves da página

###########################################Funções para escrita/leitura d arquivo########################################
def lePagina(rrn):
    offset = (tamReg*rrn)+4 #4 é do cabeçalho
    pag = paginaArvore()
    with open(arqArv, 'rb') as arq:
        arq.seek(offset)
        pag.numChaves = st.unpack('<I', arq.read(4))[0]
        for i in range(Ordem-1):
            pag.chaves[i] = st.unpack('<i', arq.read(4))[0]
        for i in range(Ordem-1):
            pag.offsetsFilhos[i] = st.unpack('<i', arq.read(4))[0]
        for i in range(Ordem):
            pag.filhos[i] = st.unpack('<i', arq.read(4))[0]
    return pag

def escrevePag(rrn, pag: paginaArvore):
    print(pag.numChaves)
    with open(arqArv, 'wb') as arq:
        offset = (tamReg*rrn)+4
        arq.seek(offset)
        pag.numChaves = st.pack("<I",pag.numChaves)
        arq.write(pag.numChaves)
        for i in range(Ordem-1):
            pag.chaves[i] = st.pack("<i",pag.chaves[i])
            arq.write(pag.chaves[i])
        for i in range(Ordem-1):
            pag.offsetsFilhos[i] = st.pack('<i', pag.offsetsFilhos[i])
            arq.write(pag.offsetsFilhos[i])
        for i in range(Ordem):
            pag.filhos[i] = st.pack('<i', pag.filhos[i])
            arq.write(pag.filhos[i])

        
            


def calcOffset(chave: int): #Função para calcular o offset da chave no arquivo games.dat
    with open(arqGam, 'rb') as arq:
        qtd_reg = st.unpack('<I',arq.read(4))[0]
        offsetPos = 4
        achou = False
        while not achou:
            print(arq.tell())
            tam = st.unpack('<h',arq.read(2))[0]
            reg = arq.read(tam).decode()
            offsetPos += tam+2
            if int(reg.split("|")[0]) == chave:
                achou = True
                offsetPos = offsetPos-(tam+2)
                return offsetPos
                
    

#######################################################################################################################  
    
############################################Funções auxiliares#########################################################
def novoRRN():
    with open(arqArv, 'rb') as arq:
        arq.seek(0, os.SEEK_END) 
        offset = arq.tell()
        return (offset - 4) // tamReg
        
    

#############################################Funções de Busca############################################################
def buscaNaPagina(chave, pag: paginaArvore):
    pos = 0
    while pos < pag.numChaves and pag.chaves[pos]:
        pos += 1
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos #se retornar verdadeiro, a chave está na página, na posição pos do vetor de chaves.
    else:
        return False, pos #Se não achar retorna falso e pos; pos é para a busca nos filhos.


def buscaNaArvore(chave, rrn):
    if rrn == -1:
        return False, -1, -1
    else:
        pag = lePagina(rrn)
        achou, pos = buscaNaPagina(chave, pag)
        
        if achou:
            return True, rrn, pos #se achar, retorna True: que achou, RRN: o rrn da página que contém a chave, e a pos em pag.chaves, na qual a chave está.
        else:
            return buscaNaArvore(chave, pag.filhos[pos])


################################################################################################################################################################

############################################## Funções referentes à inserções###################################################################################


def insereNaArvore(chave, rrnAtual): #O rrn atual na primeira chamada da inserção deve ser o rrn da raíz
    if rrnAtual == -1:
        chavePro = chave
        filhoDpro = -1
        return chavePro, filhoDpro, True
    else:
        pag = lePagina(rrnAtual)
        achou, pos = buscaNaPagina(chave, pag)
        
    if achou:
        print("Chave duplicada!")
        raise(ValueError)

    chavePro, filhoDpro, promo = insereNaArvore(chave, pag.filhos[pos])
    
    if not promo:
        return -1, -1, False
    else:
        if pag.numChaves != (Ordem-1):
            insereNaPagina(chavePro, filhoDpro, pag)
            escrevePag(rrnAtual, pag)
            return -1, -1, False
        else:
            chavePro, filhoDpro, pag, novaPag = divide(chavePro, filhoDpro, pag)
            escrevePag(rrnAtual, pag)
            escrevePag(filhoDpro, novaPag)
            return chavePro, filhoDpro, True


def insereNaPagina(chave, filhoDir, pag: paginaArvore):
    if pag.numChaves == (Ordem-1):
        pag.filhos.append(-1)
        pag.chaves.append(-1)
        pag.offsetsFilhos.append(-1)
    i = pag.numChaves
    
    while i > 0 and chave < pag.chaves[i-1]: #Liberando espaço para a nova chave
        pag.chaves[i] = pag.chaves[i-1]
        pag.offsetsFilhos[i] = pag.offsetsFilhos[i-1]
        pag.filhos[i+1] = pag.filhos[i]
        i = i-1
    
    pag.chaves[i] = chave
    pag.offsetsFilhos[i] = calcOffset(chave)
    pag.filhos[i+1] = filhoDir
    
    pag.numChaves = pag.numChaves + 1


def divide(chave, filhoDir, pag: paginaArvore):
    insereNaPagina(chave, filhoDir, pag) 
    meio = Ordem // 2 #calcula o "meio" da pagina que deve ser promovido
    chavePromo = pag.chaves[meio] 
    filhoDirPromo = novoRRN() #cria novo rrn para a nova pagina criada
    pAtual = paginaArvore()
    pNova = paginaArvore()
    #divide as paginas:
    pAtual.numChaves = meio
    pAtual.chaves = pag.chaves[:meio]
    pAtual.offsetsFilhos = pag.offsetsFilhos[:meio]
    pAtual.filhos = pag.filhos[:meio+1]
    #O ERRO ESTÁ NA HORA DE INSERIR COM [:MEIO], O RESTO DO VETOR VAI EMBORA E FICA APENAS OS INSERIDOS
    pNova.numChaves = Ordem-1-meio
    pNova.chaves = pag.chaves[meio+1:]
    pNova.offsetsFilhos = pag.offsetsFilhos[meio+1:]
    pNova.filhos = pNova.filhos[meio+1:]
    
    return chavePromo, filhoDirPromo, pAtual, pNova    
    

"""""def criaIndice(): #Função responsável por criar a árvore completa do arquivo games.dat
    primeiraPag = paginaArvore()
    escrevePag(0, primeiraPag) #Primeira pagina criada
    
    #Agora a obtenção e inserção das chaves na árvore
    
    with open(arqGam, 'rb') as arq:
        qtd_reg = st.unpack('<I',arq.read(4))[0]
        for i in range(qtd_reg):
            tam = st.unpack('<h',arq.read(2))[0]
            reg = arq.read(tam).decode()
            chave = int(reg.split("|")[0])
            insereNaArvore(chave, 0)"""""


def percorreRegs(arq) -> int: #Retorna a próxima chave
    tam = st.unpack('<h',arq.read(2))[0]
    reg = arq.read(tam).decode()
    chave = int(reg.split("|")[0])
    try:
        return chave, True
    except:
        return -1, False


def gerenciadorDeIsercao(raiz):
    with open(arqGam, 'rb') as arq:
        arq.read(4)
        chave, terminou = percorreRegs(arq)
        while terminou:
            chavePro, filhoDpro, promo = insereNaArvore(chave, raiz)
            if promo:
                pNova = paginaArvore()
                pNova.chaves[0] = chavePro
                pNova.offsetsFilhos[0] = calcOffset(chavePro)
                pNova.filhos[0] = raiz
                pNova.filhos[1] = filhoDpro
                pNova.numChaves += 1
                pNovaRRN = novoRRN()
                escrevePag(pNovaRRN, pNova)
                raiz = pNovaRRN
            chave, terminou = percorreRegs(arq)

    return raiz

def principal():
    try:
        with open(arqArv, 'rb+')as arqArvb:
            raiz = st.unpack('<I', arqArvb.read(4))[0]
    except:
        with open(arqArv, 'wb+') as arqArvb:
            raiz = st.pack("<I", 0)
            arqArvb.seek(0)
            arqArvb.write(raiz)
            pag = paginaArvore()
            raiz = st.unpack('<I', raiz)[0]
            escrevePag(raiz,pag)

        raiz = gerenciadorDeIsercao(raiz)
        raiz = st.pack("<I", raiz)
        arqArvb.seek(0)
        arqArvb.write(raiz)









        

"""if sys.argv[1] == '-c':
    print("===========================")
    print("Modo de criação da árvore-B")
    print("===========================")
    principal()#Cria indice encadeia funções de inserção da árvore, para a inserção de diversas chaves
        
elif sys.argv[1] == '-e':
    print("============================")
    print("Modo do Arquivo de operações")
    print("============================")
    
elif sys.argv[1] == '-p':
    print("=============================")
    print("Modo de impressão da Árvore-B")
    print("=============================")
    
else:
    print("Flag inválida. Encerrando...")"""

principal()

    

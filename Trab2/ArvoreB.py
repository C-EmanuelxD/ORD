import sys
import struct as st
import os
#Criação da constante de ordem da árvore
Ordem = 5

#calculo do tamanho do registro baseado na Ordem
tamRegbtree = (12*Ordem)-4 

#Nome dos arquivos
ArqG = "games.dat"
ArqARVORE = "btree.dat"

#Criação de variavel global do RRN da pagina raíz, já que ele pode ser alterado pelo código
rrnRaiz = -1

class paginaArvore:
    def __init__(self) -> None:
        self.numChaves:int = 0 #Coloca o número de chaves atualmente contido na página
        self.chaves:int = [-1]*(Ordem-1) #Insere nulo para criar o vetor das chaves da página
        self.offsetsFilhos:int = [-1]*(Ordem-1) #Insere nulo para criar o vetor dos offsets das chaves da pagina
        self.filhos:int = [-1]*(Ordem) #Insere nulo para criar o vetor que referenciaa os filhos das respectivas chaves da página
        

def LePagina(RRN:int) -> paginaArvore: #Retorna o objeto pag
    offset = 4 + (RRN * tamRegbtree) #Busca o offset baseado no RRN
    pag = paginaArvore() #cria o objeto paginaArvore
    with open(ArqARVORE, "rb") as arq: #abre o arquivo em modo de leitura binaria
        arq.seek(offset) #busca o offset marcado na variavel offset
        pag.numChaves = st.unpack('<i',arq.read(4))[0] #guarda os primeiros 4 bytes do "registro", que é o numero de chaves, utilizando do st.unpack com a flag i - unsigned int de 4b e > - big endian
        for i in range(Ordem-1): #itera no valor Ordem-1, para inserir todas as chaves do arquivo em pag
            pag.chaves[i] = st.unpack('>i',arq.read(4))[0]
        for i in range(Ordem-1): #itera no valor Ordem-1, para inserir todas os offsets das chaves em pag
            pag.offsetsFilhos[i] = st.unpack('>i',arq.read(4))[0]
        for i in range(Ordem): #itera no valor Ordem, para inserir todas os filhos de cada valor
            pag.filhos[i] = st.unpack('>i',arq.read(4))[0]
            
    return pag

def escrevePagina(RRN:int, pag:paginaArvore): #Escreve a página no arquivo btree.dat
    if RRN == -1:
        offset = 4
    else:
        offset = 4 + (RRN*tamRegbtree)
    with open(ArqARVORE, "wb") as arq:
        arq.seek(offset)
        arq.write(st.pack('>i',pag.numChaves))
        for i in range(Ordem-1): 
            print(pag.chaves[i])
            arq.write(st.pack('>i',pag.chaves[i]))
        for i in range(Ordem-1): 
            arq.write(st.pack('>i',pag.offsetsFilhos[i]))
        for i in range(Ordem): 
            arq.write(st.pack('>i',pag.filhos[i]))

def novoRRN():
    with open(ArqARVORE, "wb") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        return (offset - 4) // tamRegbtree

def calcOffset(chave):
    achou = False
    with open(ArqG, 'rb') as arq:
        offset = 4
        arq.read(4)
        while arq and not achou:
            tam = st.unpack('<h', arq.read(2))[0]
            reg = arq.read(tam).decode()
            if int(reg.split("|")[0]) == chave:
                achou = True
                offset += 2
            else:
                achou = False
                offset += 2
        return offset
        

def insereNaPag(chave, filhoDir, pag: paginaArvore):
    if pag.numChaves == (Ordem-1):
        pag.filhos.append(None)
        pag.chaves.append(None)
    i = pag.numChaves
    while i > 0 and chave < pag.chaves[i-1]:
        pag.chaves[i] = pag.chaves[i-1]
        pag.offsetsFilhos[i] = pag.offsetsFilhos[i-1]
        pag.filhos[i+1] = pag.filhos[i]
        i = i-1
    pag.chaves[i] = chave
    pag.offsetsFilhos[i] = calcOffset(chave)
    pag.filhos[i+1] = filhoDir
    pag.numChaves += 1

def divide(chave, filhoD, pag: paginaArvore):
    insereNaPag(chave, filhoD, pag)
    pAtual = paginaArvore()
    pNova = paginaArvore()
    meio = Ordem // 2
    chavePromo = pag.chaves[meio]
    filhoDirPromo = novoRRN()
    for i in range(meio):
        pAtual.chaves[i] = pag.chaves[i]
        pAtual.filhos[i] = pag.filhos[i]
        pAtual.offsetsFilhos[i] = pag.offsetsFilhos[i]
        pAtual.numChaves += 1
    for i in range(meio+1, Ordem-1):
        pNova.chaves[i] = pag.chaves[i]
        pNova.filhos[i] = pag.filhos[i]
        pNova.offsetsFilhos[i] = pag.offsetsFilhos[i]
        pNova.numChaves += 1
    return chavePromo, filhoDirPromo, pAtual, pNova
        


    
def buscanaArvore(chave: int, rrn:int): #RRN DEVE SER O RRN DA PAGINA RAIZ SEMPRE QUE ESSA FUNÇÃO FOR CHAMADA
    if rrn == -1:
        return False, None, None
    else:
        pag = LePagina(rrn) #Recebe a página do rrn em pag. Obs.: como é verificado antes se rrn = -1, nunca entrará -1 nessa função
        achou, pos = buscaNaPagina(chave, pag) #busca dentro da pagina a chave

        if achou:
            return True, rrn, pos #se achar retorna os valores para a recursão ou fim dela
        else:
            return buscanaArvore(chave, pag.filhos[pos]) #senão entra na recursão do RRN do filho da pagina especificada em pos
  
      
        
        
def buscaNaPagina(chave: int, pag: paginaArvore): #Retorna a posição da chave se achou, senão retorna que não achou e a posição, para busca no filho
    pos:int = 0
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos = pos + 1
    if pos < pag.numChaves and chave == pag.chaves[pos]: #se pos ainda estiver dentro do intervalo de numChaves E chave for achada dentro de pag.chaves, a chave existe
        return True, pos #Retorna true (achou) e a posição da chave dentro de pag.chaves
    else:
        return False, pos #Retorna false (não achou) e a posição onde a iteração do while parou, para se encontrar o filho que pode conter a chave.

    
def insereNaArvore(chave, rrnAtual): #Função de inserção na árvore
    if rrnAtual == -1:
        chavePro = chave
        filhoDpro = -1
        return chavePro, filhoDpro, True
    else:
        pag = LePagina(rrnAtual)
        achou, pos = buscaNaPagina(chave, pag)
    
    if achou:
        print("CHAVE DUPLICADA. ERRO!")
        raise(ValueError)
    
    chavePro, filhoDpro, promo = insereNaArvore(chave, pag.filhos[pos])
    if not promo:
        return -1, -1, False
    else:
        if pag.numChaves != (Ordem-1):
            insereNaPag(chavePro, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            return -1, -1, False
        else:
            chavePro, filhoDpro, pag, novapag = divide(chavePro, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            escrevePagina(novapag, filhoDpro)
            return chavePro, filhoDpro, True


def gerenciadorDeInsercao(rrnRaiz, chave: int):
    chavePro, filhoDpro, promocao = insereNaArvore(chave, rrnRaiz)
    if promocao: #Criar nova pag raiz
        print("RESTO")
        pNova = paginaArvore()
        pNova.chaves[0] = chavePro
        pNova.offsetsFilhos[0] = calcOffset(chavePro)
        pNova.filhos[1] = filhoDpro
        pNova.numChaves += 1
        rrnRaiz = novoRRN()
        escrevePagina(rrnRaiz, pNova)
    return rrnRaiz


def criaIndice():
    global rrnRaiz
    with open(ArqG, 'rb') as arqG:
        qtd_Reg = st.unpack('>i', arqG.read(4))[0]
        for i in range(qtd_Reg-1):
            cab = i
            cab = cab.to_bytes(4)
            arq = open(ArqARVORE, 'wb')
            arq.write(cab)
            arq.close()
            tam = st.unpack('<h', arqG.read(2))[0]
            reg = arqG.read(tam)
            reg = reg.decode()
            rrnRaiz = gerenciadorDeInsercao(rrnRaiz, int(reg.split("|")[0]))


criaIndice()

if sys.argv[1] == '-c':
    print("===========================")
    print("Modo de criação da árvore-B")
    print("===========================")
    criaIndice()
        
elif sys.argv[1] == '-e':
    print("============================")
    print("Modo do Arquivo de operações")
    print("============================")
    
elif sys.argv[1] == '-p':
    print("=============================")
    print("Modo de impressão da Árvore-B")
    print("=============================")
    
else:
    print("Flag inválida. Encerrando...")
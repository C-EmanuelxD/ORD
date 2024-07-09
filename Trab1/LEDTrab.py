import sys
import os
arqG = "dados.dat"
##FUNÇÃO DE LEITURA DE OPERAÇÕES###########################
def leOperacoes(nomeArqOP: str):
    ArqOP = open(nomeArqOP,'r')
    linha = ArqOP.readline()
    while linha:
        char = linha.split(sep=" ")
        linha = ArqOP.readline()
        if char[0] == "b":
            Identificador = char[1]
            print(f"Busca pelo registro de chave {Identificador}")
            BuscaPorID(Identificador, arqG)
            
        elif char[0] == "i":
            print("INSERÇÃO")
            
        elif char[0] == "r":
            Identificador = char[1]
            print(f"Remoção do registro de chave {Identificador}")
            RemoverReg(Identificador,arqG)
            
            
###########################################################

def RemoverReg(Id: str, arqG: str):
    arq = open(arqG, "rb+")
    cabLED = VerCabeca(arqG)
    print(cabLED)
        

















###Função de leitura do cabeçalho e tratamento de erro#######

def VerCabeca(arq:str):
    arq = open(arqG,"rb+")
    c = arq.read(4)
    if c == 0xffffffff:
        print("smt")



##Calculo de Offset################################
def calcOffset(Id:str, arq:str) -> int:
    arq = open(arq,"rb")
    Id = int(Id)-1
    achou = False
    arq.read(4)
    offsetPos = 4
    while arq and not achou:
        reg, tam = leia_reg(arq)
        offsetPos += tam+2
        if int(reg.split(sep="|")[0]) == Id:
            achou = True
    arq.close()
    return offsetPos
#################################################









##FUNÇÃO DE BUSCA POR IDENTIFICAÇÃO##
def BuscaPorID(ID:str, arq:str):
    try:
        entrada = open(arq,'rb+')
        chave = int(ID)
        achou = False
        entrada.read(4)
        reg, tamBytes = leia_reg(entrada)
        while reg != "" and not achou:
            
            sobrenome = int(reg.split(sep="|")[0])
            if sobrenome == chave:
                achou = True
            else:
                reg,tamBytes = leia_reg(entrada)
                
                
        if achou:
            print(reg+f" ({tamBytes} Bytes)\n")
        else:
            print("Identificador nao encontrado")
        entrada.close()

    except FileNotFoundError:
        print("Erro!!")
        print("Finalizando o programa!")
        exit(0)

#######################################

##FUNÇÃO DE LEITURA DOS REGISTROS################

def leia_reg(arq) -> str:
    try:
        tam = int.from_bytes(arq.read(2))
        if tam > 0:
            s = arq.read(tam)
            return s.decode(), tam
        return ''
    except OSError as e:
        print(f'Erro leia_reg: {e}')

#################################################

if sys.argv[1] == "-e":
    print("==================")
    print("MODO DE OPERAÇÕES")
    print("==================")
    leOperacoes(sys.argv[2])

elif sys.argv[1] == "-p":
    print("================")
    print("EXIBIÇÃO DA LED")
    print("================")
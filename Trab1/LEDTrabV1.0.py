import sys
import os
import struct

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

####FUNÇÃO DE ADICIONAR NA LED####################################################
def adicionar_na_led(offset, tam):
    arq = open(arqG, "rb+")
    cabecaLED = 0
    if cabecaLED.from_bytes(arq.read(4), byteorder='big', signed=True) == -1:
        arq.seek(0)
        offset = offset.to_bytes(4)
        arq.write(offset)
    else:
        ponteroLED, pontero_Anterior = compararTamLed(tam)
        
        if ponteroLED == -1: #Tem que ser adicionado no final
            arq.seek(offset+3)
            ponteroLED = ponteroLED.to_bytes(4, byteorder='big', signed=True)
            arq.write(ponteroLED)
            arq.seek(pontero_Anterior+3)
            offset = offset.to_bytes(4, byteorder='big', signed=False)
            arq.write(offset)
            arq.close()
        else:
                arq.seek(offset+3)
                ponteroLED = ponteroLED.to_bytes(4, byteorder='big', signed=False)
                arq.write(ponteroLED)
                if pontero_Anterior != 0:
                    arq.seek(pontero_Anterior+3)
                else:
                    arq.seek(pontero_Anterior)
                offset = offset.to_bytes(4,byteorder='big',signed=False)
                arq.write(offset)
####################################################

####### FUNÇÃO DE PERCORRER E COMPARAR NO TAMANHO DA LED (DESNECESSARIA ATE CERTO PONTO)#############
def compararTamLed(tam):
    arq = open(arqG, "rb+")
    ponteroLED = struct.unpack('!i', arq.read(4))[0]
    arq.seek(ponteroLED)
    reg, tamPontero = leia_reg(arq) #aqui eu ja sei que é menor       
    while ponteroLED != -1:
        arq.seek(ponteroLED)
        reg, tamPontero = leia_reg(arq)
        if tam > tamPontero:
            try:
                return ponteroLED, pontero_Anterior
            except UnboundLocalError: ##SE NÃO TEM NADA ANTERIORMENTE ENTÃO A CABEÇA É O ANTERIOR
                return ponteroLED, 0
        pontero_Anterior = ponteroLED #Ponteiro anterior a leitura do -1 ou menor
        arq.seek(ponteroLED+3) #ir até o prox ponteiro
        ponteroLED = struct.unpack('!i', arq.read(4))[0] #pega o offset do proximo
    return -1, pontero_Anterior
  ##########################################################################################          
            
            
def RemoverReg(Id: str, arqG: str):
    offset = calcOffset(Id, arqG)
    if offset == -1:
        print("Este registro nao foi encontrado")
    else:
        arq = open(arqG, "rb+")
        arq.seek(offset)
        tam = int.from_bytes(arq.read(2), byteorder='big', signed=False)
        print(f"Registro removido! ({tam} bytes)")
        tam = tam.to_bytes(2)
        registro = "*"
        registro = registro.encode()
        teste = -1
        teste = teste.to_bytes(4, byteorder='big', signed=True)
        tudo_junto = tam + registro + teste
        arq.seek(offset)
        arq.write(tudo_junto)
    arq.close()
    
    tam = int.from_bytes(tam, byteorder='big', signed=False)
    print(f"Local: Offset = {offset} bytes ({hex(offset)})\n")
    adicionar_na_led(offset, tam)





##Calculo de Offset################################
def calcOffset(Id:str, arq:str) -> int:
    try:
        arq = open(arq,"rb")
        Id = int(Id)-1
        achou = False
        arq.read(4)
        offsetPos = 4
        while arq and not achou:
            reg, tam = leia_reg(arq)
            if Id == 0:
                return offsetPos
            offsetPos += tam+2
            try:
                if int(reg.split(sep="|")[0]) == Id:
                    achou = True
            except ValueError: #Ignorando as leituras de números hexadecimais.
                achou = False
        arq.close()
        
        return offsetPos
    except FileNotFoundError:
        return -1
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
            print("sla")
            try:
                sobrenome = int(reg.split(sep="|")[0])
                if sobrenome == chave:
                    achou = True
                else:
                    reg,tamBytes = leia_reg(entrada)
            except ValueError or UnicodeDecodeError: #iGNORANDO A LEITURA DE NUMEROS HEXADECIMAIS E PARTINDO PARA O PROXIMO
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
            try:
                return s.decode(), tam
            except:
                return ('404|ERRO'), (tam)
            
        return '', 0
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
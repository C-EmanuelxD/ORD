import sys
import os
import struct

#VARIAVEIS GLOBAIS
arqG = "dados.dat"
tamMinimoSobra = 10 

##FUNÇÃO DE LEITURA DE OPERAÇÕES###########################
def leOperacoes(nomeArqOP: str):
    ArqOP = open(nomeArqOP,'r')
    linha = ArqOP.readline()
    while linha:
        linhaInsercao = linha
        char = linha.split(sep=" ")
        linha = ArqOP.readline()
        if char[0] == "b":
            Identificador = char[1]
            print(f"Busca pelo registro de chave {Identificador}")
            b, reg = BuscaPorID(Identificador, arqG)
            print(reg)
            
        elif char[0] == "i":
            char = char[1].split(sep="|")
            Identificador = char[0]
            Insercao(linhaInsercao, arqG)
            
        elif char[0] == "r":
            Identificador = char[1]
            print(f"Remoção do registro de chave {Identificador}")
            RemoverReg(Identificador,arqG)

###########################################################

def Insercao(linhaInsercao, arqG):
    arq = open(arqG, "rb+")
    linhaInsercao = linhaInsercao.removeprefix('i') #TIRA O "I" DO REGISTRO QUANDO LE
    linhaInsercao = linhaInsercao.removeprefix(' ') #TIRA O " " DO REGISTRO 
    linhaInsercao = linhaInsercao.removesuffix("\n") #TIRA O /n DO FIM DO REGISTRO
    tam = len(linhaInsercao) #PEGA DO TAMANHO DO REGISTRO A SER INSERIDO
    char = linhaInsercao.split(sep="|")
    Identificador = char[0]
    print(f"Inserção do registro de chave: {Identificador} ({tam} bytes)")

    #print(f"Registro adicionado: {linhaInsercao}")
    offset = struct.unpack('!i', arq.read(4))[0] #PEGAR A CABEÇA
    
    if offset == -1: #SE A CABECA DA LED FOR -1 ELE ENTRA DIRETO NESSA FUNACAO E ADICIONA O REGISTRO NO FIM DO ARQUIVO
        InsercaoNoFim(linhaInsercao, tam, arqG)
    else:
        arq.seek(offset)
        tamOffset = int.from_bytes(arq.read(2), byteorder='big', signed=False) #TAMANHO DO REGISTRO REMOVIDO A SER SUBESCRITO
        arq.seek(offset+3)
        ponteroLED = arq.read(4) #PEGOU ONDE O REGISTRO REMOVIDO A SER SUBESCRITO APONTAVA

        if tam > tamOffset: #SE O TAMANHO DO REGISTRO NOVO A SER INSERIDO FOR MAIOR QUE O TAMANHO DISPONIVEL SO INSERIR NO FIM
            InsercaoNoFim(linhaInsercao, tam, arqG)
        else:
            #escreve o registro no local indicado
            linhaInsercao = linhaInsercao.encode()
            tam = tam.to_bytes(2)
            arq.seek(offset)
            arq.write(tam)
            arq.write(linhaInsercao)
            print(f"Local: Offset = {offset} bytes ({hex(offset)})")
            tam = int.from_bytes(tam, byteorder='big', signed=False)
            posicaoPontero = arq.tell()
            #escreve nos cabecalho o proximo da led
            arq.seek(0)
            arq.write(ponteroLED)
        
            #ENTRA NO IF PARA MOSTRAR O TAMANHO REUTILIZADO E O TAMANHO DA SOBRA
            if tamOffset > tam:
                tamSobra = tamOffset-tam
                print(f"Tamanho reutilizado {tamOffset}. (Sobra de {tamOffset-tam} bytes)")
                tamOffset = tamOffset-tam-2#O -2 ESTA AQUI POR CONTA QUE O TAMANHO DISPONIVEL NAO LEVA EM CONTA OS 2 BYTES INICIAIS || CALCULO DO TAM DA SOBRA
                #ADICIONA A SOBRA NA LED NOVAMENTE
                if tamOffset > tamMinimoSobra:#TEM QUE ADICIONAR A SOBRA NO ROLE####
                    tamOffset = tamOffset.to_bytes(2) #tamOffset agora é o tamanho do novo registro (sobra)
                    registro = "*"
                    registro = registro.encode()
                    teste = -1
                    teste = teste.to_bytes(4, byteorder='big', signed=True)
                    tudo_junto = tamOffset + registro + teste
                    arq.seek(posicaoPontero)
                    arq.write(tudo_junto)
                    arq.close()
                    tamOffset = int.from_bytes(tamOffset, byteorder='big', signed=False)
                    adicionar_na_led(posicaoPontero, tamOffset)
                else:
                    print(f"Não atingiu o tamanho minimo para ser adicionado na LED, portanto será considerado fragmentação de: ({tamSobra} bytes)")
                    #nova parte
                    arq.seek(offset)
                    tamReg = arq.read(2)
                    tamReg = int.from_bytes(tamReg, byteorder='big', signed=False)
                    tamComFrag = tamReg+tamSobra
                    tamComFrag = tamComFrag.to_bytes(2)
                    arq.seek(offset)
                    arq.write(tamComFrag)
                    
                    #FIM NOVA PARTE
                    #ADICIONAR ESSA SOBRA NO TAMANHO DO REGISTRO
            print("\n")

    arq.close()
######################################################################################################

#FUNCAO DE INSERCAO NO FIM
def InsercaoNoFim(linhaInsercao, tam, arqG):
        arq = open(arqG, "rb+")
        linhaInsercao = linhaInsercao.encode()
        tam = tam.to_bytes(2)
        arq.seek(0, os.SEEK_END)#VAI ATE O FIM DO ARQUIVO
        arq.write(tam)#ESCREVE O TAMANHO DO REGISTRO NOS PRIMEIROS 2 BYTES
        arq.write(linhaInsercao)#ESCREVE O REGISTRO DEPOIS DO TAMANHO
        arq.close()
        print("Adicionado no fim do arquivo.\n")

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
            arq.seek(offset+3) #offset +3 para adicionar o -1
            ponteroLED = ponteroLED.to_bytes(4, byteorder='big', signed=True)
            arq.write(ponteroLED) #escreveu o -1
            arq.seek(pontero_Anterior+3) #ir para o anterior na LED
            offset = offset.to_bytes(4, byteorder='big', signed=False)
            arq.write(offset) #Escrever o offset na LED
            arq.close()
        else:
            arq.seek(offset+3)
            ponteroLED = ponteroLED.to_bytes(4, byteorder='big', signed=False)
            arq.write(ponteroLED)#escreve o proximo da LED
            if pontero_Anterior != 0: # vai escrever no offset anterior o offset a adicionar
                arq.seek(pontero_Anterior+3)
            else: #vai escrever no cabecalho o offset "atual" (ou a adicionar)
                arq.seek(pontero_Anterior)
            offset = offset.to_bytes(4,byteorder='big',signed=False)
            arq.write(offset)#escreveu no offset nterior (cabeça ou anterior na LED)
            arq.close()

####################################################

####### FUNÇÃO DE PERCORRER E COMPARAR NO TAMANHO DA LED (DESNECESSARIA ATE CERTO PONTO)#############
def compararTamLed(tam):
    arq = open(arqG, "rb+")
    ponteroLED = struct.unpack('!i', arq.read(4))[0]
    arq.seek(ponteroLED)
    reg, tamPontero = leia_reg(arq) #aqui eu ja sei que é menor       
    while ponteroLED != -1:
        arq.seek(ponteroLED) #memso que o de cima!
        reg, tamPontero = leia_reg(arq) #tamPonteiro é o tam do proximo na LED
        if tam >= tamPontero: # se achar um lugar que da igual ou menor ele retorno ambos e dai faz o gerenciemnto de um apontar para o proximo
            try:
                arq.close()
                return ponteroLED, pontero_Anterior
            except UnboundLocalError: ##SE NÃO TEM NADA ANTERIORMENTE ENTÃO A CABEÇA É O ANTERIOR
                arq.close()
                return ponteroLED, 0
        pontero_Anterior = ponteroLED #Ponteiro anterior a leitura do -1 ou menor
        arq.seek(ponteroLED+3) #ir até o prox ponteiro
        ponteroLED = struct.unpack('!i', arq.read(4))[0] #pega o offset do proximo
    arq.close()
    return -1, pontero_Anterior

##########################################################################################          
            
def RemoverReg(Id: str, arqG: str):
    if BuscaPorID(Id, arqG)[0] == True:
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
    else:
        print("ERRO: Registro não encontrado ou já removido!\n")

##Calculo de Offset################################
def calcOffset(Id:str, arq:str) -> int:
    try:
        arq = open(arq,"rb")
        Id = int(Id)
        achou = False
        arq.read(4)
        offsetPos = 4
        while arq and not achou:
            reg, tam = leia_reg(arq)
            offsetPos += tam+2
            try:
                if int(reg.split(sep="|")[0]) == Id:
                    offsetPos = offsetPos-(tam+2)
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
            try:
                sobrenome = int(reg.split(sep="|")[0])
                if sobrenome == chave:
                    achou = True
                else:
                    reg,tamBytes = leia_reg(entrada)
            except ValueError or UnicodeDecodeError: #iGNORANDO A LEITURA DE NUMEROS HEXADECIMAIS E PARTINDO PARA O PROXIMO
                reg,tamBytes = leia_reg(entrada)
        if achou:
            entrada.close()
            return True, reg+f" ({tamBytes} Bytes)\n"
        else:
            entrada.close()
            return False, "Não encontrado!"
        

    except FileNotFoundError:
        print("Erro: Arquivo não encontrado!!")
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

####FUNÇÃO DE EXIBIR A LED##############
def exibirLED():
    arq = open(arqG, "rb")
    offset = struct.unpack('!i', arq.read(4))[0]
    if offset == -1:
        print("LED ESTÁ VAZIA...")
        print(f"total de espaços disponíveis: 0")
    else:
        cont = 0
        print(f"LED ", end='')
        while offset != -1:
            cont += 1
            arq.seek(offset)
            tam = int.from_bytes(arq.read(2), byteorder='big', signed=False)
            print(f" -> [offset: {offset}, tamanho: {tam}]", end='')
            arq.read(1)
            offset = struct.unpack('!i', arq.read(4))[0]
        print("-> [offset: -1]")
        print(f"total de espaços disponíveis: {cont}")
               
try:
    arq = open(arqG, 'rb')
    arq.close()
except:
    print(f"arquivo {arqG} não existe ou não está no diretorio {os.getcwd()}!")
    exit(0)

if sys.argv[1] == "-e":
    leOperacoes(sys.argv[2])

elif sys.argv[1] == "-p":
    exibirLED()
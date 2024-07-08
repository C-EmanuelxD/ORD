import sys

##FUNÇÃO DE LEITURA DE OPERAÇÕES##
def leOperacoes(nomeArqOP: str):
    ArqOP = open(nomeArqOP,'r')
    linha = ArqOP.readline()
    char = linha.split(sep=" ")
    if char[0] == "b":
        Identificador = char[1]
        print(Identificador)
        BuscaPorID(Identificador, "dados.dat")
        
        
    elif char == "i":
        print("pprt")
        
    elif char == "r":
        print("pprt")    
###########################################################
    
##FUNÇÃO DE BUSCA POR IDENTIFICCAÇÃO##

def BuscaPorID(ID:str, arq:str):
    try:
        entrada = open(arq,'rb+')
        chave = int(ID)
        achou = False
        entrada.read(4)
        reg = leia_reg(entrada)
        while reg != "" and not achou:
            sobrenome = int(reg.split(sep="|")[0])
            if sobrenome == chave:
                achou = True
            else:
                reg = leia_reg(entrada)
                
                
        if achou:
            sobrenome = reg.split(sep="|")
            i = 0
            for campo in sobrenome:
                i += 1
                print(f"{i}º:"+campo)
        else:
            print("Sobrenome nao encontrado")
        entrada.close()

    except FileNotFoundError:
        print("Erro!!")
        print("Finalizando o programa!")
        exit(0)

#######################################

##FUNÇÃO DE LEITURA DOS REGISTROS##

def leia_reg(arq) -> str:
    try:
        tam = int.from_bytes(arq.read(2))
        if tam > 0:
            s = arq.read(tam)
            return s.decode()
        return ''
    except OSError as e:
        print(f'Erro leia_reg: {e}')

#####################################

if sys.argv[1] == "-e":
    print("==================")
    print("MODO DE OPERAÇÕES")
    print("==================")
    leOperacoes(sys.argv[2])

elif sys.argv[1] == "-p":
    print("================")
    print("EXIBIÇÃO DA LED")
    print("================")
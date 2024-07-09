
name = input("escreva o nome a ser lido: ")
try:
    entrada = open(name,"r")

except:
    print("ERRO")
    exit()


def leia_campo(entrada):
    campo = ""
    c = entrada.read(1)
    while c != "" and c != "|":
        campo= campo+c
        c = entrada.read(1)
    
    return campo

campo = leia_campo(entrada)
while campo != "":
    print(campo)
    campo = leia_campo(entrada)

entrada.close()
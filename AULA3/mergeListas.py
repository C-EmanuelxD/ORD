import io

valor_baixo=""
valor_alto="~"

def inicialize():
    ant1 = valor_baixo
    ant2 = valor_baixo

    lista1 = open("lista1.txt","r")
    lista2 = open("lista2.txt","r")
    saida = open("merge.txt","w")
    existem_mais_nomes = True
    return ant1,ant2,lista1,lista2,saida,existem_mais_nomes

def leia_nome(lista: io.TextIOWrapper, nome_ant:str,nome_outra_lista:str, existem_mais_nomes:bool):
    nome = lista.readline()
    if nome == "":
        if nome_outra_lista == valor_alto:
            existem_mais_nomes = False
        else:
            nome = valor_alto
    elif nome <= nome_ant:
        print(f"Erro de sequencia - {nome} - {nome_ant}")
        raise('Erro de sequencia')
    nome_ant = nome
    return nome, nome_ant, existem_mais_nomes





def merge():
    anterior1,anterior2,lista1,lista2,saida,existem_mais_nomes = inicialize()
    nome1, anterior1, existem_mais_nomes = leia_nome(lista1,anterior1,anterior2,existem_mais_nomes)
    nome2, anterior2, existem_mais_nomes = leia_nome(lista2,anterior2, anterior1, existem_mais_nomes)
    while existem_mais_nomes:
        if nome1<nome2:
            saida.write(nome1)
            nome1, anterior1, existem_mais_nomes = leia_nome(lista1,anterior1,anterior2,existem_mais_nomes)
        elif nome1>nome2:
            saida.write(nome2)
            nome2, anterior2, existem_mais_nomes = leia_nome(lista2,anterior2, anterior1, existem_mais_nomes)
        else:
            saida.write(nome1)
            nome1, anterior1, existem_mais_nomes = leia_nome(lista1,anterior1,anterior2,existem_mais_nomes)
            nome2, anterior2, existem_mais_nomes = leia_nome(lista2,anterior2, anterior1, existem_mais_nomes)

    saida.close()
    lista1.close()
    lista2.close()

if __name__ == "__main__":
    merge()
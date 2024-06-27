def main():
    Nome_Arq = input("Qual o arquivo a ser aberto?")
    try:
        entrada = open(Nome_Arq,"rb")
    except FileNotFoundError:
        print("Erro!")
        exit(0)


    cab = entrada.read(4)
    total_reg = int.from_bytes(cab)
    rrn = int(input("Qual o numero RRN a ser lido: "))
    if rrn >= total_reg:
        print("Erro, numero de registro inválido!")
    offset = rrn*64+4 #rrn*tam_reg+tam_cabeçalho
    entrada.seek(offset)
    
    reg = entrada.read(64)
    reg = reg.decode()
    reg = reg.split(sep="|")
    for campo in reg:
        print(campo)
        if campo == "\0" or campo == "0":
            exit(0)


if __name__ == "__main__":
    main()
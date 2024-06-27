def main():
    NomeArq = input("Escreva o nome do arquivo:")
    
    try:
        entrada = open(NomeArq,"rb")
        buffer = leReg(entrada)
        while buffer != "":
            lista = []
            lista = buffer.split(sep="|")
            for i in lista:
                print(i)
            buffer = leReg(entrada)
        entrada.close()
    except:
        print(FileNotFoundError)
        exit(0)



def leReg(entrada):
    tam = entrada.read(2)
    tam = int.from_bytes(tam)
    if tam > 0:
        print(tam)
        buffer = entrada.read(tam)
        buffer = buffer.decode()
        return buffer
    else:
        return ""
    

if __name__ == "__main__":
    main()
def main():
    nomeArq = input("Escreva o nome do arquivo:")
    saida = open(nomeArq,"wb")
    campo = input("Escreva o sobrenome:")
    while campo != "":
        buffer = ""
        buffer = campo+"|"
        for i in range(5):
            campo = input(f"Coloque o {i+2} campo:")
            buffer += campo+"|"
        buffer = buffer.encode()
        tam = len(buffer)
        tam = tam.to_bytes(2)

        saida.write(tam)
        saida.write(buffer)

        campo = input("Se quiser gravar outro nome, escreva, senão, apenas ENTER:")
    saida.close()

if __name__ == "__main__":
    main()
def main():
    name = input("Escreva o nome do arquivo: ")
    try:
        arq = open(name, "r")
        arqfim = open("arqfim",'w')
        c = arq.read(1)
        while c:
            if c == " ":
                arqfim.write(c)
                c = arq.read(1)
                while c == " ":
                    c = arq.read(1)
            arqfim.write(c)
            c = arq.read(1)
        arq.close()
        arqfim.close()
    except FileNotFoundError:
        raise(FileNotFoundError)



if __name__ == "__main__":
    main()
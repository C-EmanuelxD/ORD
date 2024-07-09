def main():
    name = input("Escreva o nome do arquivo")
    try:
        arq = open(name,'rb')
        numLinha = 0
        numBytes = 0
        c = arq.read(1)
        while c:
            c = arq.read(1)
            if c == b"\n":
                numLinha += 1
            numBytes += 1
        numLinha+=1
        print(f"O número de bytes é: {numBytes}")
        print(f"O número de linhas é: {numLinha}") 
        
    except FileNotFoundError:
        raise(FileNotFoundError)






if __name__ == "__main__":
    main()
def main():
    Nome_Arq = input("Qual o nome a ser encontrado?")
    try:
        entrada = open(Nome_Arq,'rb')
        chave = input("Qual o sobrenome a ser buscado? ")
        achou = False
        reg = leia_reg(entrada)
        while reg != "" and not achou:
            sobrenome = reg.split(sep="|")[0]
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




def leia_reg(arq) -> str:
    try:
        tam = int.from_bytes(arq.read(2))
        if tam > 0:
            s = arq.read(tam)
            return s.decode()
        return ''
    except OSError as e:
        print(f'Erro leia_reg: {e}')




if __name__ == '__main__':
    main()
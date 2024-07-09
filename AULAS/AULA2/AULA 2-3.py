def main():
    nome_arq = input("Qual o nome do arquivo? ")
    
    try:
        arq = open(nome_arq,"r+b")
        total_reg = arq.read(4)
        total_reg = int.from_bytes(total_reg)
        busca_e_att(arq, total_reg)
    except FileNotFoundError:
        print("Arquivo nao existe!")
        print("Deseja criar um novo?")
        esc = input("S/N: ")

        if esc == 'S':
            arq = open(nome_arq,'w+b')
            total_reg = 0
            total_reg = total_reg.to_bytes(4)
            arq.write(total_reg)
            total_reg = 0
            busca_e_att(arq, total_reg)
        else:
            exit(0)

def busca_e_att(arq, total_reg):
    reg = ""
    print("Escolha o que deseja fazer:")
    print("\n\t(1) Inserir")
    print("\t(2) buscar")
    print("\t(3) sair")
    opcao = int(input("\nQual deseja? "))
    while opcao != 3:
        if opcao == 1:
            for i in range(5):
                temp = input(f"O {i+1}º Campo")
                reg = reg+temp+"|"
                temp = ""
            reg = reg.encode()
            reg.ljust(64,b'\0')

            offset = total_reg * 64 + 4
            arq.seek(offset)
            arq.write(reg)
            total_reg += 1
            reg = reg.decode()
            reg = ""
        elif opcao == 2:
            rrn = int(input(f"Digite o RRN (menor ou igual a {total_reg}):"))
            offset = rrn * 64 + 4
            arq.seek(offset)
            regL = arq.read(64)
            regL = regL.decode()
            regL = regL.split(sep="|")
            for campo in regL:
                print(campo)
            print("Deseja alterar?\n")
            alterar = input("S/N: ")
            if alterar == "S":
                for i in range(6):
                    temp = input(f"O {i+1}º Campo")
                    regg = regg+temp+"|"
                    temp = ""
                regg = regg.encode()
                regg.ljust(64,b'\0')
                arq.seek(offset)
                arq.write(regg)
                regg = regg.decode()
                regg = ""
    arq.seek(0)
    total_reg = total_reg.to_bytes(4)
    arq.write(total_reg)
    arq.close()

if __name__ == "__main__":
    main()    
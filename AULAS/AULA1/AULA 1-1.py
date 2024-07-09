def escreve_campos():
    name = input("escreva o nome do arquivo?")
    saida = open(name,"w")
    sobrenome = input("Escreva o sobrenome: ")
    while sobrenome != '':
        nome = input("Nome:")
        endereco = input("Endereco:")
        cidade = input("Cidade:")
        estado = input("Estado:")
        cep = input("CEP:")
        saida.write(sobrenome+"|")
        saida.write(nome+"|")
        saida.write(endereco+"|")
        saida.write(cidade+"|")
        saida.write(estado+"|")
        saida.write(cep+"|")

        sobrenome = input("Se voce quer sair ENTER se nao escreva o sobrenome: ")

    saida.close()

escreve_campos()


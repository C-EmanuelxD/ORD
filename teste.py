def leitura():
    arq = open("dados.dat","rb+")
    """cab = -1
    cab = cab.to_bytes(length=4,byteorder='little',signed=True)
    arq.write(cab)
    arq.close()"""
    cab = arq.read(4)
    cab = int.from_bytes(cab,byteorder='little',signed=True)
    print(cab)
    
leitura()
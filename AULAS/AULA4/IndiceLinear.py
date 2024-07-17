from dataclasses import dataclass

SIZEOF_TOTALREG = 4
SIZEOF_TAMREG = 2

@dataclass
class ELEMINDICE:
    ID: int
    OFFSET: int

def leia_reg(arq) -> str:
    try:
        tam = int.from_bytes(arq.read(2))
        if tam > 0:
            s = arq.read(tam)
            return s.decode(),tam
        return ''
    except OSError as e:
        print(f'Erro leia_reg: {e}')


def CriaIndice():
    arq = open("trabalhos.dat",'rb')

    #construção do indice

    TOTALREG = arq.read(SIZEOF_TOTALREG)
    TOTALREG = int.from_bytes(TOTALREG)
    INDICE = []
    OFFSET = 4
    for i in range(TOTALREG):
        reg, TAMREG = leia_reg(arq)
        ID = int(reg.split(sep="|")[0])
        # INDICE[i] = ELEMINDICE.ID
        # INDICE[i] = ELEMINDICE.OFFSET
        INDICE.append(ELEMINDICE(ID, OFFSET))
        OFFSET = OFFSET + TAMREG + SIZEOF_TAMREG
    INDICE.sort(key=lambda x: x.ID)
    arq.close()
    return INDICE

def Busca():
    INDICE = CriaIndice()
    arq = open("trabalhos.dat",'rb')
    ID_BUSCADO = int(input("Qual o id a ser buscado"))
    ID_BUSCADO = buscaBinaria(ID_BUSCADO,INDICE)
    if ID_BUSCADO != -1:
        arq.seek(INDICE[ID_BUSCADO].OFFSET)
        REG, tam = leia_reg(arq)
        print(REG)
    else:
        print("ERRO")
    arq.close()





def buscaBinaria(x: int, v: list) -> int:
    i = 0
    f = len(v)-1
    while i <= f:
        m = (i + f)//2
        if v[m].ID == x: return m
        if v[m].ID < x: i = m + 1
        else: f = m - 1
    return -1



if __name__ == "__main__":
    Busca()




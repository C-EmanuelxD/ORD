from tkinter import ttk
from tkinter import *
#version : 1.0.0#   
    
def resetUI():
    global root
    root.destroy()
    root = Tk()
    frm = ttk.Frame(root,width=800,height=400,padding=400)
    frm.grid()
    
def veSave():
    resetUI()
    global save
    listaSave = []
    palavra = ""
    info = save.read(1)
    while info != "":
        if info == "|":
            listaSave.append(palavra)
            palavra = ""
            info = save.read(1)
        palavra = palavra+info
        info = save.read(1)
    ttk.Label(root, text="Suas informações: ",font=Titulo).place(x=10,y=10)
    ttk.Label(root,text=f"Seu personagem é do tipo: {listaSave[0]}").place(x=10,y=50)
    ttk.Label(root,text=f"Sua cor de cabelo é: {listaSave[1]}").place(x=10,y=70)
    
def SalvarEscolha():
    save = open("saveArq1","w+")
    for i in listaEscolhas:
        save.write(i+"|")
    resetUI()
    ttk.Label(root, text="Criação de personagem feita com sucesso! ",font=Titulo).place(x=10,y=10)
    ttk.Button(root, text="Ver Personagem",command=lambda: veSave()).place(x=10,y=50)
    ttk.Button(root, text="SAIR",command=lambda: root.destroy()).place(x=10,y=80)
    

def cabelo(cor):
    global listaEscolhas
    listaEscolhas.append(cor)
    SalvarEscolha()

def NextSelect():
    resetUI()
    Title = ttk.Label(root, text="Escolha a cor do cabelo: ",font=Titulo).place(x=10,y=10)
    Gay = ttk.Button(root, text="Azul",command=lambda: cabelo("Azul")).place(x=10,y=50)
    Hetero = ttk.Button(root, text="Branco",command=lambda: cabelo("Branco")).place(x=10,y=80)
    Lesb = ttk.Button(root, text="Loiro",command=lambda: cabelo("Loiro")).place(x=10,y=110)
    Hetera = ttk.Button(root, text="Verde",command=lambda: cabelo("Verde")).place(x=10,y=140)



def sexoSelect(sexo):
    global listaEscolhas
    listaEscolhas.append(sexo)
    NextSelect()
    

def testaSave():
    try:
        global save
        save = open("saveArq1","r")
        ttk.Label(root, text="Você parece ter um personagem criado, deseja ver as informações?").place(x=10,y=10)
        ttk.Button(root, text="Sim", command=lambda: veSave()).place(x=10,y=50)
        ttk.Button(root, text="Não", command=lambda: criaPersonagem()).place(x=10,y=80)
    except:
        criaPersonagem()


def criaPersonagem():
    resetUI()
    global save
    save = open("saveArq1","w+")
    Title = ttk.Label(root, text="Escolha seu personagem: ",font=Titulo).place(x=10,y=10)
    Gay = ttk.Button(root, text="Homem Homossexual",command=lambda: sexoSelect("HHo")).place(x=10,y=50)
    Hetero = ttk.Button(root, text="Homem Heterossexual",command=lambda: sexoSelect("HHe")).place(x=10,y=80)
    Lesb = ttk.Button(root, text="Mulher Homossexual",command=lambda: sexoSelect("MHo")).place(x=10,y=110)
    Hetera = ttk.Button(root, text="Mulher Heterossexual",command=lambda: sexoSelect("MHe")).place(x=10,y=140)


root = Tk()
frm = ttk.Frame(root,width=800,height=400,padding=400)
frm.grid()

Titulo = ("Helvetica",18)
Texto = ("Helvetica",12)

listaEscolhas = []





if __name__ == "__main__":
    testaSave()
    
root.mainloop()
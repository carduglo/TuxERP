# -*- coding: iso-8859-1 -*-
import sqlite3
import ttk
from Tkinter import *

#Criar conexão e cursor
con = sqlite3.connect('tuxdb.db')
cur = con.cursor()
#Criar tabela clientes
cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cl VARCHAR,
            endereco VARCHAR,
            cidade VARCHAR,
            cep VARCHAR,
            cpf VARCHAR,
            fone VARCHAR,
            mail VARCHAR,
            comp VARCHAR)""")

class main:
    def __init__(self,master):
        self.frame1 = Frame(master)
        self.frame1.configure(relief=GROOVE)
        self.frame1.configure(borderwidth="2")
        self.frame1.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=0.51)
        Label(self.frame1,text='CADASTRO',font=('Ariel','30')).place(relx=0.30,rely=0.01)
        Label(self.frame1,text='Cliente',font=('Ariel','15')).place(relx=0.02,rely=0.12)
        self.cliente=Entry(self.frame1,font=('Ariel','15'))
        self.cliente.place(relx=0.02,rely=0.16)
        Label(self.frame1,text='Endereco',font=('Ariel','15')).place(relx=0.02,rely=0.21)
        self.endereco = Entry(self.frame1,font=('Ariel','15'))
        self.endereco.place(relx=0.02,rely=0.25,relwidth=0.94)
        Label(self.frame1,text='Cidade',font=('Ariel','15')).place(relx=0.02,rely=0.30)
        self.cidade = Entry(self.frame1,font=('Ariel','15'))
        self.cidade.place(relx=0.02,rely=0.34)
        Label(self.frame1,text='CEP',font=('Ariel','15')).place(relx=0.02,rely=0.39)
        self.cep = Entry(self.frame1,font=('Ariel','15'))
        self.cep.place(relx=0.02,rely=0.43)
        Label(self.frame1,text='CPF/CNPJ',font=('Ariel','15')).place(relx=0.02,rely=0.48)
        self.cpf = Entry(self.frame1,font=('Ariel','15'))
        self.cpf.place(relx=0.02,rely=0.52)
        Label(self.frame1,text='Telefone',font=('Ariel','15')).place(relx=0.02,rely=0.57)
        self.fone = Entry(self.frame1,font=('Ariel','15'))
        self.fone.place(relx=0.02,rely=0.61)
        Label(self.frame1,text='E-mail',font=('Ariel','15')).place(relx=0.02,rely=0.66)
        self.mail = Entry(self.frame1,font=('Ariel','15'))
        self.mail.place(relx=0.02,rely=0.71)
        Label(self.frame1,text='Complemento',font=('Ariel','15')).place(relx=0.02,rely=0.76)
        self.comp = Text(self.frame1,font=('Ariel','15'))
        self.comp.place(relx=0.02,rely=0.81,relwidth=0.94,relheight=0.19)
        self.botaocadastra = Button(self.frame1,text='Cadastrar',font=('Ariel','20'),
                                    fg='green',command=self.cadastraclientes)
        self.botaocadastra.place(relx=0.62,rely=0.33,relwidth=0.31)
        self.botaocancela = Button(self.frame1,text='Cancelar',font=('Ariel','20'),
                                   fg='red',command=self.limpaclientes)
        self.botaocancela.place(relx=0.62,rely=0.44,relwidth=0.31)
        
        self.frame2 = Frame(master)
        self.frame2.configure(relief=GROOVE)
        self.frame2.configure(borderwidth="2")
        self.frame2.place(relx=0.53,rely=0.0,relheight=0.31,relwidth=0.47)
        Label(self.frame2,text='CONSULTA',font=('Ariel','30')).place(relx=0.29,rely=0.05)
        self.consulta= ttk.Combobox(self.frame2,font=("Ariel","15"))
        self.consulta.place(relx=0.32,rely=0.47)
        cur.execute("SELECT cl FROM clientes ORDER BY cl")
        self.col = cur.fetchall()
        self.col = [cli[0] for cli in self.col]
        self.consulta["values"] = self.col
        #self.consulta.set("Escolha")
        self.consulta.bind("<<ComboboxSelected>>",self.mostraclientes)

        self.frame3 = Frame(master)
        self.frame3.configure(relief=GROOVE)
        self.frame3.configure(borderwidth="2")
        self.frame3.place(relx=0.53,rely=0.31,relheight=0.69,relwidth=0.47)
        self.mostra1 = Text(self.frame3,bg='grey',font=('Courier','20'))
        self.mostra1.place(relx=0.02,rely=0.02,relheight=0.97,relwidth=0.96)
        

#-----------------------------------------FUNÇÕES-----------------------------------------------------------#
    def cadastraclientes(self):
        cliente=self.cliente.get()
        endereco=self.endereco.get()
        cidade=self.cidade.get()
        cep=self.cep.get()
        cpf=self.cpf.get()
        fone=self.fone.get()
        mail=self.mail.get()
        comp=self.comp.get(0.0,END)
        cur.execute("INSERT INTO clientes VALUES(?,?,?,?,?,?,?,?,?)",
                    (None,cliente,endereco,cidade,cep,cpf,fone,mail,comp))
        con.commit()
        self.limpaclientes()
        cur.execute("SELECT cl FROM clientes ORDER BY cl")
        self.col = cur.fetchall()
        self.col = [cli[0] for cli in self.col]
        self.consulta["values"] = self.col

    def limpaclientes(self):
        self.cliente.delete(0,END)
        self.endereco.delete(0,END)
        self.cidade.delete(0,END)
        self.cep.delete(0,END)
        self.cpf.delete(0,END)
        self.fone.delete(0,END)
        self.mail.delete(0,END)
        self.comp.delete(0.0,END)

    def mostraclientes(self,event):
        self.mostra1.delete(0.0,END)
        consulta = cur.execute("SELECT * FROM clientes WHERE cl = '%s'" %self.consulta.get())
        for i in consulta:
            self.mostra1.insert(END,'''Cliente:{}
End:{}
Cidade:{}
CEP:{}
CPF:{}
Fone:{}
E-mail:{}
Complemento:{}'''.format(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))         
            
        
root = Tk()
root.title("TuxClientes")
root.geometry("1024x768")
main(root)
root.mainloop()

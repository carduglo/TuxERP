# -*- coding: iso-8859-1 -*-
import sqlite3
import ttk
from Tkinter import *
import win32ui
import win32print
import win32con

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
#Criar tabela produtos
cur.execute("""CREATE TABLE IF NOT EXISTS produtos(
            ref int primary key NOT NULL,
            desc varchar(100) NOT NULL,
            precoV dec NOT NULL,
            precoA dec NOT NULL)""")
con.commit()
#Cria tabela do pedido
cur.execute("""CREATE TABLE IF NOT EXISTS pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ref INTEGER NOT NULL,
            quant INTEGER NOT NULL,
            desc VARCHAR(100) NOT NULL,
            preco DEC NOT NULL,
            total DEC NOT NULL)""")

cur.execute("DELETE FROM pedido WHERE 1")

#Limpa a tabela


class main:
    def __init__(self,master):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Abas~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.abas = ttk.Notebook(master)
        self.abas.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=1.0)
        self.abas.configure(width=800)
        self.abas.configure(takefocus="")
        self.abas_pg0 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg0, padding=3)
        self.abas.tab(0, text="Cadastro",underline="-1",)
        self.abas_pg1 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg1, padding=3)
        self.abas.tab(1, text="Venda",underline="-1",)
        self.abas_pg2 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg2, padding=3)
        self.abas.tab(2, text="Clientes",underline="-1",)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aba Cadastro~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Referencia
        Label(self.abas_pg0, text="Referencia",font=('Ariel','15')).place(relx=0.06,rely=0.01)
        self.ref_c = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.ref_c.place(relx=0.02,rely=0.07,width=170)
        #Descrição
        Label(self.abas_pg0, text="Descricao",font=('Ariel','15')).place(relx=0.40,rely=0.19)
        self.desc_c = Entry(self.abas_pg0, width=6, font=('Ariel','30'))
        self.desc_c.place(relx=0.25,rely=0.25,width=400)
        #Preço varejo
        Label(self.abas_pg0, text="Preco Varejo",font=('Ariel','15')).place(relx=0.425,rely=0.01)
        self.precov = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.precov.place(relx=0.4,rely=0.07,width=170)
        #Preço Atacado
        Label(self.abas_pg0, text="Preco Atacado",font=('Ariel','15')).place(relx=0.755,rely=0.01)
        self.precoa = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.precoa.place(relx=0.75,rely=0.07,width=170)
        #Botão Cadastra
        self.botao_cadastra = Button(self.abas_pg0, text="Cadastrar", font=('Ariel','15'),
                                     fg='green',command=self.cadastra)
        self.botao_cadastra.place(relx=0.38,rely=0.5,height=100,width=200)
        #Botao Cancela cadastro
        self.botao_cancela = Button(self.abas_pg0, text="Novo/Cancelar",
                             font=('Ariel','15'),fg='red',command=self.calcela_cadastro)
        self.botao_cancela.place(relx=0.38,rely=0.80,height=100,width=200)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aba Venda~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Entrada referencia
        Label(self.abas_pg1, text="Referencia",font=('Ariel','15')).place(relx=-0.0,rely=0.02)
        self.ref = Entry(self.abas_pg1, width=6, font=('Ariel','20'))
        self.ref.place(relx=0.0,rely=0.07)
        #Entrada quantidade
        Label(self.abas_pg1, text="Quantidade",font=('Ariel','15')).place(relx=-0.0,rely=0.2)
        self.quant = Entry(self.abas_pg1, width=6, font=('Ariel','20'))
        self.quant.place(relx=0.00,rely=0.25)
        #Total             
        Label(self.abas_pg1,text="Total do Pedido",font=('Courier','16','bold')).place(relx=0.75,rely=0.30)
        self.totalp=Entry(self.abas_pg1, width=15,font=('Courier','30'), fg='red')
        self.totalp.place(relx=0.7,rely=0.37)
        #Botão OK
        self.botao1 = Button(self.abas_pg1, text="Faturar", font=('Ariel','20'),
                             fg='green',command=self.pedido)
        self.botao1.place(relx=0.35,rely=0.08,height=46,width=167)
        #Botão Imprimir
        self.botao2 = Button(self.abas_pg1, text="Imprimir", font=('Ariel','15'),
                             fg='green',command=self.imprimir)
        self.botao2.place(relx=0.35,rely=0.25,height=46,width=167)
        #Botão Cancelar
        self.botao3 = Button(self.abas_pg1, text="Novo/Cancelar", font=('Ariel','15'),
                             fg='red',command=self.cancela)
        self.botao3.place(relx=0.33,rely=0.40,height=40,width=200)
        #Radio buttons
        self.escolha = BooleanVar()
        self.r1 = Radiobutton(self.abas_pg1, text = 'Varejo',font=('Ariel','20'),variable=self.escolha,value=True)
        self.r1.place(relx=0.75,rely=0.03)
        self.r2 = Radiobutton(self.abas_pg1, text='Atacado',font=('Ariel','20'),variable=self.escolha,value=False)
        self.r2.place(relx=0.75,rely=0.12)
        #Desconto
        Label(self.abas_pg1, text="Desconto",font=('Ariel','15')).place(relx=0.0,rely=0.37)                                                               
        self.desconto = Entry(self.abas_pg1, width=6, font=('Ariel','20'))
        self.desconto.place(relx=0.0,rely=0.42)
        #ListBox
        scrollbar = Scrollbar(self.abas_pg1)
        scrollbar.place(x=1000,y=362,height=325)
        
        self.listbox = Listbox(self.abas_pg1,selectmode='single',font=('Courier','15'),fg="blue")
        self.listbox.place(relx=0.0,rely=0.50,width=1000,height=350)
        self.listbox.config(yscrollcommand=scrollbar.set)        
        scrollbar.config(command=self.listbox.yview)

        self.frame1 = Frame(self.abas_pg2)
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
        
        self.frame2 = Frame(self.abas_pg2)
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

        self.frame3 = Frame(self.abas_pg2)
        self.frame3.configure(relief=GROOVE)
        self.frame3.configure(borderwidth="2")
        self.frame3.place(relx=0.53,rely=0.31,relheight=0.69,relwidth=0.47)
        self.mostra1 = Text(self.frame3,bg='grey',font=('Courier','20'))
        self.mostra1.place(relx=0.02,rely=0.02,relheight=0.97,relwidth=0.96)
        
#===================================================Funções============================================================                
    #Função Cadastra produto
    def cadastra(self):
        ref = self.ref_c.get()
        desc = self.desc_c.get()
        precov = self.precov.get()
        precoa = self.precoa.get() 
        cur.execute("INSERT INTO produtos VALUES(?,?,?,?)",(ref,desc,precov,precoa))
        con.commit()

    #Função Cancela cadastro
    def calcela_cadastro(self):
        self.ref_c.delete(0,END)
        self.desc_c.delete(0,END)
        self.precov.delete(0,END)
        self.precoa.delete(0,END)

    #Função pedido
    def pedido(self):
        self.listbox.delete(0,END) #Limpa a listbox
        ref = self.ref.get() #Pega o valor da referencia digitado
        quant = float(self.quant.get()) #Pega a quantidade informada
        cur.execute("SELECT * FROM produtos WHERE ref = %s" %ref) #Consulta pela referencia
        item = cur.fetchone()
        desc= item[1]
        preco = float(item[2])
        precoa = float(item[3])
        v = self.escolha.get()
        if v == 1:
            precof = preco
        else:
            precof = precoa
        desconto = float(self.desconto.get())
        total = quant*precof #Calcula preço total
        desconto = total*desconto/100.00
        total = total-desconto
        cur.execute("INSERT INTO pedido VALUES(?,?,?,?,?,?)",
                    (None,ref,quant,desc,precof,total))
        con.commit() #Insere dados na tabela pedido
        tb=cur.execute("SELECT * FROM pedido") #Pesquisa tudo na tabela pedido
        #Insere os dados na lista
        self.listbox.insert(END,"Ref         Qtd                    Descricao                    Unit        Total")
        tb = list(tb)
        for i in tb: 
            self.listbox.insert(END,"{:.<9}{:.^10}{:.^43}{:.^8.2f}{:.>12.2f}" .format(i[1],i[2],i[3],i[4],i[5]))#Insere dados na listbox
            self.listbox.select_clear(self.listbox.size() - 2)
            self.listbox.select_set(END)
            self.listbox.yview(END)
            cur.execute("SELECT SUM(total)FROM pedido")#Soma total
            totalp = cur.fetchone()
            self.totalp.delete(0,END) #Limpa Total
            self.totalp.insert(END,"R$:%.2f"%totalp)#Insere total
                  
    #Função cancela pedido
    def cancela(self):
        cur.execute("DELETE FROM pedido WHERE 1")#Apaga pedido
        self.listbox.delete(0,END) #Limpa a listbox
        self.ref.delete(0,END)#Apaga campo referencia
        self.quant.delete(0,END)#Apaga campo quantidade
        self.totalp.delete(0,END)#Apaga campo Total do Pedido
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
            
    #Função Imprimir
    def imprimir(self):
        cabecalho = '''------------------------------------LINE FITNESS-------------------------------------
---------------------------E-mail: linefitness2014@gmail.com-------------------------
--------------------------------Fone: (47) 9682 6062---------------------------------'''
        hDC = win32ui.CreateDC()
        print win32print.GetDefaultPrinter() # test
        hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
        hDC.StartDoc("Test doc")
        hDC.StartPage()
        hDC.SetMapMode(win32con.MM_TWIPS)
        font = win32ui.CreateFont({
        'name': 'Courier',
        'height': 200,
        'weight': win32con.FW_NORMAL,
        'pitch and family':win32con.FIXED_PITCH})
        hDC.SelectObject(font)
        # draws text within a box (assume about 1400 dots per inch for typical HP printer)
        ulc_x = 1000 # give a left margin
        ulc_y = -1700 # give a top margin
        lrc_x = 11500 # width of text area-margin, close to right edge of page
        lrc_y = -15000 # height of text area-margin, close to bottom of the page
        tb=self.listbox.get(0,END)
        hDC.DrawText(cabecalho,(ulc_x, -950, lrc_x, lrc_y), win32con.DT_TOP)
                
        for i in tb: 
            i=("{}" .format(i))
            hDC.DrawText(i, (ulc_x, ulc_y, lrc_x, lrc_y), win32con.DT_LEFT)
            ulc_y = ulc_y-500 
        totalprint = "Total do Pedido:" + 60*'-'+ str(self.totalp.get())
        hDC.DrawText(totalprint,(ulc_x, ulc_y, lrc_x, lrc_y), win32con.DT_LEFT)  
        hDC.EndPage()
        hDC.EndDoc()
        
root = Tk()
root.title("TuxERP 1.0")
root.geometry("1024x768")
main(root)
root.mainloop()


        

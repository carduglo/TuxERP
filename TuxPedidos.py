# -*- coding: iso-8859-1 -*-
import sqlite3
import ttk
from Tkinter import *
import subprocess
import tkMessageBox

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
cur.execute('''CREATE TABLE IF NOT EXISTS produtos(
            ref int primary key NOT NULL,
            desc varchar(100) NOT NULL,
            precoV dec NOT NULL,
            precoA dec NOT NULL,
            pp INTEGER DEFAULT (0),
            p INTEGER DEFAULT (0),
            m INTEGER DEFAULT (0),
            g INTEGER DEFAULT (0),
            gg INTEGER DEFAULT (0))''')
con.commit()
#Cria tabela do pedido
cur.execute("""CREATE TABLE IF NOT EXISTS pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ref INTEGER NOT NULL,
            quant INTEGER NOT NULL,
            desc VARCHAR(100) NOT NULL,
            preco DEC NOT NULL,
            total DEC NOT NULL,
            pp INTEGER DEFAULT (0),
            p INTEGER DEFAULT (0),
            m INTEGER DEFAULT (0),
            g INTEGER DEFAULT (0),
            gg INTEGER DEFAULT (0))""")
#Limpa a tabela pedido
cur.execute("DELETE FROM pedido WHERE 1")

class main:
    def __init__(self,master):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Abas~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.abas = ttk.Notebook(master)
        self.abas.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=1.0)
        self.abas.configure(width=1024)
        self.abas.configure(takefocus="")
        self.abas_pg0 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg0, padding=3)
        self.abas.tab(0, text="Cadastro",underline="-1")
        self.abas_pg1 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg1, padding=3)
        self.abas.tab(1, text="Venda",underline="-1",)
        self.abas_pg2 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg2, padding=3)
        self.abas.tab(2, text="Clientes",underline="-1",)
        self.abas_pg3 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg3, padding=3)
        self.abas.tab(3, text="Estoque",underline="-1",)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aba Cadastro~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Referencia
        Label(self.abas_pg0, text=u"Referência",font=('Ariel','15')).place(relx=0.00,rely=0.01)
        self.ref_c = Entry(self.abas_pg0, width=20, font=('Ariel','20'))
        self.ref_c.place(relx=0.00,rely=0.07)
        #Preço varejo
        Label(self.abas_pg0, text=u"Preço Varejo",font=('Ariel','15')).place(relx=0.408,rely=0.01)
        self.precov = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.precov.place(relx=0.4,rely=0.07,width=170)
        #Preço Atacado
        Label(self.abas_pg0, text=u"Preço Atacado",font=('Ariel','15')).place(relx=0.755,rely=0.01)
        self.precoa = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.precoa.place(relx=0.75,rely=0.07,width=170)
        #Descrição
        Label(self.abas_pg0, text=u"Descrição",font=('Ariel','15')).place(relx=0.410,rely=0.19)
        self.desc_c = Entry(self.abas_pg0,font=('Ariel','30'))
        self.desc_c.place(relx=0.25,rely=0.25,relwidth=0.45)
        #Botão Cadastra
        self.botao_cadastra = Button(self.abas_pg0, text="Cadastrar", font=('Ariel','15'),
                                     fg='green',command=self.cadastra)
        self.botao_cadastra.place(relx=0.38,rely=0.5,height=100,width=200)
        #Botao Cancela cadastro
        self.botao_cancela = Button(self.abas_pg0, text="Novo/Cancelar",
                             font=('Ariel','15'),fg='red',command=self.cancela_cadastro)
        self.botao_cancela.place(relx=0.38,rely=0.80,height=100,width=200)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aba Venda~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Entrada referencia
        Label(self.abas_pg1, text=u"Referência",font=('Ariel','15')).place(relx=-0.0,rely=0.02)
        self.ref = Entry(self.abas_pg1, width=6, font=('Ariel','20'))
        self.ref.place(relx=0.0,rely=0.07)
        #Entrada quantidade
        #Label(self.abas_pg1, text="Quantidade",font=('Ariel','15')).place(relx=-0.0,rely=0.2)
        #self.quant = Entry(self.abas_pg1, width=6, font=('Ariel','20'))
        #self.quant.place(relx=0.00,rely=0.25)

#-------------------------------------------Separador----------------------------------------------------------------------
        self.separador0 = Frame(self.abas_pg1,bd=3,relief=SUNKEN,width=2)
        self.separador0.place(relx=0.10,rely=0.0,relheight=0.55)

        Label(self.abas_pg1, text=u"PP/Único",font=('Ariel','15'),fg='blue').place(relx=0.11,rely=0.00)
        self.pp_quant=Entry(self.abas_pg1, width=15, font=('Ariel','15'))
        self.pp_quant.place(relx=0.11,rely=0.04)

        Label(self.abas_pg1, text="P",font=('Ariel','15'),fg='blue').place(relx=0.11,rely=0.10)
        self.p_quant=Entry(self.abas_pg1, width=15, font=('Ariel','15'))
        self.p_quant.place(relx=0.11,rely=0.14)

        Label(self.abas_pg1, text="M",font=('Ariel','15'),fg='blue').place(relx=0.11,rely=0.20)
        self.m_quant=Entry(self.abas_pg1, width=15, font=('Ariel','15'))
        self.m_quant.place(relx=0.11,rely=0.24)

        Label(self.abas_pg1, text="G",font=('Ariel','15'),fg='blue').place(relx=0.11,rely=0.30)
        self.g_quant=Entry(self.abas_pg1, width=15, font=('Ariel','15'))
        self.g_quant.place(relx=0.11,rely=0.34)

        Label(self.abas_pg1, text="GG",font=('Ariel','15'),fg='blue').place(relx=0.11,rely=0.40)
        self.gg_quant=Entry(self.abas_pg1, width=15, font=('Ariel','15'))
        self.gg_quant.place(relx=0.11,rely=0.44)
               
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
        self.botao3.place(relx=0.34,rely=0.40,height=40,width=200)
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
        #scrollbar = Scrollbar(self.abas_pg1)
        #scrollbar.place(x=1000,y=372,relheight=0.46)
        
        self.listbox = Listbox(self.abas_pg1,selectmode='single',font=('Courier','15'),fg="blue")
        self.listbox.place(relx=0.0,rely=0.50,width=1000,height=350)
        #self.listbox.config(yscrollcommand=scrollbar.set)        
        #scrollbar.config(command=self.listbox.yview)
#-------------------------------Aba Clientes-------------------------------------------------------------------------
        self.frame1 = Frame(self.abas_pg2)
        self.frame1.configure(relief=GROOVE)
        self.frame1.configure(borderwidth="2")
        self.frame1.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=0.50)
        Label(self.frame1,text='CADASTRO',font=('Ariel','30')).place(relx=0.30,rely=0.01)
        Label(self.frame1,text='Cliente',font=('Ariel','15')).place(relx=0.02,rely=0.12)
        self.cliente=Entry(self.frame1,font=('Ariel','15'))
        self.cliente.place(relx=0.02,rely=0.16)
        Label(self.frame1,text=u'Endereço',font=('Ariel','15')).place(relx=0.02,rely=0.21)
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
        self.frame2.place(relx=0.50,rely=0.0,relheight=0.31,relwidth=0.50)
        Label(self.frame2,text='CONSULTA',font=('Ariel','30')).place(relx=0.32,rely=0.05)
        self.consulta= ttk.Combobox(self.frame2,font=("Ariel","15"))
        self.consulta.place(relx=0.29,rely=0.47)
        cur.execute("SELECT cl FROM clientes ORDER BY cl")
        self.col = cur.fetchall()
        self.col = [cli[0] for cli in self.col]
        self.consulta["values"] = self.col
        #self.consulta.set("Escolha")
        self.consulta.bind("<<ComboboxSelected>>",self.mostraclientes)

        self.frame3 = Frame(self.abas_pg2)
        self.frame3.configure(relief=GROOVE)
        self.frame3.configure(borderwidth="2")
        self.frame3.place(relx=0.50,rely=0.31,relheight=0.69,relwidth=0.50)
        self.mostra1 = Text(self.frame3,bg='light grey',font=('Ariel','20'))
        self.mostra1.place(relx=0.0,rely=0.00,relheight=1.0,relwidth=1.0)
#----------------------------------------------------ABA ESTOQUE-------------------------------------------------------
        self.frame4 = Frame(self.abas_pg3)
        self.frame4.place(relx=0.0,rely=0.00,relheight=1.0,relwidth=1.0)
        
        Label(self.frame4, text=u"PP/Único",font=('Ariel','15'),fg='blue').place(relx=0.0,rely=0.00)
        self.pp_estoque=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.pp_estoque.place(relx=0.0,rely=0.04)

        Label(self.frame4, text="P",font=('Ariel','15'),fg='blue').place(relx=0.0,rely=0.10)
        self.p_estoque=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.p_estoque.place(relx=0.0,rely=0.14)

        Label(self.frame4, text="M",font=('Ariel','15'),fg='blue').place(relx=0.0,rely=0.20)
        self.m_estoque=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.m_estoque.place(relx=0.0,rely=0.24)

        Label(self.frame4, text="G",font=('Ariel','15'),fg='blue').place(relx=0.0,rely=0.30)
        self.g_estoque=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.g_estoque.place(relx=0.0,rely=0.34)

        Label(self.frame4, text="GG",font=('Ariel','15'),fg='blue').place(relx=0.0,rely=0.40)
        self.gg_estoque=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.gg_estoque.place(relx=0.0,rely=0.44)

        Label(self.frame4, text=u"Referência",font=('Ariel','20'),fg='blue').place(relx=0.7,rely=0.00)
        self.ref_estoque=Entry(self.frame4, width=15, font=('Ariel','20'))
        self.ref_estoque.place(relx=0.7,rely=0.08)
                
        #Cabeçalho da lista
        self.dataCols = (u'Referência',u'Descrição',u'PP/Único','P','M','G','GG')
        self.arvore = ttk.Treeview(self.frame4,columns=self.dataCols, show='headings')
        self.arvore.place(relx=0.0,rely=0.55,relheight=0.45,relwidth=0.990)
        for c in self.dataCols:
            self.arvore.heading(c, text = c)
            self.arvore.column(c,minwidth=1,width=10)
        self.rolagemy = Scrollbar(self.frame4)
        self.rolagemy.place(relx=0.990,rely=0.550,relheight=0.45)
        self.arvore.config(yscrollcommand=self.rolagemy.set)
        self.rolagemy.config(command=self.arvore.yview)

        self.botao_alt_produto = Button(self.frame4,text='Alterar',font=('Arial','25'),command=self.alterar_produto)
        self.botao_alt_produto.place(relx=0.17,rely=0.012)
        self.botao_alt_produto = Button(self.frame4,text='Limpar',font=('Arial','25'),command=self.limpa_estoque)
        self.botao_alt_produto.place(relx=0.17,rely=0.12)
#-------------------------------------------Separador----------------------------------------------------------------------
        self.separador = Frame(self.frame4,bd=3,relief=SUNKEN,width=2)
        self.separador.place(relx=0.27,rely=0.0,relheight=0.55)

        Label(self.frame4, text=u"PP/Único",font=('Ariel','15'),fg='blue').place(relx=0.28,rely=0.00)
        self.pp_soma=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.pp_soma.place(relx=0.28,rely=0.04)

        Label(self.frame4, text="P",font=('Ariel','15'),fg='blue').place(relx=0.28,rely=0.10)
        self.p_soma=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.p_soma.place(relx=0.28,rely=0.14)

        Label(self.frame4, text="M",font=('Ariel','15'),fg='blue').place(relx=0.28,rely=0.20)
        self.m_soma=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.m_soma.place(relx=0.28,rely=0.24)

        Label(self.frame4, text="G",font=('Ariel','15'),fg='blue').place(relx=0.28,rely=0.30)
        self.g_soma=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.g_soma.place(relx=0.28,rely=0.34)

        Label(self.frame4, text="GG",font=('Ariel','15'),fg='blue').place(relx=0.28,rely=0.40)
        self.gg_soma=Entry(self.frame4, width=15, font=('Ariel','15'))
        self.gg_soma.place(relx=0.28,rely=0.44)

        self.botao_add = Button(self.frame4,text='Adicionar',font=('Arial','25'),
                                command=self.somar_estoque)
        self.botao_add.place(relx=0.44,rely=0.012)
        
#---------------------------------------Separador--------------------------------------------------------------------------

        self.separador2 = Frame(self.frame4,bd=3,relief=SUNKEN,width=2)
        self.separador2.place(relx=0.573,rely=0.0,relheight=0.55)
        
        self.botao_pesq_produto = Button(self.frame4,text='Pesquisar',font=('Arial','25'),
                                         command=self.pesquisa_referencia)
        self.botao_pesq_produto.place(relx=0.7,rely=0.20)

        self.botao_del_produto = Button(self.frame4,text='Apagar',font=('Arial','25'),fg='red',
                                        command=self.deleta_produto)
        self.botao_del_produto.place(relx=0.88,rely=0.45)
        
        self.lista_estoque()
        self.zera_soma()
        self.zera_pedido()
        self.zera_desconto()
        
#===================================================Funções============================================================                
    #Função Cadastra produto
    def cadastra(self):
        ref = self.ref_c.get()
        desc = self.desc_c.get()
        precov = self.precov.get()
        precoa = self.precoa.get()
        qt = 0
        try:
            cur.execute("INSERT INTO produtos VALUES(?,?,?,?,?,?,?,?,?)",(ref,desc,precov,precoa,qt,qt,qt,qt,qt))
        except:
            tkMessageBox.showinfo('Aviso!',u'Referência já existente, ou valor inválido')
        con.commit()
        self.lista_estoque()
        self.cancela_cadastro()

    #Função Cancela cadastro
    def cancela_cadastro(self):
        self.ref_c.delete(0,END)
        self.desc_c.delete(0,END)
        self.precov.delete(0,END)
        self.precoa.delete(0,END)

    #Função pedido
    def pedido(self):
        self.listbox.delete(0,END) #Limpa a listbox
        ref = self.ref.get() #Pega o valor da referencia digitado
        pp = float(self.pp_quant.get())
        p = float(self.p_quant.get())
        m = float(self.m_quant.get())
        g = float(self.g_quant.get())
        gg =float(self.gg_quant.get()) 
        quant = pp+p+m+g+gg #Soma da quantidade de peças por tamanho
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
        desconto = total*desconto/100.00#Calculo do desconto em porcentagem
        total = total-desconto
        cur.execute("INSERT INTO pedido VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (None,ref,quant,desc,precof,total,pp,p,m,g,gg))
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
        self.zera_pedido()
        
                  
    #Função cancela pedido
    def cancela(self):
        cur.execute("DELETE FROM pedido WHERE 1")#Apaga pedido
        self.listbox.delete(0,END) #Limpa a listbox
        self.ref.delete(0,END)#Apaga campo referencia
        self.totalp.delete(0,END)#Apaga campo Total do Pedido
        self.zera_desconto()
        
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
            self.mostra1.insert(END,u'''Cliente: {}
End: {}
Cidade: {}
CEP: {}
CPF: {}
Fone: {}
E-mail: {}
Complemento: {}'''.format(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
            
    #Função Imprimir
    def imprimir(self):
        self.diminui_estoque()
        outfile = open('outfile.txt','w')
        cabecalho = '''------------------------------------LINE FITNESS-------------------------------------
---------------------------E-mail: linefitness2014@gmail.com-------------------------
--------------------------------Fone: (47) 9682 6062---------------------------------'''
        outfile.write(cabecalho+'\n\n\n')
        tb=self.listbox.get(0,END)        
        for i in tb: 
            i=("{}\n" .format(i))
            outfile.write(i)
        totalprint = "Total do Pedido:" + 57*'-'+ str(self.totalp.get())
        outfile.write('\n\n'+totalprint)
        outfile.close()
        subprocess.call(['notepad.exe','/p','outfile.txt'])*2 #versão notepad windows
        #subprocess.call(['swriter','outfile.txt']) #Linux writer
        
#-------------------------------------Funções de Estoque----------------------------------------------------
    def lista_estoque(self):
        #Limpar lista
        for i in self.arvore.get_children():
            self.arvore.delete(i)
        #Consulta BD e preenche a lista    
        dados=cur.execute('SELECT ref,desc,pp,p,m,g,gg FROM produtos ORDER BY ref')
        for item in dados:
            self.arvore.insert('','end',values=item)
        self.arvore.bind('<<TreeviewSelect>>',self.itemselect)

    def itemselect(self,event):
        self.ref_estoque.delete(0,END)
        self.limpa_estoque()       
        item = self.arvore.selection()
        item = self.arvore.item(item,'values')
        #Preenche os campos
        self.ref_estoque.insert(END,item[0])
        self.pp_estoque.insert(END,item[2])
        self.p_estoque.insert(END,item[3])
        self.m_estoque.insert(END,item[4])
        self.g_estoque.insert(END,item[5])
        self.gg_estoque.insert(END,item[6])

    def limpa_estoque(self):
        #Limpa os campos
        self.pp_estoque.delete(0,END)
        self.p_estoque.delete(0,END)
        self.m_estoque.delete(0,END)
        self.g_estoque.delete(0,END)
        self.gg_estoque.delete(0,END)
        
    def alterar_produto(self):
        indice = self.ref_estoque.get()
        pp_novo = self.pp_estoque.get()
        p_novo = self.p_estoque.get()
        m_novo = self.m_estoque.get()
        g_novo = self.g_estoque.get()
        gg_novo = self.gg_estoque.get()
        cur.execute('''UPDATE produtos SET pp = ?,
                    p = ?,
                    m = ?,
                    g = ?,
                    gg = ?
                    WHERE ref = ?''',
                    (pp_novo,p_novo,m_novo,g_novo,gg_novo,indice))
        con.commit()
        self.lista_estoque()

    def pesquisa_referencia(self):
        ref_pesq = self.ref_estoque.get()
        cur.execute('SELECT * FROM produtos WHERE ref = %s'%ref_pesq)
        item = cur.fetchone()
        self.limpa_estoque()
        self.pp_estoque.insert(END,item[4])
        self.p_estoque.insert(END,item[5])
        self.m_estoque.insert(END,item[6])
        self.g_estoque.insert(END,item[7])
        self.gg_estoque.insert(END,item[8])
        self.lista_estoque()
       
    def somar_estoque(self):
        indice = self.ref_estoque.get()
        cur.execute('SELECT * FROM produtos WHERE ref = %s'%indice)
        item = cur.fetchone()
        pp_soma = int(self.pp_soma.get())+int(item[4])
        p_soma = int(self.p_soma.get())+int(item[5])
        m_soma = int(self.m_soma.get())+int(item[6])
        g_soma = int(self.g_soma.get())+int(item[7])
        gg_soma = int(self.gg_soma.get())+int(item[8])
        cur.execute('''UPDATE produtos SET pp = ?,
                    p = ?,
                    m = ?,
                    g = ?,
                    gg = ?
                    WHERE ref = ?''',
                    (pp_soma,p_soma,m_soma,g_soma,gg_soma,indice))
        con.commit()
        self.lista_estoque()
        self.zera_soma()

    def diminui_estoque(self):
        cur.execute('''UPDATE produtos SET pp =
                   (SELECT produtos.pp-pedido.pp FROM pedido
                    WHERE produtos.ref = pedido.ref)
                    WHERE produtos.ref IN (SELECT pedido.ref FROM pedido)''')
        
        cur.execute('''UPDATE produtos SET p =
                   (SELECT produtos.p-pedido.p FROM pedido
                    WHERE produtos.ref = pedido.ref)
                    WHERE produtos.ref IN (SELECT pedido.ref FROM pedido)''')
        
        cur.execute('''UPDATE produtos SET m =
                   (SELECT produtos.m-pedido.m FROM pedido
                    WHERE produtos.ref = pedido.ref)
                    WHERE produtos.ref IN (SELECT pedido.ref FROM pedido)''')

        cur.execute('''UPDATE produtos SET g =
                   (SELECT produtos.g-pedido.g FROM pedido
                    WHERE produtos.ref = pedido.ref)
                    WHERE produtos.ref IN (SELECT pedido.ref FROM pedido)''')

        cur.execute('''UPDATE produtos SET gg =
                   (SELECT produtos.gg-pedido.gg FROM pedido
                    WHERE produtos.ref = pedido.ref)
                    WHERE produtos.ref IN (SELECT pedido.ref FROM pedido)''')
        con.commit()
        self.lista_estoque()

    def deleta_produto(self):
        ref_del = self.ref_estoque.get()
        cur.execute("DELETE FROM produtos WHERE ref=%s "%ref_del)
        con.commit()
        self.lista_estoque()

    def zera_soma(self):
        self.pp_soma.delete(0,END)
        self.p_soma.delete(0,END)
        self.m_soma.delete(0,END)
        self.g_soma.delete(0,END)
        self.gg_soma.delete(0,END)
        self.pp_soma.insert(0,'0')
        self.p_soma.insert(0,'0')
        self.m_soma.insert(0,'0')
        self.g_soma.insert(0,'0')
        self.gg_soma.insert(0,'0')

    def zera_pedido(self):
        self.pp_quant.delete(0,END)
        self.p_quant.delete(0,END)
        self.m_quant.delete(0,END)
        self.g_quant.delete(0,END)
        self.gg_quant.delete(0,END)
        self.pp_quant.insert(0,'0')
        self.p_quant.insert(0,'0')
        self.m_quant.insert(0,'0')
        self.g_quant.insert(0,'0')
        self.gg_quant.insert(0,'0')
    def zera_desconto(self):
        self.desconto.delete(0,END)
        self.desconto.insert(0,'0')
                          
        
root = Tk()
root.title("TuxPedidos 1.0")
root.geometry("1366x768")
img = PhotoImage(file='tuxd.png')
root.tk.call('wm','iconphoto',root._w,img)
main(root)
root.mainloop()


        

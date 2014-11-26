# -*- coding: UTF-8 -*-

# TuxERP volney 2014

import sqlite3
from autocomplete import *
import ttk
from Tkinter import *
import subprocess
import tkMessageBox
from datetime import date
import tkFont
import tabelas
import relatorios
from maskedentry import MaskedWidget

#Criação de tabelas
tabelas.cria_tabelas()

#Criar conexão e cursor com banco de dados
con = sqlite3.connect('tuxdb.db')
cur = con.cursor()

cur.execute("DELETE FROM pedido WHERE 1")#Limpa tabela pedido

class main:
    def __init__(self,master):
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Abas~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        f = tkFont.Font(family='helvetica', size=14)
        s = ttk.Style()
        s.configure('.', font=f)
        
        self.abas = ttk.Notebook(master)
        self.abas.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=1.0)
        #self.abas.configure(width=1024) Ainda não descobri pra que serve isso
        self.abas.configure(takefocus="")
        self.abas_pg0 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg0, padding=3)
        self.abas.tab(0, text="Cadastro",underline="-1")
        self.abas_pg3 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg3, padding=3)
        self.abas.tab(1, text="Estoque",underline="-1",)
        self.abas_pg2 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg2, padding=3)
        self.abas.tab(2, text="Clientes",underline="-1",)
        self.abas_pg1 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg1, padding=3)
        self.abas.tab(3, text="Venda",underline="-1",)
        self.abas_pg4 = ttk.Frame(self.abas)
        self.abas.add(self.abas_pg4, padding=3)
        self.abas.tab(4, text=u"Relatórios",underline="-1",)
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aba Cadastro~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Label(self.abas_pg0, text=u"CADASTRO DE PRODUTO",font=('Ariel','25'),fg='blue').place(relx=0.350,rely=0.0)
        #Referencia
        Label(self.abas_pg0, text=u"Referência",font=('Ariel','15')).place(relx=0.00,rely=0.11)
        self.ref_c = Entry(self.abas_pg0, width=20, font=('Ariel','20'))
        self.ref_c.place(relx=0.00,rely=0.17)
        #Preço varejo
        Label(self.abas_pg0, text=u"Preço Varejo",font=('Ariel','15')).place(relx=0.430,rely=0.11)
        self.precov = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.precov.place(relx=0.417,rely=0.17,width=170)
        #Preço Atacado
        Label(self.abas_pg0, text=u"Preço Atacado",font=('Ariel','15')).place(relx=0.755,rely=0.11)
        self.precoa = Entry(self.abas_pg0, width=6, font=('Ariel','20'))
        self.precoa.place(relx=0.75,rely=0.17,width=170)
        #Descrição
        Label(self.abas_pg0, text=u"Descrição",font=('Ariel','15')).place(relx=0.450,rely=0.29)
        self.desc_c = Entry(self.abas_pg0,font=('Ariel','30'))
        self.desc_c.place(relx=0.265,rely=0.35,relwidth=0.45)
        #Botão Cadastra
        self.botao_cadastra = Button(self.abas_pg0, text="Cadastrar", font=('Ariel','18'),
                                     fg='green',command=self.cadastra)
        self.botao_cadastra.place(relx=0.30,rely=0.45,height=100,width=200)
        #Botao Cancela cadastro
        self.botao_cancela = Button(self.abas_pg0, text="Novo/Cancelar",
                             font=('Ariel','15'),fg='red',command=self.cancela_cadastro)
        self.botao_cancela.place(relx=0.49,rely=0.45,height=100,width=200)

        self.sep_cadastro = Frame(self.abas_pg0,bd=3,relief=SUNKEN,height=2)
        self.sep_cadastro.place(relx=0.0,rely=0.60,relwidth=1.0)
        #Cadastra Vendedor
        Label(self.abas_pg0, text=u"CADASTRO DE VENDEDORES",font=('Ariel','25'),fg='blue').place(relx=0.340,rely=0.61)
        #Entrada cadastra vendedor
        Label(self.abas_pg0, text=u"Vendedor",font=('Ariel','15')).place(relx=0.00,rely=0.70)
        self.vend_c = Entry(self.abas_pg0, width=20, font=('Ariel','20'))
        self.vend_c.place(relx=0.00,rely=0.75)
        #Entrada cadastra senha vendedor
        Label(self.abas_pg0, text=u"Senha",font=('Ariel','15')).place(relx=0.00,rely=0.85)
        self.senha_c = Entry(self.abas_pg0, width=20, font=('Ariel','20'),show='*')
        self.senha_c.place(relx=0.00,rely=0.90)
        #Botão cadastra vendedor
        Button(self.abas_pg0, text="Cadastrar",
               font=('Ariel','15'),fg='green',command=self.cadastra_vendedor).place(relx=0.40,rely=0.85,height=100,width=200)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Aba Venda~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Entrada vendedor
        Label(self.abas_pg1, text=u"Vendedor",font=('Ariel','15')).place(relx=-0.0,rely=0.02)
        self.lista_vendedores()
        #Entrada cliente
        Label(self.abas_pg1,text='Cliente',font=('Ariel','15')).place(relx=0.0,rely=0.135)
        self.venda_cliente = AutocompleteCombobox(self.abas_pg1, font=("Ariel","18"),width=7)
        self.venda_cliente.place(relx=0.0, rely=0.18)
        #Entrada referencia
        Label(self.abas_pg1, text=u"Referência",font=('Ariel','15')).place(relx=-0.0,rely=0.25)
        self.ref = Entry(self.abas_pg1, width=6, font=('Ariel','20'))
        self.ref.place(relx=0.0,rely=0.30)
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
        #Botão Cancelar
        self.botao3 = Button(self.abas_pg1, text="Novo/Cancelar", font=('Ariel','15'),
                             fg='red',command=self.cancela)
        self.botao3.place(relx=0.34,rely=0.25,height=40,width=200)
        #Botão Imprimir
        self.botao2 = Button(self.abas_pg1, text="Imprimir", font=('Ariel','15'),
                             fg='green',command=self.imprimir)
        self.botao2.place(relx=0.35,rely=0.40,height=46,width=167)
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
        scrollbar.place(relx=0.99,rely=0.52,relheight=0.450)
        
        self.listbox = Listbox(self.abas_pg1,selectmode='single',font=('Courier','15'),fg="blue")
        self.listbox.place(relx=0.0,rely=0.52,relwidth=0.987,relheight=0.450)
        self.listbox.config(yscrollcommand=scrollbar.set)        
        scrollbar.config(command=self.listbox.yview)
#-------------------------------Aba Clientes-------------------------------------------------------------------------
        self.frame1 = Frame(self.abas_pg2)
        self.frame1.configure(relief=GROOVE)
        self.frame1.configure(borderwidth="2")
        self.frame1.place(relx=0.0,rely=0.0,relheight=1.0,relwidth=0.50)
        Label(self.frame1,text='CADASTRO',font=('Ariel','30'), fg='blue').place(relx=0.30,rely=0.01)
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
        
        self.botaocancela = Button(self.frame1,text='Limpar/Cancelar',font=('Ariel','20'),
                                   fg='blue',command=self.limpaclientes)
        self.botaocancela.place(relx=0.62,rely=0.44,relwidth=0.31)

        self.botao_alt_cliente = Button(self.frame1, text='Alterar', font=('Ariel', '20'),
                                        fg='red', command = self.alt_cliente)
        self.botao_alt_cliente.place(relx = 0.62, rely = 0.55, relwidth = 0.31)
        
        self.frame2 = Frame(self.abas_pg2)
        self.frame2.configure(relief=GROOVE)
        self.frame2.configure(borderwidth="2")
        self.frame2.place(relx=0.50,rely=0.0,relheight=0.31,relwidth=0.50)

        Label(self.frame2,text='CONSULTA',font=('Ariel','30'), fg='blue').place(relx=0.32,rely=0.05)
        self.consulta= AutocompleteCombobox(self.frame2,font=("Ariel","15"))
        
        #self.consulta["values"] = self.col
        self.consulta.bind("<<ComboboxSelected>>",self.mostraclientes)
        self.consulta.bind("<Return>",self.mostraclientes)
        self.consulta.bind("<KP_Enter>",self.mostraclientes)
        self.consulta.place(relx=0.29,rely=0.47)

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

        Label(self.frame4, text=u"Referência",font=('Ariel','18'),fg='blue').place(relx=0.58,rely=0.00)
        self.ref_estoque=Entry(self.frame4, width=15, font=('Ariel','18'))
        self.ref_estoque.bind("<Return>",self.pesquisa_referencia_bind)
        self.ref_estoque.bind("<KP_Enter>",self.pesquisa_referencia_bind)
        self.ref_estoque.place(relx=0.58,rely=0.07)

        self.botao_pesq_produto = Button(self.frame4,text='Pesquisar',font=('Arial','20'),
                                         command=self.pesquisa_referencia)
        self.botao_pesq_produto.place(relx=0.85,rely=0.07)

        Label(self.frame4, text=u"Descrição",font=('Ariel','18'),fg='blue').place(relx=0.58,rely=0.15)
        self.lista_referencia()

        self.botao_del_produto = Button(self.frame4,text='Apagar',font=('Arial','25'),fg='red',
                                        command=self.deleta_produto)
        self.botao_del_produto.place(relx=0.88,rely=0.45)

#--------------------------------------Aba Relatórios-------------------------------------------------------------------
        Button(self.abas_pg4,text='Mais Vendido',font=('Courier','20'),
                command=self.rel_mais_vendido).place(relx=0.01,rely=0.01)

        Button(self.abas_pg4,text='Por Data',font=('Courier','20'),
                command=self.janela_data).place(relx=0.01,rely=0.10)

        Button(self.abas_pg4,text='Por vendedor',font=('Courier','20'),
                command=self.janela_vend_data).place(relx=0.01,rely=0.20)

        Button(self.abas_pg4,text='Por Cliente',font=('Courier','20'),
                command=self.janela_rel_cliente).place(relx=0.01,rely=0.30)
        
        self.lista_estoque()
        self.lista_clientes()
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
        if ref == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo referência')
        elif desc == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo descrição')
        elif precov == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo preço varejo')
        elif precoa == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo preço atacado')
        else:
            qt = 0
            try:
                cur.execute("INSERT INTO produtos VALUES(?,?,?,?,?,?,?,?,?)",(ref,desc,precov,precoa,qt,qt,qt,qt,qt))
                self.cancela_cadastro()
                tkMessageBox.showinfo('Aviso!',u'Produto cadastrado com sucesso')
            except:
                tkMessageBox.showinfo('Aviso!',u'Referência já existente, ou valor inválido')
            con.commit()
            self.lista_estoque()
            self.lista_referencia()
                        

    #Função Cancela cadastro
    def cancela_cadastro(self):
        self.ref_c.delete(0,END)
        self.desc_c.delete(0,END)
        self.precov.delete(0,END)
        self.precoa.delete(0,END)

    def lista_clientes(self):
        cur.execute("SELECT cl FROM clientes ORDER BY cl")
        self.clientes = cur.fetchall()
        self.clientes = [cli[0] for cli in self.clientes]
        self.consulta.set_completion_list(self.clientes)
        self.venda_cliente.set_completion_list(self.clientes)        

    def lista_referencia(self):
        self.consulta_ref= AutocompleteCombobox(self.frame4,font=("Ariel","18"))
        cur.execute("SELECT descricao FROM produtos ORDER BY descricao")
        self.col = cur.fetchall()
        self.col = [cli[0] for cli in self.col]
        self.consulta_ref.set_completion_list(self.col)
        self.consulta_ref.bind("<<ComboboxSelected>>",self.consulta_referencia)
        self.consulta_ref.bind("<Return>",self.consulta_referencia)
        self.consulta_ref.bind("<KP_Enter>",self.mostraclientes)
        self.consulta_ref.place(relx=0.58,rely=0.20)

    def lista_vendedores(self):
        self.vendedor= AutocompleteCombobox(self.abas_pg1,font=("Ariel","18"),width=7)
        cur.execute("SELECT vendedor FROM vendedores ORDER BY vendedor")
        listav = cur.fetchall()
        listav = [cli[0] for cli in listav]
        self.vendedor.set_completion_list(listav)
        self.vendedor.place(relx=0.0,rely=0.07)     

    def consulta_referencia(self,event):
        self.ref_estoque.delete(0,END)
        desc_pesq = self.consulta_ref.get()
        cur.execute('SELECT ref FROM produtos WHERE descricao = "%s"' %desc_pesq)
        item = cur.fetchone()
        self.ref_estoque.insert(END,item)
        self.pesquisa_referencia()
        
                
    #Função pedido
    def pedido(self):      
        ref = self.ref.get() #Pega o valor da referencia digitado
        cliente = self.venda_cliente.get() # Entrada do cliente
        if ref == '': # Checa se campo referência está preenchido
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo referência')
        else:
            pp = float(self.pp_quant.get())
            p = float(self.p_quant.get())
            m = float(self.m_quant.get())
            g = float(self.g_quant.get())
            gg =float(self.gg_quant.get()) 
            quant = pp+p+m+g+gg #Soma da quantidade de peças por tamanho
            cur.execute("SELECT * FROM produtos WHERE ref = %s" %ref) #Consulta pela referencia
            item = cur.fetchone()
            desc = item[1]
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
            total = total-desconto #Aplica desconto
            vendedor = self.vendedor.get()
            if vendedor == '': # Checa se campo referência está preenchido
                tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo vendedor')
            else:
                cur.execute("INSERT INTO pedido VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (None,ref,quant,desc,precof,total,pp,p,m,g,gg,vendedor,cliente)) # Insere dados na table pedido
                con.commit() #Insere dados na tabela pedido
                tb=cur.execute("SELECT * FROM pedido") #Pesquisa tudo na tabela pedido
                self.listbox.delete(0,END) #Limpa a listbox
                #Insere os dados na lista
                self.listbox.insert(END,"Ref         Qtd                    Descricao                    Unit        Total")
                tb = list(tb)
                for i in tb: 
                    self.listbox.insert(END,u"{:.<9}{:.^10}{:.^43}{:.^8.2f}{:.>12.2f}" .format(i[1],i[2],i[3],i[4],i[5]))#Insere dados na listbox
                    self.listbox.select_clear(self.listbox.size() - 2)
                    self.listbox.select_set(END)
                    self.listbox.yview(END)
                    cur.execute("SELECT SUM(total)FROM pedido")#Soma total
                    totalp = cur.fetchone()
                    self.totalp.delete(0,END) #Limpa Total
                    self.totalp.insert(END,"R$:%.2f"%totalp)#Insere total
                self.zera_pedido()
                
        

    def cancela(self):
        cur.execute("DELETE FROM pedido WHERE 1")#Apaga pedido
        self.listbox.delete(0,END) #Limpa a listbox
        self.ref.delete(0,END)#Apaga campo referencia
        self.totalp.delete(0,END)#Apaga campo Total do Pedido
        self.zera_desconto()
        con.commit()
        
    def cadastraclientes(self):
        cliente=self.cliente.get()
        endereco=self.endereco.get()
        cidade=self.cidade.get()
        cep=self.cep.get()
        cpf=self.cpf.get()
        fone=self.fone.get()
        mail=self.mail.get()
        comp=self.comp.get(0.0,END)
        if cliente == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo cliente')
        elif endereco == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo endereço')
        elif cidade == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo cidade')
        elif fone == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo telefone')
        else:
            cur.execute("INSERT INTO clientes VALUES(?,?,?,?,?,?,?,?,?)",
                        (None,cliente,endereco,cidade,cep,cpf,fone,mail,comp))
            con.commit()
            self.limpaclientes()
            tkMessageBox.showinfo('Aviso!',u'Cliente cadastrado com sucesso')
            cur.execute("SELECT cl FROM clientes ORDER BY cl")
            self.col = cur.fetchall()
            self.col = [cli[0] for cli in self.col]
            self.consulta["values"] = self.col
        self.lista_clientes()

    def limpaclientes(self):
        self.cliente.delete(0,END)
        self.endereco.delete(0,END)
        self.cidade.delete(0,END)
        self.cep.delete(0,END)
        self.cpf.delete(0,END)
        self.fone.delete(0,END)
        self.mail.delete(0,END)
        self.comp.delete(0.0,END)
        self.mostra1.delete(0.0,END)
        #self.consulta.delete(0,END)

    def mostraclientes(self,event):
        self.limpaclientes()
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
        self.cliente.insert(END,i[1])
        self.endereco.insert(END,i[2])
        self.cidade.insert(END,i[3])
        self.cep.insert(END,i[4])
        self.cpf.insert(END,i[5])
        self.fone.insert(END,i[6])
        self.mail.insert(END,i[7])
        self.comp.insert(END,i[8])

    def alt_cliente(self):
        i = self.consulta.get()
        cliente=self.cliente.get()
        endereco=self.endereco.get()
        cidade=self.cidade.get()
        cep=self.cep.get()
        cpf=self.cpf.get()
        fone=self.fone.get()
        mail=self.mail.get()
        comp=self.comp.get(0.0,END)
        if cliente == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo cliente')
        elif endereco == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo endereço')
        elif cidade == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo cidade')
        elif fone == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo telefone')
        else:
            cur.execute('''UPDATE clientes SET cl = ?,
                        endereco = ?,
                        cidade = ?,
                        cep = ?,
                        cpf = ?,
                        fone = ?,
                        mail = ?,
                        comp = ?
                        WHERE cl = ?''',
                        (cliente,endereco,cidade,cep,cpf,fone,mail,comp,i))
            con.commit()
            self.limpaclientes()
            tkMessageBox.showinfo('Aviso!',u'Cliente alterado com sucesso')    
            
    #Função Imprimir
    def imprimir(self):
        outfile = open('outfile.txt','w')
        cabecalho = '''------------------------------------LINE FITNESS-------------------------------------
---------------------------E-mail: linefitness2014@gmail.com-------------------------
--------------------------------Fone: (47) 9682 6062---------------------------------'''
        outfile.write(cabecalho+'\n\n\n')
        tb=self.listbox.get(0,END)        
        for i in tb: 
            i=(u"{}\n" .format(i))
            outfile.write(i.encode('utf-8'))
        totalprint = "Total do Pedido:" + 57*'-'+ str(self.totalp.get())
        outfile.write('\n\n'+totalprint)
        outfile.close()
        #subprocess.call(['notepad.exe','/p','outfile.txt'])*2 #versão notepad windows
        #subprocess.call(['swriter','outfile.txt']) #Linux writer
        self.diminui_estoque()
        self.cadastra_venda()
        self.cancela()        
        
#-------------------------------------Funções de Estoque----------------------------------------------------
    def lista_estoque(self):
        #Limpar lista
        for i in self.arvore.get_children():
            self.arvore.delete(i)
        #Consulta BD e preenche a lista    
        dados=cur.execute('SELECT ref,descricao,pp,p,m,g,gg FROM produtos ORDER BY ref')
        for item in dados:
            self.arvore.insert('','end',values=item)
        self.arvore.bind('<<TreeviewSelect>>',self.itemselect)

    def itemselect(self,event):
        self.ref_estoque.delete(0,END)
        self.consulta_ref.delete(0,END)
        self.limpa_estoque()       
        item = self.arvore.selection()
        item = self.arvore.item(item,'values')
        #Preenche os campos        
        self.ref_estoque.insert(END,item[0])
        self.consulta_ref.insert(END,item[1])
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
        self.consulta_ref.delete(0,END)
        
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

    def pesquisa_referencia_bind(self, event):
        self.pesquisa_referencia()

    def pesquisa_referencia(self):
        ref_pesq = self.ref_estoque.get()
        try:
            cur.execute('SELECT * FROM produtos WHERE ref = %s'%ref_pesq)
            item = cur.fetchone()
            self.limpa_estoque()
            self.pp_estoque.insert(END,item[4])
            self.p_estoque.insert(END,item[5])
            self.m_estoque.insert(END,item[6])
            self.g_estoque.insert(END,item[7])
            self.gg_estoque.insert(END,item[8])
            self.consulta_ref.insert(END,item[1]) #insere descrição na combobox      
            self.lista_estoque()
        except:
            tkMessageBox.showinfo('Aviso!',u'Referência inválida')
       
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

    def cadastra_venda(self):
        hoje = date.today()
        #hoje = hoje.strftime('%d/%m/%Y')
        cur.execute("SELECT * FROM pedido")
        pedido=cur.fetchall()
        for i in pedido:
            cur.execute("INSERT INTO vendas VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (hoje,i[1],i[2],i[3],i[4],i[5],i[6],
                         i[7],i[8],i[9],i[10],i[11],i[12]))
        con.commit()

    def cadastra_vendedor(self):
        vendedor = self.vend_c.get()
        senhac = self.senha_c.get()
        if vendedor == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo vendedor')
        elif senhac == '':
            tkMessageBox.showwarning('Aviso!',u'Você precisa preencher o campo senha')
        else:
            try:
                cur.execute("INSERT INTO vendedores VALUES(?,?)",
                        (vendedor,senhac))
                tkMessageBox.showwarning('Aviso!',u'Vendedor cadastardo com sucesso.')
                con.commit()
            except:
                tkMessageBox.showwarning('Erro!',u'Vendedor já cadastardo ou inválido.')
        self.vend_c.delete(0,END)
        self.senha_c.delete(0,END)
        self.lista_vendedores()   
        

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

#-----------------------Funções de relatórios--------------------------------
    def rel_mais_vendido(self):
        relatorios.mais_vendido()
        subprocess.call(['swriter', 'mais_vendido.txt'])

    def janela_data(self):
        self.top2 = Toplevel(bg='sky blue')
        #self.top2.geometry("500 x 700")

        Label(self.top2,text='Data inicial',bg='sky blue',font=('Arial','14')).place(relx=0.0,rely=0.00)
        self.rel_data_inicial = MaskedWidget(self.top2, 'fixed', font=("Ariel","14"), width=18, mask="99/99/9999")
        self.rel_data_inicial.place(relx=0.0,rely=0.15)
        Label(self.top2,text='Data final',bg='sky blue',font=('Arial','14')).place(relx=0.0,rely=0.35)
        self.rel_data_final = MaskedWidget(self.top2, 'fixed', font=("Ariel","14"), width=18, mask="99/99/9999")
        self.rel_data_final.place(relx=0.0,rely=0.48)

        botao = Button(self.top2,text='OK',fg='green',font=('Arial','14'),
                       command=self.rel_data).place(relx=0.25,rely=0.70,width=100)

    def rel_data(self):
        datai = self.rel_data_inicial.get()
        datai = datai[6:] + "-" + datai[3:5] + "-" + datai[:2] #Converte dd/mm/aaaa para aaaa-mm-dd
        dataf = self.rel_data_final.get()
        dataf = dataf[6:] + "-" + dataf[3:5] + "-" + dataf[:2] #Converte dd/mm/aaaa para aaaa-mm-dd
        self.top2.destroy()
        relatorios.reldata(datai,dataf)
        subprocess.call(['swriter', 'pordata.txt'])

    def janela_vend_data(self):
        self.top3 = Toplevel(bg='sky blue')
        self.top3.geometry("%dx%d" %(200,300))
        Label(self.top3,text='Vendedor',bg='sky blue',font=('Arial','14')).place(relx=0.22,rely=0.02)
        self.box_vendedor2= AutocompleteCombobox(self.top3,font=("Ariel","14"),width=10)
        cur.execute("SELECT vendedor FROM vendedores ORDER BY vendedor")
        listav = cur.fetchall()
        listav = [cli[0] for cli in listav]
        self.box_vendedor2.set_completion_list(listav)
        self.box_vendedor2.place(relx=0.20,rely=0.10)

        Label(self.top3,text='Data inicial',bg='sky blue',font=('Arial','14')).place(relx=0.20, rely=0.30)
        self.rel_data_inicial2 = MaskedWidget(self.top3, 'fixed', font=("Ariel","14"), width=18, mask="99/99/9999")
        self.rel_data_inicial2.place(relx=0.0, rely=0.40)
        Label(self.top3,text='Data final',bg='sky blue',font=('Arial','14')).place(relx=0.20, rely=0.60)
        self.rel_data_final2 = MaskedWidget(self.top3, 'fixed', font=("Ariel","14"), width=18, mask="99/99/9999")
        self.rel_data_final2.place(relx=0.0, rely=0.68)

        botao = Button(self.top3,text='OK',fg='green',font=('Arial','14'),
                       command=self.rel_data_vend).place(relx=0.25,rely=0.85,width=100)

    def rel_data_vend(self):
        vend = self.box_vendedor2.get()
        datai = self.rel_data_inicial2.get()
        datai = datai[6:] + "-" + datai[3:5] + "-" + datai[:2] #Converte dd/mm/aaaa para aaaa-mm-dd
        dataf = self.rel_data_final2.get()
        dataf = dataf[6:] + "-" + dataf[3:5] + "-" + dataf[:2] #Converte dd/mm/aaaa para aaaa-mm-dd
        self.top3.destroy()
        relatorios.reldatavend(datai,dataf,vend)
        subprocess.call(['swriter', 'pordata_e_vendedor.txt'])

    def janela_rel_cliente(self):
        self.top4 = Toplevel(bg='sky blue')
        self.top4.geometry("%dx%d" %(200,300))
        Label(self.top4,text='Cliente',bg='sky blue',font=('Arial','14')).place(relx=0.22,rely=0.02)
        self.box_cliente= AutocompleteCombobox(self.top4,font=("Ariel","14"),width=10)
             
        self.box_cliente.set_completion_list(self.clientes) #Dados vindos da função lista_clientes
        self.box_cliente.place(relx=0.20,rely=0.10)

        Label(self.top4,text='Data inicial',bg='sky blue',font=('Arial','14')).place(relx=0.20, rely=0.30)
        self.rel_data_inicial3 = MaskedWidget(self.top4, 'fixed', font=("Ariel","14"), width=18, mask="99/99/9999")
        self.rel_data_inicial3.place(relx=0.0, rely=0.40)
        Label(self.top4,text='Data final',bg='sky blue',font=('Arial','14')).place(relx=0.20, rely=0.60)
        self.rel_data_final3 = MaskedWidget(self.top4, 'fixed', font=("Ariel","14"), width=18, mask="99/99/9999")
        self.rel_data_final3.place(relx=0.0, rely=0.68)

        botao = Button(self.top4,text='OK',fg='green',font=('Arial','14'),
                       command=self.rel_cliente).place(relx=0.25,rely=0.85,width=100) 

    def rel_cliente(self):
        cliente = self.box_cliente.get()
        datai = self.rel_data_inicial3.get()
        datai = datai[6:] + "-" + datai[3:5] + "-" + datai[:2] #Converte dd/mm/aaaa para aaaa-mm-dd
        dataf = self.rel_data_final3.get()
        dataf = dataf[6:] + "-" + dataf[3:5] + "-" + dataf[:2] #Converte dd/mm/aaaa para aaaa-mm-dd
        if dataf < datai:
            tkMessageBox.showwarning('Aviso', 'Data final deve ser maior que data inicial')
        else:
            self.top4.destroy()
            relatorios.relcliente(datai,dataf,cliente)
            subprocess.call(['swriter', 'porcliente.txt'])



#----------------------Classe de Login---------------------------------------
class Login:
    def __init__(self,janela):
        Label(janela,text='Senha',font=('Arial','16')).place(relx=0.3,rely=0.02)
        self.entrasenha = Entry(janela,font=('Arial','16'),show='*')
        self.entrasenha.place(relx=0.0,rely=0.2)
        self.botao_login=Button(janela, text='Login',font=('Arial','16'),
                                command=self.autentica)
        self.botao_login.place(relx=0.25,rely=0.65)
    
    def autentica(self):
        senha = self.entrasenha.get()
        if senha == '123':
            top.destroy()#Fecha janela de login
            root = Tk()
            root.title("TuxPedidos 1.0")
            root.geometry("1366x768")
            #img = PhotoImage(file='tuxd.png')
            #root.tk.call('wm','iconphoto',root._w,img)
            main(root)
            root.mainloop()#Loop da janela principal
            
        else:
            tkMessageBox.showwarning('Aviso!',u'Senha inválida')
                 
top = Tk()
Login(top)
top.mainloop()#Loop da janela de login

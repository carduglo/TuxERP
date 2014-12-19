# -*- coding: utf-8 -*-
import sqlite3

def cria_tabelas():
    #Criar conexão e cursor com banco de dados
    con = sqlite3.connect('tuxdb.db')
    cur = con.cursor()
    #Criar tabela clientes
    cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 cl TEXT,
                 endereco TEXT,
                 cidade TEXT,
                 cep TEXT,
                 cpf TEXT,
                 fone TEXT,
                 mail TEXT,
                 comp TEXT)""")
    #Criar tabela produtos
    cur.execute('''CREATE TABLE IF NOT EXISTS produtos (
                 ref TEXT primary key NOT NULL,
                 descricao TEXT NOT NULL,
                 precoV dec NOT NULL,
                 precoA dec NOT NULL)''')

    #Cria tabela do pedido
    cur.execute("""CREATE TABLE IF NOT EXISTS pedido (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ref INTEGER NOT NULL,
                 quant INTEGER NOT NULL,
                 descricao TEXT NOT NULL,
                 preco DEC NOT NULL,
                 total DEC NOT NULL,
                 pp INTEGER DEFAULT (0),
                 p INTEGER DEFAULT (0),
                 m INTEGER DEFAULT (0),
                 g INTEGER DEFAULT (0),
                 gg INTEGER DEFAULT (0),
                 vendedor TEXT NOT NULL,
                 cliente TEXT NOT NULL)""")
    
    #Cria tabela vendas
    cur.execute("""CREATE TABLE IF NOT EXISTS vendas (
                 data DATE,
                 ref INTEGER NOT NULL,
                 quant INTEGER NOT NULL,
                 descricao TEXT(100) NOT NULL,
                 preco DEC NOT NULL,
                 total DEC NOT NULL,
                 pp INTEGER DEFAULT (0),
                 p INTEGER DEFAULT (0),
                 m INTEGER DEFAULT (0),
                 g INTEGER DEFAULT (0),
                 gg INTEGER DEFAULT (0),
                 vendedor TEXT NOT NULL,
                 cliente TEXT NOT NUll)""")

    #Cria tabela vendedores
    cur.execute(""" CREATE TABLE IF NOT EXISTS vendedores(
                vendedor TEXT PRIMARY KEY,
                senha TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS estoque(
                ref TEXT,
                descricao TEXT,
                cor TEXT,
                tamanho TEXT,
                quantidade INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS entrada_estoque (
                data DATE,
                ref TEXT,
                descricao TEXT,
                cor TEXT,
                tamanho TEXT,
                quantidade INTEGER )""")
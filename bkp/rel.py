# -*- coding: UTF-8 -*-

'''notepad com fonte Lucida Console - Regular - 10'''

import sqlite3
import subprocess

#Criar conexão e cursor com banco de dados
con = sqlite3.connect('tuxdb.db')
cursor = con.cursor()


def relvendedor(vendedor):
	''' Função relatório por vendedor.
    Retorna tupla com os dados.
	Ex. de uso: variavel = relvendedor('nome do vendedor')
    	        print variável'''
	cursor.execute("SELECT * FROM vendas WHERE vendedor = '%s'" %vendedor)
	resultado = cursor.fetchall()
	outfile = open('vendedor.txt','w')
	cabecalho = u'Data........Ref.......Quantidade.....Descricao................Preco.....Total \n\n'
	outfile.write(cabecalho)
	for i in resultado:
		i=(u"{:.<12}{:.<10d}{:.<15}{:.<25}{:.<10.2f}{:.2f}\n" .format(i[0],i[1],i[2],i[3],i[4],i[5]))
		outfile.write(i.encode('utf-8'))
	cursor.execute("SELECT SUM(total)FROM vendas WHERE vendedor = '%s'" %vendedor)
	total = float(cursor.fetchone()[0])
	total = "\n\nTotal:.............................................................R$ %.2f" %total
	outfile.write(total)
	outfile.close()
	
def reldata(datai, dataf):
	'''Função relatório por datas
   	Ex. de uso: res = reldata('2014-10-01', '2014-10-31')
    	        print res'''
	cursor.execute(" SELECT * FROM vendas WHERE data BETWEEN '%s' AND '%s' "%(datai,dataf))
	resultado = cursor.fetchall()
	outfile = open('pordata.txt','w')
	cabecalho = u'Data........Ref.......Quantidade.....Descrição................Preço.....Total \n\n'
	outfile.write(cabecalho.encode('utf-8'))
	for i in resultado:
		i=(u"{:.<12}{:.<10d}{:.<15}{:.<25}{:.<10.2f}{:.2f}\n" .format(i[0],i[1],i[2],i[3],i[4],i[5]))
		outfile.write(i.encode('utf-8'))
	cursor.execute("SELECT SUM(total)FROM vendas WHERE data BETWEEN '%s' AND '%s' "%(datai,dataf))
	total = float(cursor.fetchone()[0])
	total = "\n\nTotal:.............................................................R$ %.2f" %total
	outfile.write(total)
	outfile.close()

def reldatavend(datai, dataf, vendedor):
	'''Função relatório por datas
   	Ex. de uso: res = reldata('2014-10-01', '2014-10-31', 'vendedor')
    	        print res'''
	cursor.execute(" SELECT * FROM vendas WHERE data BETWEEN '%s' AND '%s' AND vendedor = '%s' "%(datai,dataf,vendedor))
	resultado = cursor.fetchall()
	outfile = open('pordata_e_vendedor.txt','w')
	cabecalho = u'Data........Ref.......Quantidade.....Descrição................Preço.....Total \n\n'
	outfile.write(cabecalho.encode('utf-8'))
	for i in resultado:
		i=(u"{:.<12}{:.<10d}{:.<15}{:.<25}{:.<10.2f}{:.2f}\n" .format(i[0],i[1],i[2],i[3],i[4],i[5]))
		outfile.write(i.encode('utf-8'))
	cursor.execute("SELECT SUM(total)FROM vendas WHERE data BETWEEN '%s' AND '%s' AND vendedor = '%s' "%(datai,dataf,vendedor))
	total = float(cursor.fetchone()[0])
	total = "\n\nTotal:.............................................................R$ %.2f" %total
	outfile.write(total)
	outfile.close()

def relcliente(datai, dataf, cliente):
	'''Função relatório por datas
   	Ex. de uso: res = relcliente('2014-10-01', '2014-10-31', 'cliente')
    	        print res'''
	cursor.execute("SELECT * FROM vendas WHERE data BETWEEN '%s' AND '%s' AND cliente = '%s'" %(datai, dataf, cliente))
	resultado = cursor.fetchall()
	outfile = open('porcliente.txt', 'w')
	cabecalho = u'CLIENTE = %s \n\nData........Ref.......Quantidade.....Descrição................Preço.....Total \n\n' %(cliente)
	outfile.write(cabecalho.encode('utf-8'))
	for i in resultado:
		i=(u"{:.<12}{:.<10d}{:.<15}{:.<25}{:.<10.2f}{:.2f}\n" .format(i[0],i[1],i[2],i[3],i[4],i[5]))
		outfile.write(i.encode('utf-8'))
	cursor.execute("SELECT SUM(total)FROM vendas WHERE data BETWEEN '%s' AND '%s' AND cliente = '%s' "%(datai, dataf, cliente))
	total = float(cursor.fetchone()[0])
	total = "\n\nTotal:.............................................................R$ %.2f" %total
	outfile.write(total)
	outfile.close()

def mais_vendido():
	cursor.execute('''SELECT ref, descricao,
					 SUM(pp),
					 SUM(p),
					 SUM(m),
					 SUM(g),
					 SUM(gg),
					 SUM(quant)
					 FROM vendas GROUP BY ref ORDER BY SUM (quant) DESC''')
	resultado = cursor.fetchall()
	outfile = open('mais_vendido.txt', 'w')
	cabecalho = u'Ref...Descrição...........PP........P.........M.........G.........GG.......Total\n\n'
	outfile.write(cabecalho.encode('utf-8'))
	for i in resultado:
		i = (u"{:.<6}{:.<20}{:.<10}{:.<10}{:.<10}{:.<10}{:.<9}{}\n" .format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
		outfile.write(i.encode('utf-8'))
	outfile.close()

if __name__ == '__main__':
	pass
	#relcliente('2014-10-01', '2014-10-31', 'Dino da Silva Sauro')
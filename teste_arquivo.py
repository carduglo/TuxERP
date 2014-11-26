# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

lista = [('saia','blusa'), ('farinha','sabão')]

arquivo = open('arquivo.txt','w') 
for i in lista:
	i = ('%u   %u \n' %(i[0],i[1]))
	arquivo.write(i)
arquivo.close()

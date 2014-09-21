def diminui_estoque(self):
        tb=cur.execute('SELECT ref,pp,p,m,g,gg FROM pedido')
        for i in tb:
            print i
            cur.execute('UPDATE produtos SET pp = pp-? WHERE ref = ?',
                        (i[1],i[0]))
        #con.commit
        #self.lista_estoque()

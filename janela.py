from tkinter import *
from tkinter import Tk
from tkinter import ttk
import sqlite3
import uuid
import pandas as pd

janela = Tk()

class Funcs():
    
    # Limpa os campos de entrada
    def limpaTela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.quant_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        
    # Conecta ao banco de dados
    def Conectadb(self):
        self.conn = sqlite3.connect('produtos_cadastrados.db')
        self.cursor = self.conn.cursor()
       
    def deconectadb(self):
    # Desconecta do banco de dados  
        self.conn.close()  
        
    def criardb(self):
    # Cria um banco de dados para produtos cadastrados
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS produtos_cadstrados(
                                codigo INTEGER PRIMARY KEY,
                                produto CHAR (40) NOT NULL,
                                valor REAL
                            )
                            """)
        self.conn.commit()
        
    def criardb1(self):
    #cria um banco de dados para produtos pagos
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS produtos_pagos(
                                
                                pagamento_id CHAR(999) PRIMARY KEY,
                                codigo INTEGER ,
                                produto CHAR (40) NOT NULL,
                                quantidade INTEGER,
                                valor REAL,
                                total REAL
                            )
                            """)
        self.conn.commit()
        
    def criardb2(self):
    #  Cria um banco de dados para o carrinho
            self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS carrinho(
                                
                                pagamento_id CHAR(999) PRIMARY KEY,
                                codigo INTEGER ,
                                produto CHAR (40) NOT NULL,
                                quantidade INTEGER,
                                valor REAL,
                                total REAL
                            )
                            """)
            self.conn.commit()
        
    def add_produtos(self):
    # cadastra produtos
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.quant = self.quant_entry.get()
        self.valor = self.valor_entry.get()
        self.Conectadb()
        self.cursor.execute("INSERT INTO produtos_cadstrados (codigo, produto,  valor) VALUES (?, ?, ?)", (self.codigo, self.nome, self.valor))  # Corrigido: valores passados como tupla
        self.conn.commit()
        
        self.limpaTela()
        
        self.deconectadb()
        
    def add_comprados(self):
        #coloca os itens no produtos pagos
        
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.quant = int(self.quant_entry.get())
        self.valor = float(self.valor_entry.get())
        self.total = self.quant * self.valor
        self.pagamento_id = str(uuid.uuid4())
        self.Conectadb()
        self.cursor.execute("INSERT INTO produtos_pagos (pagamento_id, codigo, produto, quantidade, valor, total) VALUES (?, ?, ?,?,?,?)", (self.pagamento_id, self.codigo, self.nome,self.quant, self.valor,self.total))
        self.conn.commit()
        self.atualizar_total()
        
        self.limpaTela()
        
        self.deconectadb()
        
    def carrinho(self):
        #coloca os itens no carrinho
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.quant = int(self.quant_entry.get())
        self.valor = float(self.valor_entry.get())
        self.total = self.quant * self.valor
        self.pagamento_id = str(uuid.uuid4())
        self.Conectadb()
        
        self.cursor.execute("INSERT INTO carrinho (pagamento_id, codigo, produto, quantidade, valor, total) VALUES (?, ?, ?,?,?,?)", (self.pagamento_id, self.codigo, self.nome,self.quant, self.valor,self.total))
        self.cursor.execute("INSERT INTO produtos_pagos (pagamento_id, codigo, produto, quantidade, valor, total) VALUES (?, ?, ?,?,?,?)", (self.pagamento_id, self.codigo, self.nome,self.quant, self.valor,self.total))
        self.conn.commit()
        
        
        self.select_pg()
        self.atualizar_total()
        
        
       
        
      
    
        self.limpaTela()
        self.deconectadb()
        
        self.limpaTela()
        
        self.deconectadb()
        
    def del_carrinho(self):
        #deleta os itens do carrinho para uma nova compra
        self.Conectadb()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS carrinho(
                                
                                pagamento_id CHAR(999) PRIMARY KEY,
                                codigo INTEGER ,
                                produto CHAR (40) NOT NULL,
                                quantidade INTEGER,
                                valor REAL,
                                total REAL
                            )
                            """)
            
        self.conn.commit()
        
        self.cursor.execute("DROP TABLE IF EXISTS carrinho")
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS carrinho(
                                
                                pagamento_id CHAR(999) PRIMARY KEY,
                                codigo INTEGER ,
                                produto CHAR (40) NOT NULL,
                                quantidade INTEGER,
                                valor REAL,
                                total REAL
                            )
                            """)
            
        self.conn.commit()
        
        self.select_pg()# Desconecta do banco de dados  
        self.atualizar_total()
        self.deconectadb()
       
        
    def select(self):
        #manda os itens adcionados para a lista do carrinho na interface
        self.lista_cl.delete(*self.lista_cl.get_children())  
        self.Conectadb()
        
        lista = self.cursor.execute("""SELECT codigo, produto, valor FROM produtos_cadstrados
                                    ORDER BY codigo ASC;""")  
        for i in lista:
            self.lista_cl.insert("", END, values=i)
        self.conn.commit()
        self.deconectadb()
        self.limpaTela()
        
    def select_pg(self):
        
        self.lista_cl.delete(*self.lista_cl.get_children())  
        self.Conectadb()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS carrinho(
                                
                                pagamento_id CHAR(999) PRIMARY KEY,
                                codigo INTEGER ,
                                produto CHAR (40) NOT NULL,
                                quantidade INTEGER,
                                valor REAL,
                                total REAL
                            )
                            """)
            
        self.conn.commit()
        
        lista = self.cursor.execute("""SELECT codigo, produto, quantidade, valor,total FROM carrinho
                                    ORDER BY codigo ASC;""")  
        
        for i in lista:
            self.lista_cl.insert("", END, values=i)
        self.conn.commit()
        self.deconectadb()
        self.limpaTela()
        
        
    def buscar_item(self, event=None):
        #busca itens da tabela produtos cadstrados
        
        self.Conectadb()
        self.codigo = int(self.codigo_entry.get())
       
        
        self.cursor.execute("""SELECT produto, valor FROM produtos_cadstrados WHERE codigo=?""", (self.codigo,))


        self.item = self.cursor.fetchone()
        if self.item:
            self.nome_entry.delete(0, END)  # Limpa o campo antes de preencher
            self.nome_entry.insert(0, self.item[0])  # Preenche o campo com o nome do item
            self.valor_entry.delete(0, END)  # Limpa o campo antes de preencher
            self.valor_entry.insert(0, self.item[1])  # Preenche o campo com o preço do item
            
            
    def calcular_total_carrinho(self):
    # calcula o total dos valores que estao no carrinho
        self.Conectadb()
        self.total = self.cursor.execute("SELECT SUM(total) FROM carrinho").fetchone()[0] or 0
        
           
        return self.total
        
    def atualizar_total(self):
    #atualiza o total a cada item adcionado
        self.total_carrinho = self.calcular_total_carrinho()
        self.total_text.set(f"TOTAL: R${self.total_carrinho:.2f}")

    
        
        
        
   
        
        
        
        
class Aplication(Funcs):
#cria a classe que vai rodar a aplicação
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1()
        self.lista_frame2()
        self.total_text = StringVar()
        self.widgets_frame_3()
        self.select_pg()
        self.Conectadb()
        self.criardb()
        self.criardb1()
        self.criardb2()
        
      
      
        
        
        self.del_carrinho()
     
        self.total_text.set("TOTAL: R$0.00")
        
        
        janela.mainloop()
        
    def tela(self):
    # Cria a tela
        self.janela.title('cadastro de mercadorias')
        self.janela.configure(background='#1e3743')
        self.janela.geometry('1080x720')
        
    def frames_da_tela(self):
    #cria os frams dentro da tela
        self.frame_1 = Frame(self.janela, bd=4, background='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        
        self.frame_2 = Frame(self.janela, bd=4, background='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.30)
        
        self.frame_3 = Frame(self.janela, bd=4, background='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_3.place(relx=0.02, rely=0.83, relwidth=0.96, relheight=0.15)
        
    def widgets_frame_1(self):
    # adciona widgets ao frame 1
        self.bt_limpar = Button(self.frame_1, text='adicionar', command=self.carrinho)
        self.bt_limpar.place(relx=0.82, rely=0.47, relwidth=0.1, relheight=0.15)

        self.bt_buscar = Button(self.frame_1, text='buscar', command=self.buscar_item)
        self.bt_buscar.place(relx=0.1, rely=0.1, relwidth=0.1, relheight=0.15)
        
        
        self.janela.bind('<Return>', self.buscar_item)
        
        
        
        

        self.bt_novo = Button(self.frame_1, text='adcionar \r produto', command=self.add_produtos)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        

        

        self.lb_codigo = Label(self.frame_1, text='codigo')
        self.lb_codigo.place(relx=0.03, rely=0.05)

        self.lb_valor = Label(self.frame_1, text='valor')
        self.lb_valor.place(relx=0.95, rely=0.29)

        self.valor_entry = Entry(self.frame_1)
        self.valor_entry.place(relx=0.92, rely=0.35, relwidth=0.10, relheight=0.12)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.01, rely=0.13, relwidth=0.09, relheight=0.09)

        self.lb_nome = Label(self.frame_1, text='produto')
        self.lb_nome.place(relx=0.4, rely=0.29)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.01, rely=0.35, relwidth=0.8, relheight=0.12)

        self.lb_quant = Label(self.frame_1, text='quantidade')
        self.lb_quant.place(relx=0.82, rely=0.29)

        self.quant_entry = Entry(self.frame_1)
        self.quant_entry.place(relx=0.82, rely=0.35, relwidth=0.10, relheight=0.12)

        
    def lista_frame2(self):
    #adciona widgets para o fram 2
        self.bt_alterar = Button(self.frame_2, text='pagar', command=self.del_carrinho)
        self.bt_alterar.place(relx=0.83, rely=0.20, relwidth=0.1, relheight=0.25)
        
        self.lista_cl = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.lista_cl.heading("#0", text=" ")
        self.lista_cl.heading("#1", text="codigo")
        self.lista_cl.heading("#2", text="produto")
        self.lista_cl.heading("#3", text="quantidade")
        self.lista_cl.heading("#4", text="valor")
        self.lista_cl.heading("#5", text="TOTAL")
        
        self.lista_cl.column("#0", width=1)
        self.lista_cl.column("#1", width=50)
        self.lista_cl.column("#2", width=250)
        self.lista_cl.column("#3", width=225)
        self.lista_cl.column("#4", width=100)
        self.lista_cl.column("#5", width=100)
        
        self.lista_cl.place(relx=0.01, rely=0.01, relwidth=0.80, relheight=0.85)
        
        self.scrool = Scrollbar(self.frame_2, orient='vertical')
        self.lista_cl.configure(yscroll=self.scrool.set)
        self.scrool.place(relx=0.96, rely=0.1, relheight=0.78, relwidth=0.03)
        
    def widgets_frame_3(self):
    #adciona widgets para o fram 3
        self.lb_totalLb = Label(self.frame_3, text='TOTAL:')
        self.lb_totalLb.place(relx=0.03, rely=0.23, relheight=0.5, relwidth=0.5)
        
        # Vincule a variável StringVar ao Label
        self.total = Label(self.frame_3, textvariable= self.total_text)
        self.total.place(relx=0.5, rely=0.23, relheight=0.5, relwidth=0.5)
        
        self.total_carrinho = self.calcular_total_carrinho()  
        self.atualizar_total()  
        
        
        
       

        
        
 #inicia a aplicação      
Aplication()

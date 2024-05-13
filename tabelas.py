from tkinter import *
from tkinter import ttk

#As funçãos nesse arquivo servem somente para criar as tabelas
#na nossa interface.

def criarTabela(frame):
    global table 
    table = ttk.Treeview(frame, columns = ('ID', 'Produto', 'Linha', 'Classificacao', 'Saldo Estoque', 'Un. Estoque', 'Qtd. Compra', 'Unidade', 'Pç Ultima Compra'), show = 'headings', height=25)
    table.heading('ID', text = 'ID')
    table.heading('Produto', text = 'Produto')
    table.heading('Linha', text = 'Linha')
    table.heading('Classificacao', text = 'Classificacao')
    table.heading('Saldo Estoque', text = 'Saldo Estoque')
    table.heading('Un. Estoque', text = 'Un. Estoque')
    table.heading('Qtd. Compra', text = 'Qtd. Compra')
    table.heading('Unidade', text = 'Unidade')
    table.heading('Pç Ultima Compra', text = 'Pç Ultima Compra')
    table.grid(row=7, column=0, columnspan=2, padx=(80, 0), pady=10, sticky="nsew")

    table.column('ID', width=60, anchor=CENTER)
    table.column('Produto', width=300, anchor=CENTER)
    table.column('Linha', width=160, anchor=CENTER)
    table.column('Classificacao', width=150, anchor=CENTER)
    table.column('Saldo Estoque', width=100, anchor=CENTER)
    table.column('Un. Estoque', width=80, anchor=CENTER)
    table.column('Qtd. Compra', width=90, anchor=CENTER)
    table.column('Unidade', width=60, anchor=CENTER)
    table.column('Pç Ultima Compra', width=120, anchor=CENTER)
 


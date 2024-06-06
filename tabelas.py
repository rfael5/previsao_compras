from tkinter import *
from tkinter import ttk
import connection

#As funçãos nesse arquivo servem somente para criar as tabelas
#na nossa interface.

def criarTabela(frame):
    global table 
    table = ttk.Treeview(frame, columns = ('Produto', 'Linha', 'Classificacao', 'Saldo Estoque', 'Un. Estoque', 'Qtd. Compra', 'Unidade', 'Pç Ultima Compra'), show = 'headings', height=25)
    table.heading('Produto', text = 'Produto')
    table.heading('Linha', text = 'Linha')
    table.heading('Classificacao', text = 'Classificacao')
    table.heading('Saldo Estoque', text = 'Saldo Estoque')
    table.heading('Un. Estoque', text = 'Un. Estoque')
    table.heading('Qtd. Compra', text = 'Qtd. Compra')
    table.heading('Unidade', text = 'Unidade')
    table.heading('Pç Ultima Compra', text = 'Pç Ultima Compra')
    table.grid(row=7, column=0, columnspan=2, padx=(50, 0), pady=10, sticky="nsew")

    table.column('Produto', width=250, anchor=CENTER)
    table.column('Linha', width=160, anchor=CENTER)
    table.column('Classificacao', width=150, anchor=CENTER)
    table.column('Saldo Estoque', width=100, anchor=CENTER)
    table.column('Un. Estoque', width=80, anchor=CENTER)
    table.column('Qtd. Compra', width=90, anchor=CENTER)
    table.column('Unidade', width=60, anchor=CENTER)
    table.column('Pç Ultima Compra', width=120, anchor=CENTER)


def tabelaProdutosFornecedor(frame):
    global tbl_produtos_fornecedor
    tbl_produtos_fornecedor = ttk.Treeview(frame, columns = ('Código', 'Produto', 'Data compra', 'Preço', 'Última compra', 'Último preço', 'Último fornecedor'), show = 'headings', height=25)
    tbl_produtos_fornecedor.heading('Código', text = 'Código')
    tbl_produtos_fornecedor.heading('Produto', text = 'Produto')
    tbl_produtos_fornecedor.heading('Data compra', text = 'Data compra')
    tbl_produtos_fornecedor.heading('Preço', text = 'Preço')
    tbl_produtos_fornecedor.heading('Última compra', text = 'Última compra')
    tbl_produtos_fornecedor.heading('Último preço', text = 'Último preço')
    tbl_produtos_fornecedor.heading('Último fornecedor', text = 'Último fornecedor')
    tbl_produtos_fornecedor.grid(row=1, column=0, columnspan=2, padx=(80, 0), pady=10, sticky="nsew")

    tbl_produtos_fornecedor.column('Código', width=40, anchor=CENTER)
    tbl_produtos_fornecedor.column('Produto', width=200, anchor=CENTER)
    tbl_produtos_fornecedor.column('Data compra', width=100, anchor=CENTER)
    tbl_produtos_fornecedor.column('Preço', width=40, anchor=CENTER)
    tbl_produtos_fornecedor.column('Última compra', width=100, anchor=CENTER)
    tbl_produtos_fornecedor.column('Último preço', width=80, anchor=CENTER)
    tbl_produtos_fornecedor.column('Último fornecedor', width=120, anchor=CENTER)

def tabelaFornecedores(frame):
    global tbl_fornecedores
    tbl_fornecedores = ttk.Treeview(frame, columns = ('ID', 'Fornecedor', 'Nome fantasia', 'CPF/CNPJ'), show = 'headings', height=10)
    tbl_fornecedores.heading('ID', text = 'Fornecedor')
    tbl_fornecedores.heading('Fornecedor', text = 'Fornecedor')
    tbl_fornecedores.heading('Nome fantasia', text = 'Nome fantasia')
    tbl_fornecedores.heading('CPF/CNPJ', text = 'CPF/CNPJ')
    tbl_fornecedores.grid(row=4, column=0, columnspan=2, padx=(80, 0), pady=10, sticky="nsew")

    tbl_fornecedores.column('ID', width=60, anchor=CENTER)
    tbl_fornecedores.column('Fornecedor', width=250, anchor=CENTER)
    tbl_fornecedores.column('Nome fantasia', width=250, anchor=CENTER)
    tbl_fornecedores.column('CPF/CNPJ', width=100, anchor=CENTER)
    buscarFornecedores()
    tbl_fornecedores.bind('<ButtonRelease>', armazenarIdFornecedor)
    

def armazenarIdFornecedor(event):
    global dados_fornecedor
    indice = tbl_fornecedores.selection()
    if indice:
        dados_fornecedor = {
            'cnpjcpf':tbl_fornecedores.item(indice)['values'][3],
            'nome':tbl_fornecedores.item(indice)['values'][2]
        }
        

def buscarFornecedores():
    res_fornecedores = connection.getFornecedores()
    global fornecedores
    fornecedores = sorted(res_fornecedores, key=lambda p:p['NOME'], reverse=True)
    for x in fornecedores:
        id = x['PK_CADASTRO']
        nome = x['NOME']
        fantasia = x['FANTASIA']
        cpf_cnpj = f"{x['CNPJCPF']}\x00"
        data = (id, nome, fantasia, cpf_cnpj)
        tbl_fornecedores.insert(parent='', index=0, values=data) 
    
 


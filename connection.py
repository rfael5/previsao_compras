from sqlalchemy import create_engine
import pandas as pd
import json

#Conexão banco de testes
# conexao = (
#     "mssql+pyodbc:///?odbc_connect=" + 
#     "DRIVER={ODBC Driver 17 for SQL Server};" +
#     "SERVER=192.168.1.137;" +
#     "DATABASE=SOUTTOMAYOR;" +
#     "UID=Sa;" +
#     "PWD=P@ssw0rd2023"
# )

#Conexão no banco principal
conexao = (
    "mssql+pyodbc:///?odbc_connect=" + 
    "DRIVER={ODBC Driver 17 for SQL Server};" +
    "SERVER=192.168.1.43;" +
    "DATABASE=SOUTTOMAYOR;" +
    "UID=Sa;" +
    "PWD=P@ssw0rd2023@#$"
)

engine = create_engine(conexao, pool_pre_ping=True)

#Executa a query e armazena os dados em uma variável
#Retorna os dados convertidos para json
def receberDados(query):
    response = pd.read_sql_query(query, engine)
    resultadosJson = response.to_json(orient='records')
    dadosDesserializados = json.loads(resultadosJson)
    return dadosDesserializados

#Query que busca os produtos usados na composição das receitas
def getProdutosComposicao(dataInicio, dataFim):
    queryProdutosComposicao =  f"""
    select 
        e.PK_DOCTOPED as idEvento, e.NOME as nomeEvento, e.DOCUMENTO as documento, c.IDX_NEGOCIO as negocio, e.DTEVENTO as dataEvento, 
        e.DTPREVISAO as dataPrevisao, e.DATA as dataPedido, p.PK_MOVTOPED as idMovtoped, ca.IDX_LINHA as linha, p.DESCRICAO as nomeProdutoAcabado, 
        ca.RENDIMENTO as rendimento, p.UNIDADE as unidadeAcabado, a.RDX_PRODUTO as idProdutoAcabado, c.DESCRICAO as nomeProdutoComposicao, 
        c.IDX_LINHA as classificacao, c.IDX_CLASSIFICACAO, c.PK_PRODUTO as idProdutoComposicao, a.QUANTIDADE as qtdProdutoComposicao, 
        a.UN as unidadeComposicao, p.L_QUANTIDADE as qtdProdutoEvento, c.PCCUSTO as precoUltimaCompra, a.DTINC
    from TPAPRODCOMPOSICAO as a 
        inner join TPAPRODUTO as c on a.IDX_PRODUTO = c.PK_PRODUTO
        inner join TPAMOVTOPED as p on a.RDX_PRODUTO = p.IDX_PRODUTO
        inner join TPADOCTOPED as e on p.RDX_DOCTOPED = e.PK_DOCTOPED
        inner join TPAPRODUTO as ca on p.IDX_PRODUTO = ca.PK_PRODUTO
    where e.TPDOCTO = 'EC' 
        and e.DTPREVISAO between '{dataInicio}' and '{dataFim}'
        and e.SITUACAO = 'Z'
        and c.OPSUPRIMENTOMP = 'S'
    or e.TPDOCTO = 'EC' 
        and e.DTPREVISAO between '{dataInicio}' and '{dataFim}'
        and e.SITUACAO = 'B'
        and c.OPSUPRIMENTOMP = 'S'
    or e.TPDOCTO = 'OR' 
        and e.DTEVENTO between '{dataInicio}' and '{dataFim}'
        and e.SITUACAO = 'V'
        and c.OPSUPRIMENTOMP = 'S'
    or e.TPDOCTO = 'OR' 
        and e.DTEVENTO between '{dataInicio}' and '{dataFim}'
        and e.SITUACAO = 'B'
        and c.OPSUPRIMENTOMP = 'S'
    order by p.DESCRICAO
    """
    produtosComposicao = receberDados(queryProdutosComposicao)

    return produtosComposicao

#Query que busca os produtos usados na composição dos semi-acabados, que são
#massas e recheios que vão nas receitas prontas, e que também tem que ser 
#requisitados no estoque.
def getCompSemiAcabados(dataInicio, dataFim):
    queryComposicao = f"""
    SELECT 
    C.IDX_PRODUTO as idProduto, 
    P.DESCRICAO as nomeProdutoComposicao,
    P.IDX_NEGOCIO as negocio,
    P.PCCUSTO as precoUltimaCompra, 
    C.UN as unidadeProdutoComposicao, 
    C.QUANTIDADE as qtdProdutoComposicao, 
    P.IDX_LINHA as classificacao,
    P.IDX_CLASSIFICACAO, 
    P2.PK_PRODUTO as idProdutoAcabado, 
    P2.DESCRICAO as nomeProdutoAcabado, 
    P2.RENDIMENTO1 AS rendimento, 
    P.OPSUPRIMENTOMP,
    C.DTINC
FROM 
    TPAPRODCOMPOSICAO AS C
    INNER JOIN TPAPRODUTO AS P ON C.IDX_PRODUTO = P.PK_PRODUTO
    INNER JOIN TPAPRODUTO AS P2 ON C.RDX_PRODUTO = P2.PK_PRODUTO
WHERE 
    C.RDX_PRODUTO IN  (
        SELECT 
            DISTINCT c.PK_PRODUTO
        FROM 
            TPAPRODCOMPOSICAO as a
            INNER JOIN TPAPRODUTO as c ON a.IDX_PRODUTO = c.PK_PRODUTO
            INNER JOIN TPAMOVTOPED as p ON a.RDX_PRODUTO = p.IDX_PRODUTO
            INNER JOIN TPADOCTOPED as e ON p.RDX_DOCTOPED = e.PK_DOCTOPED
            INNER JOIN TPAPRODUTO as ca ON p.IDX_PRODUTO = ca.PK_PRODUTO
        WHERE 
            e.DTPREVISAO BETWEEN '{dataInicio}' AND '{dataFim}'
            AND e.SITUACAO IN ('Z', 'B', 'V') -- Verifica se SITUACAO está em um conjunto de valores
            AND c.OPSUPRIMENTOMP = 'S'
            AND (e.TPDOCTO = 'EC' OR e.TPDOCTO = 'OR') -- Verifica se TPDOCTO é 'EC' ou 'OR'
    )
    AND P.OPSUPRIMENTOMP = 'S'
ORDER BY 
    P.DESCRICAO;
    """
    composicaoSemiAcabados = receberDados(queryComposicao)
    return composicaoSemiAcabados
    
#Query que busca ajustes feitos nos pedidos, aumentos ou diminuições solicitada
#pelo cliente.
def getAjustes(dataInicio, dataFim):
    queryAjustes = f"""
    select A.IDX_MOVTOPED AS idMovtoped, V.IDX_PRODUTO AS idProduto, V.DESCRICAO AS nomeProduto, A.QUANTIDADE AS ajuste, A.PRECO AS precoAjuste from TPAAJUSTEPEDITEM AS A 
        inner join TPAMOVTOPED AS V ON A.IDX_MOVTOPED = V.PK_MOVTOPED
        inner join TPADOCTOPED AS E ON V.RDX_DOCTOPED = E.PK_DOCTOPED
        inner join TPAPRODUTO AS P ON V.IDX_PRODUTO = P.PK_PRODUTO
    where e.TPDOCTO = 'EC' 
        and E.DTPREVISAO between '{dataInicio}' and '{dataFim}'
        and E.SITUACAO = 'Z'
        and P.OPSUPRIMENTOMP = 'S'
    or e.TPDOCTO = 'EC' 
        and E.DTPREVISAO between '{dataInicio}' and '{dataFim}'
        and E.SITUACAO = 'B'
        and P.OPSUPRIMENTOMP = 'S'
    or e.TPDOCTO = 'OR' 
        and E.DTPREVISAO between '{dataInicio}' and '{dataFim}'
        and E.SITUACAO = 'V'
        and P.OPSUPRIMENTOMP = 'S'
    or e.TPDOCTO = 'OR' 
        and E.DTPREVISAO between '{dataInicio}' and '{dataFim}'
        and E.SITUACAO = 'B'
        and P.OPSUPRIMENTOMP = 'S'
    ORDER BY V.DESCRICAO
    """
    ajustes = receberDados(queryAjustes)
    return ajustes

#Query que busca o saldo de estoque do produto.
def getEstoque():
    queryEstoque = """
    WITH RankedResults AS (
        SELECT 
            E.RDX_PRODUTO,
            E.SALDOESTOQUE,
            E.DTULTCPA,
            P.DESCRICAO,
            P.UN,
            ROW_NUMBER() OVER (PARTITION BY RDX_PRODUTO ORDER BY DTULTCPA DESC) AS Rank
        FROM TPAESTOQUE AS E INNER JOIN TPAPRODUTO AS P ON E.RDX_PRODUTO = P.PK_PRODUTO 
        WHERE E.DTULTCPA IS NOT NULL
    )
    SELECT
        RDX_PRODUTO,
        SALDOESTOQUE,
        DTULTCPA,
        DESCRICAO,
        UN
    FROM RankedResults
    WHERE Rank = 1
    ORDER BY RDX_PRODUTO
    """
    estoque = receberDados(queryEstoque)
    return estoque


def getFornecedores():
    query = """
        SELECT PK_CADASTRO, CODCADASTRO, NOME, FANTASIA, CNPJCPF FROM TPACADASTRO WHERE FORNECEDOR = 'S'
    """
    
    fornecedores = receberDados(query)
    return fornecedores

def getProdutosFornecedor(cnpj_cpf):
    query = f"""
        SELECT P.CODPRODUTO AS codProduto, 
            M.DESCRICAO AS nomeProduto, 
            M.DATA AS dataCompra, 
            M.L_PRECOUNI AS precoUnitario,
            queryMax.ultimaCompra,
            queryMax.ultimoPreco,
            queryMax.ultimoFornecedor
        FROM TPADOCTOEST AS D 
        INNER JOIN TPAMOVTOEST AS M ON D.PK_DOCTOEST = M.RDX_DOCTOEST
        INNER JOIN TPAPRODUTO AS P ON M.IDX_PRODUTO = P.PK_PRODUTO
        INNER JOIN (
            SELECT IDX_PRODUTO, MAX(D.DATA) AS maxData FROM TPAMOVTOEST AS M
                INNER JOIN TPADOCTOEST AS D ON M.RDX_DOCTOEST = D.PK_DOCTOEST
                WHERE D.CNPJCPF = '{cnpj_cpf}' AND D.TPENTIDADE = 'F'
            GROUP BY IDX_PRODUTO
        ) AS subquery ON M.IDX_PRODUTO = subquery.IDX_PRODUTO AND M.DATA = subquery.maxData
        INNER JOIN (
            SELECT T1.IDX_PRODUTO, T1.DATA AS ultimaCompra, T1.L_PRECOUNI AS ultimoPreco, D.NOME as ultimoFornecedor
                FROM TPAMOVTOEST T1 JOIN(
                    SELECT IDX_PRODUTO, MAX(DATA) AS maiorData FROM TPAMOVTOEST
                        WHERE OPERACAO = 'CP'
                        GROUP BY IDX_PRODUTO
                ) T2 ON T1.IDX_PRODUTO = T2.IDX_PRODUTO AND T1.DATA = T2.maiorData
            INNER JOIN TPADOCTOEST AS D ON T1.RDX_DOCTOEST = D.PK_DOCTOEST
        ) AS queryMax ON M.IDX_PRODUTO = queryMax.IDX_PRODUTO
        WHERE D.CNPJCPF = '{cnpj_cpf}' AND D.TPENTIDADE = 'F'
        ORDER BY M.DESCRICAO
    """ 
    
    produtos = receberDados(query)
    return produtos
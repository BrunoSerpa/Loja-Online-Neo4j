from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from Programa.conexaoBanco.configuracao import configuracao, tabelas, indices
from Programa.funcoes.utils.salvarErro import salvarErro

def conectar():
    try:
        configNuvem, idCliente, segredoCliente = configuracao()
        provedorAutenticacao = PlainTextAuthProvider(idCliente, segredoCliente)
        cluster = Cluster(cloud=configNuvem, auth_provider=provedorAutenticacao)
        sessao = cluster.connect()
        sessao.execute("USE loja_online;")
        # for query in tabelas():
        #     try:
        #         sessao.execute(query)
        #         print(f"Comando executado com sucesso: {query}")
        #     except Exception as e:
        #         salvarErro("Erro ao criar tabela", e)
        # for query in indices():
        #     try:
        #         sessao.execute(query)
        #         print(f"Comando executado com sucesso: {query}")
        #     except Exception as e:
        #         salvarErro("Erro ao criar índice", e)
        return sessao
    except Exception as e:
        salvarErro("Erro ao conectar ao Cassandra", e)
        return None
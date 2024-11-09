from neo4j import GraphDatabase

from Programa.conexaoBanco.credenciais import uri, user, password
from Programa.funcoes.utils.salvarErro import salvarErro

def conectar():
    try:
        driver = GraphDatabase.driver(uri, auth = (user, password))
        return driver.session()
    except Exception as e:
        salvarErro("Erro ao conectar ao Cassandra", e)
        return None
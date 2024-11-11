from Programa.conexaoBanco.conectar import conectar
from Programa.funcoes.utils.salvarErro import salvarErro

from uuid import uuid4

driver, sessao = conectar()

def escolherLabel(nome):
    if sessao is None:
        salvarErro("Erro na sessão", "Sessão de banco de dados não estabelecida")
        return None

    labels = {
        'Usuarios': 'Usuario',
        'Vendedores': 'Vendedor',
        'Produtos': 'Produto',
        'Compras': 'Compra',
        'Enderecos': 'Endereco'
    }
    return labels.get(nome)

def cadastrar(nomeLabel, dados):
    label = escolherLabel(nomeLabel)
    if label is None:
        return None
    try:
        id = str(uuid4())
        dados['id'] = id

        propriedades = ', '.join(f"{k}: ${k}" for k in dados.keys())

        query = f"CREATE (n:{label} {{{propriedades}}})"
        sessao.run(query, dados)
        for key, value in dados.items():
            if isinstance(value, str) and key in ["id_vendedor", "remetente", "destinatario", "id_cliente"]:
                vincularRelacao(id, key, value, label)
        return id

    except Exception as e:
        salvarErro(f"Erro ao cadastrar em {nomeLabel}", e)
        return None

def atualizar(nomeLabel, dados):
    label = escolherLabel(nomeLabel)
    if label == None:
        return None
    try:
        id = dados.pop('id', None)
        if not id:
            salvarErro(f"Erro ao atualizar {nomeLabel}", "ID não fornecido")
            return None

        updates = ', '.join(f"n.{k} = ${k}" for k in dados.keys())
        query = f"MATCH (n:{label} {{id: '{id}'}}) SET {updates}"
        sessao.run(query, dados)

        for key, value in dados.items():
            if isinstance(value, list):
                vincularRelacao(id, key, value, label)
        dados['id'] = id
        return id

    except Exception as e:
        salvarErro(f"Erro ao atualizar {nomeLabel}", e)
        return None


def excluir(nomeLabel, id):
    label = escolherLabel(nomeLabel)
    if label == None:
        return None
    try:
        query = f"MATCH (n:{label} {{id: $id}})-[r]-() DELETE r"
        sessao.run(query, {"id": id})
    except Exception as e:
        salvarErro(f"Erro ao excluir relacionamentos {nomeLabel}", e)
        return None
    try:
        query = f"MATCH (n:{label} {{id: $id}}) DELETE n"
        sessao.run(query, {"id": id})
        return id
    except Exception as e:
        salvarErro(f"Erro ao excluir em {nomeLabel}", e)
        return None

def buscarTodos(nomeLabel):
    label = escolherLabel(nomeLabel)
    if label == None:
        return None
    try:
        query = f"MATCH (n:{label}) RETURN n"
        resultados = sessao.run(query)
        return [dict(record['n']) for record in resultados]
    except Exception as e:
        salvarErro("Erro ao buscar todos os registros", e)
    return None

def buscarPorId(nomeLabel, id):
    label = escolherLabel(nomeLabel)
    if label == None:
        return None
    try:
        query = f"MATCH (n:{label} {{id: $id}}) RETURN n"
        resultado = sessao.run(query, {"id": id}).single()
        if resultado:
            return dict(resultado['n'])
        else:
            salvarErro("Registro não encontrado", f'ID {id} não encontrado na label {nomeLabel}')
            return None
    except Exception as e:
        salvarErro("Erro ao buscar registro por ID", e)
        return None

def buscarPorAtributo(nomeLabel, nomeCampo, atributo):
    label = escolherLabel(nomeLabel)
    if label == None:
        return None
    try:
        query = f"MATCH (n:{label}) WHERE n.{nomeCampo} = $atributo RETURN n"
        resultados = sessao.run(query, {'atributo': atributo})
        return [dict(record['n']) for record in resultados]
    except Exception as e:
        salvarErro("Erro ao buscar registro por atributo semelhante", e)
        return None

def vincularRelacao(id, campo, item_id, label):
    relacoes = {
        "enderecos": "TEM_ENDERECO",
        "favoritos": "FAVORITOU",
        "compras": "FEZ_COMPRA",
        "vendas": "REALIZA_VENDA",
        "produtos": "TEM_PRODUTO",
        "id_vendedor": "VENDIDO_POR",
        "remetente": "ENVIADO_POR",
        "destinatario": "ENVIADO_A",
        "id_cliente": "COMPRADO_POR"
    }

    if campo in relacoes:
        relacao = relacoes[campo]
        try:
            if isinstance(item_id, list):
                for id_item in item_id:
                    query = f"MATCH (u:{label} {{id: $id}}), (e {{id: $item_id}}) MERGE (u)-[:{relacao}]->(e)"
                    sessao.run(query, {"id": id, "item_id": id_item})
            else:
                query = f"MATCH (u:{label} {{id: $id}}), (e {{id: $item_id}}) MERGE (u)-[:{relacao}]->(e)"
                sessao.run(query, {"id": id, "item_id": item_id})
        except Exception as e:
            salvarErro(f"Erro ao criar a relação {relacao}", e)
            return False

def fecharConexao():
    try:
        if sessao:
            sessao.close()
        if driver:
            driver.close()
        print("Conexão com o Neo4j encerrada com sucesso.")
    except Exception as e:
        salvarErro("Erro ao encerrar conexão com o Neo4j", e)

def rowParaDict(row, colecao):
    def corrigindoSet(s):
        return set(s) if s is not None else set()

    if colecao == 'usuarios':
        return {
            'id': row.id,
            'nome_usuario': row.nome_usuario,
            'cpf': row.cpf,
            'email_usuario': row.email_usuario,
            'telefone_usuario': row.telefone_usuario,
            'enderecos': corrigindoSet(row.enderecos),
            'favoritos': corrigindoSet(row.favoritos),
            'compras': corrigindoSet(row.compras)
        }
    elif colecao == 'vendedores':
        return {
            'id': row.id,
            'nome_vendedor': row.nome_vendedor,
            'cnpj': row.cnpj,
            'email_vendedor': row.email_vendedor,
            'telefone_vendedor': row.telefone_vendedor,
            'enderecos': corrigindoSet(row.enderecos),
            'produtos': corrigindoSet(row.produtos),
            'vendas': corrigindoSet(row.vendas)
        }
    elif colecao == 'produtos':
        return {
            'id': row.id,
            'nome_produto': row.nome_produto,
            'valor_produto': row.valor_produto,
            'id_vendedor': row.id_vendedor
        }
    elif colecao == 'compras':
        return {
            'id': row.id,
            'data_compra': row.data_compra,
            'id_cliente': row.id_cliente,
            'destinatario': row.destinatario,
            'id_vendedor': row.id_vendedor,
            'remetente': row.remetente,
            'produtos': corrigindoSet(row.produtos),
            'valor_total': row.valor_total
        }
    else:
        return {
            'id': row.id,
            'rua': row.rua,
            'numero': row.numero,
            'descricao': row.descricao,
            'bairro': row.bairro,
            'cidade': row.cidade,
            'estado': row.estado,
            'pais': row.pais,
            'cep': row.cep
        }
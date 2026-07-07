from model.cidade_favorita import CidadeFavorita

class FavoritoController:
    def __init__(self, favorita_dao):
        self.favorita_dao = favorita_dao

    def adicionar(self, cidade, apelido):
        if not cidade or not apelido:
            raise ValueError("Cidade e apelido são obrigatórios.")
        favorita = CidadeFavorita(cidade=cidade.strip(), apelido=apelido.strip())
        return self.favorita_dao.salvar(favorita)

    def listar(self):
        return self.favorita_dao.listar_todas()

    def atualizar(self, favorita_id, cidade, apelido):
        if not cidade or not apelido:
            raise ValueError("Cidade e apelido são obrigatórios.")
        return self.favorita_dao.atualizar(favorita_id, cidade.strip(), apelido.strip())

    def excluir(self, favorita_id):
        return self.favorita_dao.deletar_por_id(favorita_id)

from model.cidade_favorita import CidadeFavorita

class CidadeFavoritaDAO:
    def __init__(self, session):
        self.session = session

    def salvar(self, favorita):
        self.session.add(favorita)
        self.session.commit()
        self.session.refresh(favorita)
        return favorita

    def listar_todas(self):
        return self.session.query(CidadeFavorita).order_by(CidadeFavorita.apelido.asc()).all()

    def buscar_por_id(self, favorita_id):
        return self.session.query(CidadeFavorita).filter(CidadeFavorita.id == favorita_id).first()

    def atualizar(self, favorita_id, cidade, apelido):
        favorita = self.buscar_por_id(favorita_id)
        if favorita is None:
            return False
        favorita.cidade = cidade
        favorita.apelido = apelido
        self.session.commit()
        return True

    def deletar_por_id(self, favorita_id):
        favorita = self.buscar_por_id(favorita_id)
        if favorita is None:
            return False
        self.session.delete(favorita)
        self.session.commit()
        return True

from model.consulta_clima import ConsultaClima

class ConsultaClimaDAO:
    def __init__(self, session):
        self.session = session

    def salvar(self, consulta):
        self.session.add(consulta)
        self.session.commit()
        self.session.refresh(consulta)
        return consulta

    def listar_todas(self):
        return self.session.query(ConsultaClima).order_by(ConsultaClima.data_consulta.desc()).all()

    def buscar_por_cidade(self, cidade):
        return (
            self.session.query(ConsultaClima)
            .filter(ConsultaClima.cidade.ilike(f"%{cidade}%"))
            .order_by(ConsultaClima.data_consulta.desc())
            .all()
        )

    def buscar_por_id(self, consulta_id):
        return self.session.query(ConsultaClima).filter(ConsultaClima.id == consulta_id).first()

    def atualizar_observacao(self, consulta_id, nova_observacao):
        consulta = self.buscar_por_id(consulta_id)
        if consulta is None:
            return False
        consulta.observacao = nova_observacao
        self.session.commit()
        return True

    def deletar_por_id(self, consulta_id):
        consulta = self.buscar_por_id(consulta_id)
        if consulta is None:
            return False
        self.session.delete(consulta)
        self.session.commit()
        return True

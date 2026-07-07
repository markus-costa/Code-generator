from model.consulta_clima import ConsultaClima

class ClimaController:
    def __init__(self, openweather_client, consulta_dao):
        self.openweather_client = openweather_client
        self.consulta_dao = consulta_dao

    def consultar_e_salvar(self, cidade):
        if not cidade or cidade.strip() == "":
            raise ValueError("Digite uma cidade.")

        dados = self.openweather_client.consultar_clima(cidade.strip())
        consulta = ConsultaClima(
            cidade=dados.get("name", cidade.strip()),
            pais=dados.get("sys", {}).get("country", ""),
            descricao=dados["weather"][0]["description"].capitalize(),
            temperatura=dados["main"]["temp"],
            temp_min=dados["main"].get("temp_min"),
            temp_max=dados["main"].get("temp_max"),
            sensacao_termica=dados["main"].get("feels_like"),
            umidade=dados["main"].get("humidity"),
            pressao=dados["main"].get("pressure"),
            velocidade_vento=dados.get("wind", {}).get("speed")
        )
        return self.consulta_dao.salvar(consulta)

    def listar_historico(self):
        return self.consulta_dao.listar_todas()

    def buscar_por_cidade(self, cidade):
        if not cidade or cidade.strip() == "":
            return self.listar_historico()
        return self.consulta_dao.buscar_por_cidade(cidade.strip())

    def atualizar_observacao(self, consulta_id, observacao):
        return self.consulta_dao.atualizar_observacao(consulta_id, observacao)

    def excluir_consulta(self, consulta_id):
        return self.consulta_dao.deletar_por_id(consulta_id)

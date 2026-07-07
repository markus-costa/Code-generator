class AssistenteController:
    def __init__(self, clima_controller, chatgpt_client):
        self.clima_controller = clima_controller
        self.chatgpt_client = chatgpt_client

    def perguntar(self, pergunta, cidade):
        if not pergunta or pergunta.strip() == "":
            raise ValueError("Digite uma pergunta para a assistente.")
        consulta = self.clima_controller.consultar_e_salvar(cidade)
        resposta = self.chatgpt_client.gerar_resposta_climatica(pergunta, consulta)
        return consulta, resposta

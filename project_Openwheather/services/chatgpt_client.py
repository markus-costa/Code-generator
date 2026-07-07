import requests

class ChatGPTClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/responses"

    def gerar_resposta_climatica(self, pergunta, consulta):
        print("CHAVE OPENAI:", self.api_key)
        if not self.api_key:
            return "Erro: a chave OPENAI_API_KEY não foi carregada."

        prompt = f"""
Você é uma assistente climática. Responda em português, de forma curta, clara e útil.
Pergunta do usuário: {pergunta}
Dados reais do clima:
Cidade: {consulta.cidade}
Descrição: {consulta.descricao}
Temperatura: {consulta.temperatura}°C
Sensação térmica: {consulta.sensacao_termica}°C
Mínima: {consulta.temp_min}°C
Máxima: {consulta.temp_max}°C
Umidade: {consulta.umidade}%
Pressão: {consulta.pressao} hPa
Vento: {consulta.velocidade_vento} m/s
"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4.1-mini",
            "input": prompt
        }
        resposta = requests.post(self.url, headers=headers, json=payload, timeout=20)
        if resposta.status_code != 200:
            return f"Erro OpenAI {resposta.status_code}: {resposta.text}"

        dados = resposta.json()
        return dados.get("output_text", f"Resposta sem output_text: {dados}")

    def _resposta_local(self, pergunta, consulta):
        temp = consulta.temperatura
        if temp <= 15:
            dica = "Leve casaco, porque a temperatura está baixa."
        elif temp <= 24:
            dica = "O clima está agradável, mas vale levar uma blusa leve."
        else:
            dica = "Está quente, então use roupas leves e se hidrate bem."
        return (
            f"Em {consulta.cidade}, agora está {temp:.1f}°C, com sensação de "
            f"{consulta.sensacao_termica:.1f}°C e clima {consulta.descricao}. {dica}"
        )

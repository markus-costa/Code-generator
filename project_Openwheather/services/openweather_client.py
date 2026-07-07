import requests

class OpenWeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openweathermap.org/data/2.5/weather"

    def consultar_clima(self, cidade):
        if not self.api_key:
            raise ValueError("Configure a chave OPENWEATHER_API_KEY no arquivo .env")

        parametros = {
            "q": cidade,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br"
        }
        resposta = requests.get(self.url, params=parametros, timeout=10)

        if resposta.status_code == 404:
            raise ValueError("Cidade não encontrada. Tente digitar cidade, estado ou país.")
        if resposta.status_code == 401:
            raise ValueError("Chave da OpenWeather inválida ou ainda não ativada.")
        if resposta.status_code != 200:
            raise Exception(f"Erro ao consultar OpenWeather: {resposta.status_code}")

        return resposta.json()

import os

from database.connection import DatabaseManager
from model.consulta_clima import ConsultaClima
from model.cidade_favorita import CidadeFavorita
from dao.consulta_clima_dao import ConsultaClimaDAO
from dao.cidade_favorita_dao import CidadeFavoritaDAO
from services.openweather_client import OpenWeatherClient
from services.chatgpt_client import ChatGPTClient
from controller.clima_controller import ClimaController
from controller.favorito_controller import FavoritoController
from controller.assistente_controller import AssistenteController
from view.tela_clima import TelaClima


def main():
    db = DatabaseManager()
    db.criar_tabelas()
    session = db.criar_sessao()

    openweather_client = OpenWeatherClient(os.getenv("OPENWEATHER_API_KEY"))
    chatgpt_client = ChatGPTClient(os.getenv("OPENAI_API_KEY"))

    consulta_dao = ConsultaClimaDAO(session)
    favorita_dao = CidadeFavoritaDAO(session)

    clima_controller = ClimaController(openweather_client, consulta_dao)
    favorito_controller = FavoritoController(favorita_dao)
    assistente_controller = AssistenteController(clima_controller, chatgpt_client)

    tela = TelaClima(clima_controller, favorito_controller, assistente_controller)
    tela.iniciar()

if __name__ == "__main__":
    main()

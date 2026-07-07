import PySimpleGUI as sg

class TelaClima:
    def __init__(self, clima_controller, favorito_controller, assistente_controller):
        self.clima_controller = clima_controller
        self.favorito_controller = favorito_controller
        self.assistente_controller = assistente_controller
        self.consulta_atual = None
        sg.theme("DarkBlue14")

    def _card_clima(self):
        return [
            [sg.Text("Sistema Climático", font=("Arial", 22, "bold"), key="-TITULO-")],
            [sg.Text("Digite uma cidade", font=("Arial", 11)), sg.Input(key="-CIDADE-", size=(28, 1)), sg.Button("Buscar clima", key="-BUSCAR-")],
            [sg.HorizontalSeparator()],
            [sg.Text("--", font=("Arial", 20, "bold"), key="-LOCAL-")],
            [sg.Text("--°", font=("Arial", 72), key="-TEMP-")],
            [sg.Text("Clima: --", font=("Arial", 14), key="-DESC-")],
            [sg.Text("Mínima/Máxima: --", font=("Arial", 12), key="-MINMAX-")],
            [sg.Frame("Detalhes", [
                [sg.Text("Sensação térmica:", size=(18,1)), sg.Text("--", key="-SENSACAO-")],
                [sg.Text("Pressão:", size=(18,1)), sg.Text("--", key="-PRESSAO-")],
                [sg.Text("Umidade:", size=(18,1)), sg.Text("--", key="-UMIDADE-")],
                [sg.Text("Vento:", size=(18,1)), sg.Text("--", key="-VENTO-")],
                [sg.Text("Data e hora:", size=(18,1)), sg.Text("--", key="-DATA-")],
            ], expand_x=True)],
            [sg.Button("Adicionar favorito", key="-ADD_FAV-"), sg.Button("Histórico", key="-HIST-"), sg.Button("Favoritos", key="-FAV-"), sg.Button("Sair")]
        ]

    def _painel_assistente(self):
        return [
            [sg.Text("Assistente virtual", font=("Arial", 16, "bold"))],
            [sg.Text("Pergunte algo sobre o clima da cidade pesquisada:")],
            [sg.Multiline(default_text="Ex: Preciso levar casaco? Dá pra correr hoje?",key="-PERGUNTA-",size=(45,4))],
            [sg.Button("Perguntar", key="-PERGUNTAR-")],
            [sg.Multiline(key="-RESPOSTA-", size=(45, 12), disabled=True)]
        ]

    def iniciar(self):
        layout = [
            [sg.Column(self._card_clima(), size=(500, 650), element_justification="left"),
             sg.VSeparator(),
             sg.Column(self._painel_assistente(), size=(420, 650))]
        ]
        janela = sg.Window("Clima Inteligente - OpenWeather", layout, finalize=True, resizable=True)

        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "Sair"):
                break
            try:
                if evento == "-BUSCAR-":
                    consulta = self.clima_controller.consultar_e_salvar(valores["-CIDADE-"])
                    self.consulta_atual = consulta
                    self._atualizar_tela(janela, consulta)
                    sg.popup("Consulta salva com sucesso!")

                elif evento == "-PERGUNTAR-":
                    cidade = valores["-CIDADE-"]
                    consulta, resposta = self.assistente_controller.perguntar(valores["-PERGUNTA-"], cidade)
                    self.consulta_atual = consulta
                    self._atualizar_tela(janela, consulta)
                    janela["-RESPOSTA-"].update(resposta)

                elif evento == "-HIST-":
                    self._abrir_historico()

                elif evento == "-FAV-":
                    self._abrir_favoritos(janela)

                elif evento == "-ADD_FAV-":
                    self._adicionar_favorito(valores.get("-CIDADE-", ""))

            except Exception as erro:
                sg.popup_error("Erro", str(erro))
        janela.close()

    def _atualizar_tela(self, janela, c):
        d = c.to_dict()
        janela["-LOCAL-"].update(f"{d['cidade']} {d['pais']}")
        janela["-TEMP-"].update(f"{d['temperatura']:.0f}°")
        janela["-DESC-"].update(f"Clima: {d['descricao']}")
        janela["-MINMAX-"].update(f"Mínima/Máxima: {d['temp_min']:.0f}° / {d['temp_max']:.0f}°")
        janela["-SENSACAO-"].update(f"{d['sensacao_termica']:.1f}°C")
        janela["-PRESSAO-"].update(f"{d['pressao']} hPa")
        janela["-UMIDADE-"].update(f"{d['umidade']}%")
        janela["-VENTO-"].update(f"{d['velocidade_vento']} m/s")
        janela["-DATA-"].update(d["data_consulta"])

    def _abrir_historico(self):
        historico = self.clima_controller.listar_historico()
        dados = [[c.id, c.cidade, f"{c.temperatura:.1f}°C", c.descricao, c.data_consulta.strftime("%d/%m/%Y %H:%M"), c.observacao or ""] for c in historico]
        layout = [
            [sg.Text("Histórico de consultas", font=("Arial", 16, "bold"))],
            [sg.Table(dados, headings=["ID", "Cidade", "Temp.", "Clima", "Data", "Observação"], key="-TABELA-", enable_events=True, auto_size_columns=True, num_rows=12)],
            [sg.Text("ID:"), sg.Input(key="-ID-", size=(6,1)), sg.Text("Observação:"), sg.Input(key="-OBS-", size=(35,1))],
            [sg.Button("Atualizar observação", key="-ATUALIZAR-"), sg.Button("Excluir", key="-EXCLUIR-"), sg.Button("Fechar")]
        ]
        janela = sg.Window("Histórico", layout, modal=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "Fechar"):
                break
            try:
                if evento == "-ATUALIZAR-":
                    ok = self.clima_controller.atualizar_observacao(int(valores["-ID-"]), valores["-OBS-"])
                    sg.popup("Atualizado!" if ok else "ID não encontrado.")
                    break
                if evento == "-EXCLUIR-":
                    ok = self.clima_controller.excluir_consulta(int(valores["-ID-"]))
                    sg.popup("Excluído!" if ok else "ID não encontrado.")
                    break
            except Exception as erro:
                sg.popup_error("Erro", str(erro))
        janela.close()

    def _adicionar_favorito(self, cidade):
        if not cidade:
            sg.popup("Digite uma cidade primeiro.")
            return
        apelido = sg.popup_get_text("Digite um apelido para essa cidade:", default_text=cidade)
        if apelido:
            self.favorito_controller.adicionar(cidade, apelido)
            sg.popup("Favorito salvo!")

    def _abrir_favoritos(self, janela_principal):
        favoritas = self.favorito_controller.listar()
        dados = [[f.id, f.apelido, f.cidade] for f in favoritas]
        layout = [
            [sg.Text("Cidades favoritas", font=("Arial", 16, "bold"))],
            [sg.Table(dados, headings=["ID", "Apelido", "Cidade"], key="-TABELA_FAV-", auto_size_columns=True, num_rows=10)],
            [sg.Text("ID:"), sg.Input(key="-ID-", size=(6,1)), sg.Text("Cidade:"), sg.Input(key="-CIDADE_FAV-", size=(18,1)), sg.Text("Apelido:"), sg.Input(key="-APELIDO-", size=(18,1))],
            [sg.Button("Buscar clima", key="-BUSCAR_FAV-"), sg.Button("Atualizar favorito", key="-ATUALIZAR_FAV-"), sg.Button("Excluir favorito", key="-EXCLUIR_FAV-"), sg.Button("Fechar")]
        ]
        janela = sg.Window("Favoritos", layout, modal=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "Fechar"):
                break
            try:
                if evento == "-BUSCAR_FAV-":
                    cidade = valores["-CIDADE_FAV-"]
                    consulta = self.clima_controller.consultar_e_salvar(cidade)
                    self.consulta_atual = consulta
                    janela_principal["-CIDADE-"].update(cidade)
                    self._atualizar_tela(janela_principal, consulta)
                    sg.popup("Consulta salva com sucesso!")
                    break
                if evento == "-ATUALIZAR_FAV-":
                    ok = self.favorito_controller.atualizar(int(valores["-ID-"]), valores["-CIDADE_FAV-"], valores["-APELIDO-"])
                    sg.popup("Favorito atualizado!" if ok else "ID não encontrado.")
                    break
                if evento == "-EXCLUIR_FAV-":
                    ok = self.favorito_controller.excluir(int(valores["-ID-"]))
                    sg.popup("Favorito excluído!" if ok else "ID não encontrado.")
                    break
            except Exception as erro:
                sg.popup_error("Erro", str(erro))
        janela.close()

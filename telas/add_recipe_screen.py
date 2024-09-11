from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivymd.app import MDApp  # Importando o MDApp para acessar o app principal
from database import adicionar_receita  # arquivo database.py

class AddRecipeScreen(MDScreen):
    # Propriedades do formulário de adicionar receita
    receita_titulo = ObjectProperty(None)
    receita_descricao = ObjectProperty(None)
    receita_ingredientes = ObjectProperty(None)
    receita_steps = ObjectProperty(None)

    def salvar_receita(self):
        # Obtém a instância do aplicativo em execução
        app = MDApp.get_running_app()

        # Obtém os valores dos campos do formulário
        titulo = self.receita_titulo.text
        descricao = self.receita_descricao.text
        ingredientes = self.receita_ingredientes.text
        instrucoes = self.receita_instrucoes.text
        id_usuario = app.pegar_usuario_atual()  # Obtém o ID do usuário logado

        # Verifica se todos os campos foram preenchidos
        if titulo and ingredientes and instrucoes:
            # Adiciona a receita ao banco de dados
            adicionar_receita(titulo, descricao, ingredientes, instrucoes, id_usuario)
            # Voltar ao menu principal
            self.manager.current = 'menu'
        else:
            # Mostra um diálogo de erro se algum campo estiver vazio
            app.alerta_dialogo("Erro", "Por favor, preencha todos os campos.")
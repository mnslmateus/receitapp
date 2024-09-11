from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
from kivy.properties import ObjectProperty
from database import get_receitas_recentes
from kivymd.app import MDApp

class MenuScreen(MDScreen):
    # Propriedades do formulário de menu
    recipe_list = ObjectProperty(None)
    search_field = ObjectProperty(None)
    search_box = ObjectProperty(None)

    def on_enter(self, *args):
        # Carrega as receitas recentes quando a tela é aberta
        self.carregar_receitas_recentes()

    def carregar_receitas_recentes(self):
        # Obtém as receitas recentes do banco de dados
        receitas = get_receitas_recentes()

        # Limpar widgets da lista de receitas
        self.recipe_list.clear_widgets()

        # Adicionar cada receita à lista
        for receita in receitas:
            # Cortar a descrição para 60 caracteres
            descricao = (receita[2][:60] + '...') if len(receita[2]) > 60 else receita[2]
            # Criar um item de lista para cada receita
            item = TwoLineListItem(
                text=receita[1],  # Nome da receita
                secondary_text=descricao,  # Descrição cortada
                on_release=self.criar_on_release(receita)  # Função on_release para abrir a receita correta
            )
            # Adicionar o item à lista
            self.recipe_list.add_widget(item)

    def criar_on_release(self, receita):
        # Cria um botão para cada receita que, quando clicado, mostra os detalhes daquela receita
        # Retorna uma função lambda que abre a receita correta
        return lambda x: self.visualizar_receita(receita)

    def visualizar_receita(self, receita):
        # Obtém a instância do aplicativo em execução
        app = MDApp.get_running_app()
        # Armazena a receita atual
        app.recipe = receita
        # Verifica se a tela de detalhes da receita já existe
        if not self.manager.has_screen('recipe_details'):
            # Importa a tela de detalhes, se necessário
            from telas.recipe_details_screen import RecipeDetailsScreen
            # Adiciona a tela de detalhes ao gerenciador de telas
            self.manager.add_widget(RecipeDetailsScreen(name='recipe_details'))
        # Mudar para a tela de detalhes
        self.manager.current = 'recipe_details'

    def alternar_pesquisa(self):
        # Obtém o widget de busca
        search_box = self.ids.search_box
        # Alterna a visibilidade da caixa de busca
        if search_box.opacity == 0:
            search_box.opacity = 1
            # Foca no campo de busca
            self.ids.search_field.focus = True
        else:
            # Limpa a busca
            self.limpar_pesquisa()

    def limpar_pesquisa(self):
        # Limpa o campo de busca
        self.ids.search_field.text = ""
        # Remove o foco do campo de busca
        self.ids.search_field.focus = False
        # Oculta a caixa de busca
        self.ids.search_box.opacity = 0

    def mostrar_adicionar_receita(self):
        # Mudar para a tela de adicionar receita
        self.manager.current = 'add_recipe'
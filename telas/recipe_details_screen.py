from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

class RecipeDetailsScreen(MDScreen):
    def on_pre_enter(self, *args):
        # Obtém a instância do aplicativo em execução
        app = MDApp.get_running_app()
        # Obtém a receita atual
        receita = app.recipe

        # Verifica se a receita existe
        if not receita:
            return

        # Atualiza o título da toolbar com o nome da receita
        self.ids.toolbar.title = receita[1]

        # Atualiza o campo de descrição
        # Verifica se a descrição existe e a atualiza
        self.ids.description_label.text = receita[2] if receita[2] else "Sem descrição."

        # Atualiza a lista de ingredientes
        self.atualiza_lista(self.ids.ingredients_list, receita[3])

        # Atualiza a lista de instruções
        self.atualiza_lista(self.ids.instructions_list, receita[4])

    def atualiza_lista(self, list_widget, items):
        # Divide a string de itens em uma lista
        for item in items.split('\n'):
            # Verifica se o item não é vazio
            if item.strip():  
                # Cria um item de lista para cada ingrediente ou instrução
                list_widget.add_widget(
                    OneLineListItem(text=f"• {item.strip()}")
                )
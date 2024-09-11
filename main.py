from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from database import criar_tabelas, get_usuario_logado_id, iniciar_sessao, verificar_usuario, encerrar_sessao
from telas.login_screen import LoginScreen
from telas.signup_screen import SignUpScreen
from telas.menu_screen import MenuScreen
from telas.add_recipe_screen import AddRecipeScreen
from telas.welcome_screen import WelcomeScreen
from telas.recipe_details_screen import RecipeDetailsScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import TwoLineListItem

Builder.load_file('kv/login_screen.kv')
Builder.load_file('kv/signup_screen.kv')
Builder.load_file('kv/menu_screen.kv')
Builder.load_file('kv/add_recipe_screen.kv')
Builder.load_file('kv/welcome_screen.kv')
Builder.load_file('kv/recipe_details_screen.kv')

Window.size = (360, 640)

class ReceitasApp(MDApp):
    recipe = None
    dialog = None
    dialog_login = None
    dialog_saida = None
    dialog_exclusao = None
    current_category = None

    def build(self):
        # Cria as tabelas no banco de dados
        criar_tabelas()
        # Define o tema da aplicação
        self.theme_cls.primary_palette = "Blue"

        # Cria o gerenciador de telas
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(AddRecipeScreen(name='add_recipe'))
        sm.add_widget(RecipeDetailsScreen(name='detalhes_receita'))

        return sm

    def login(self, email, password):
        # Verifica se o usuário existe e inicia a sessão
        user_id = verificar_usuario(email, password)
        if user_id:
            iniciar_sessao(user_id)
            self.root.current = 'menu'
        else:
            # Mostra um diálogo de erro se as credenciais forem inválidas
            self.dialogo_login("Erro", "Credenciais inválidas!")

    def dialogo_login(self, title, text):
        if self.dialog_login:
            self.dialog_login.dismiss()
        self.dialog_login = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="Fechar", on_release=self.close_login_dialog)]
        )
        self.dialog_login.open()

    def close_login_dialog(self, obj):
        self.dialog_login.dismiss()

    def dialogo_saida(self):
        # Mostra um diálogo para confirmar a saída
        if self.dialog_saida:
            self.dialog_saida.dismiss()
        self.dialog_saida = MDDialog(
            title="Confirmar saída",
            text="Você realmente deseja sair?",
            buttons=[
                MDFlatButton(text="Cancelar", on_release=self.fechar_dialogo_saida),
                MDFlatButton(text="Sair", on_release=self.sair)
            ]
        )
        self.dialog_saida.open()

    def fechar_dialogo_saida(self, obj):
        # Fecha o diálogo
        self.dialog_saida.dismiss()

    def sair(self, obj):
        # Finaliza a sessão e volta para a tela inicial
        user_id = get_usuario_logado_id()  # Obter o ID do usuário logado
        if user_id:
            encerrar_sessao(user_id)  # Finaliza a sessão para o usuário
            self.fechar_dialogo_saida(obj)  # Fecha o diálogo
            self.root.current = 'welcome'  # Retorna para a tela inicial
        else:
            print("Nenhum usuário logado.")

    def alerta_dialogo(self, title, text):
        if self.dialog_login:
            self.dialog_login.dismiss()
        self.dialog_login = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="Fechar", on_release=self.fechar_dialogo_alerta)]
        )
        self.dialog_login.open()

    def fechar_dialogo_alerta(self, obj):
        # Fecha o diálogo de alerta
        self.dialog_login.dismiss()

    def pesquisar_receitas(self, query):
        # Pesquisa receitas com base na consulta
        recipes = self.pesquisa_receita_bd(query)
        menu_screen = self.root.get_screen('menu')
        menu_screen.ids.recipe_list.clear_widgets()
        for recipe in recipes:
            item = TwoLineListItem(
                text=recipe[1],  # Nome da receita
                secondary_text=recipe[2][:60] + '...' if len(recipe[2]) > 60 else recipe[2],  # Descrição cortada
                on_release=self.create_on_release(recipe)  # Ação ao clicar
            )
            menu_screen.ids.recipe_list.add_widget(item)

    def create_on_release(self, recipe):
        # Cria um botão para cada receita que, quando clicado, mostra os detalhes daquela receita
        return lambda x: self.ver_receita(recipe)

    def ver_receita(self, recipe):
        # Mostra os detalhes da receita selecionada
        app = MDApp.get_running_app()
        app.recipe = recipe
        if not self.root.has_screen('recipe_details'):
            from telas.recipe_details_screen import RecipeDetailsScreen  # Importa a tela de detalhes
            self.root.add_widget(RecipeDetailsScreen(name='recipe_details'))
        self.root.current = 'recipe_details'  # Mudar para a tela de detalhes

    def conectar_db(self):
        # Conecta ao banco de dados
        import sqlite3
        return sqlite3.connect('app.db')

    def mostrar_tela_receita(self):
        # Mostra a tela de adicionar receita
        self.root.current = 'add_recipe'

    def pesquisa_receita_bd(self, query):
        # Busca receitas no banco de dados com base na consulta
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receitas WHERE titulo LIKE ?", ('%' + query + '%',))
        recipes = cursor.fetchall()
        conn.close()
        return recipes

    def voltar_para_o_menu(self):
        # Volta para a tela do menu
        self.root.current = 'menu'

    def salvar_receita(self, title, description, ingredients, steps):
        # Salva a receita no banco de dados
        if not title or not ingredients or not steps:
            self.alerta_dialogo("Erro", "Por favor, preencha todos os campos.")
            return

        # Usando a função existente `add_recipe` do database.py
        user_id = self.pegar_usuario_atual()  # Obtendo o ID do usuário logado
        add_receita(title, description, ingredients, steps, user_id)

        # Voltar para a tela do menu após salvar
        self.root.current = 'menu'

    def pegar_usuario_atual(self):
        # Obtém o ID do usuário logado
        user_id = get_usuario_logado_id()
        if user_id:
            return user_id
        else:
            return None

    def excluir_receita(self):
        # Obter a receita atual
        recipe = self.recipe

        # Verificar se a receita pertence ao usuário atual
        user_id = self.pegar_usuario_atual()
        if recipe[5] == user_id:
            # Mostrar um diálogo de confirmação
            if self.dialog_exclusao:
                self.dialog_exclusao.dismiss()
            self.dialog_exclusao = MDDialog(
                title="Confirmar exclusão",
                text="Você realmente deseja excluir essa receita?",
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=self.fechar_dialogo_exclusao),
                    MDFlatButton(text="Excluir", on_release=lambda x: self.confirmar_exclusao_receita(recipe))
                ]
            )
            self.dialog_exclusao.open()
        else:
            self.alerta_dialogo("Erro", "Você não tem permissão para excluir essa receita.")

    def confirmar_exclusao_receita(self, recipe):
        # Excluir a receita do banco de dados
        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM receitas WHERE id = ?", (recipe[0],))
        conn.commit()
        conn.close()

        # Fechar o diálogo
        self.dialog_exclusao.dismiss()

        # Voltar para a tela de menu
        self.root.current = 'menu'

    def fechar_dialogo_exclusao(self, obj):
        # Fecha o diálogo de exclusão
        self.dialog_exclusao.dismiss()

ReceitasApp().run()
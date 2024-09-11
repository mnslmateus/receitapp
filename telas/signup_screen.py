from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from database import criar_usuario
import re

class SignUpScreen(MDScreen):
    # Variável para armazenar o diálogo de erro
    dialog = None

    def cadastrar(self, nome, email, senha, confirmar_senha):
        # Verifica se as senhas coincidem
        if senha != confirmar_senha:
            # Mostra um diálogo de erro se as senhas não coincidem
            self.mostrar_dialogo("Erro", "As senhas não coincidem ou este email já está cadastrado.")
            return

        # Verifica se a senha é válida
        if not self.validate_senha(senha):
            # Mostra um diálogo de erro se a senha não é válida
            self.mostrar_dialogo("Erro", "A senha deve ter pelo menos 8 caracteres, incluindo um dígito, uma letra maiúscula, uma minúscula e um carácter especial.")
            return

        # Tenta criar um usuário com os dados fornecidos
        success = criar_usuario(nome, email, senha)
        if success:
            # Se o usuário for criado com sucesso, volta para a tela de login
            self.manager.current = 'login'
        else:
            # Mostra um diálogo de erro se o email já está cadastrado
            self.mostrar_dialogo("Erro", "Este email já está cadastrado.")

    def validate_senha(self, senha):
        # Verifica se a senha tem pelo menos 8 caracteres
        if len(senha) < 8:
            return False
        # Verifica se a senha tem um dígito
        if not re.search(r"\d", senha):
            return False
        # Verifica se a senha tem uma letra maiúscula
        if not re.search(r"[A-Z]", senha):
            return False
        # Verifica se a senha tem uma letra minúscula
        if not re.search(r"[a-z]", senha):
            return False
        # Verifica se a senha tem um carácter especial
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            return False
        # Verifica se a senha tem um espaço
        if " " in senha:
            return False
        # Se a senha passar por todas as verificações, retorna True
        return True

    def mostrar_dialogo(self, title, text):
        # Verifica se o diálogo já foi criado
        if not self.dialog:
            # Cria um diálogo com um botão OK
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                    ),
                ],
            )
        # Abre o diálogo
        self.dialog.open()

    def close_dialog(self, *args):
        # Fecha o diálogo
        self.dialog.dismiss()

class MyApp(App):
    def build(self):
        # Cria um gerenciador de telas
        sm = ScreenManager()
        # Adiciona a tela de cadastro ao gerenciador de telas
        sm.add_widget(SignUpScreen(name='signup'))
        # Retorna o gerenciador de telas
        return sm

if __name__ == '__main__':
    # Inicia o aplicativo
    MyApp().run()

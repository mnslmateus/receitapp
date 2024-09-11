from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from database import verificar_usuario, iniciar_sessao

class LoginScreen(MDScreen):
    def fazer_login(self, email, password):
        # Verifica se o email e senha estão corretos
        user_id = verificar_usuario(email, password)
        
        # Se o usuário for encontrado, inicia a sessão
        if user_id:
            # Inicia a sessão do usuário ao fazer login
            iniciar_sessao(user_id)
            # Redireciona para a tela do menu
            self.manager.current = 'menu'
        else:
            # Obtém a instância do aplicativo em execução
            app = MDApp.get_running_app()
            # Mostra um diálogo de erro se o login falhar
            app.alerta_dialogo("Login falhou", "Email ou senha incorretos.")
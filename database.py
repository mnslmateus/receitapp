import sqlite3
import bcrypt

# Conexão com o banco de dados
def conectar_bd():
    return sqlite3.connect('app.db')

# Criação das tabelas de usuários e receitas
def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL)''')
    
    # Tabela de sessões
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessao (
                        id_sessao INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_usuario INTEGER,
                        logado BOOLEAN NOT NULL,
                        FOREIGN KEY (id_usuario) REFERENCES usuarios(id))''')
    
    # Tabela de receitas
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         titulo TEXT NOT NULL,
                         descricao TEXT,
                         ingredientes TEXT NOT NULL,
                         instrucoes TEXT NOT NULL,
                         id_usuario INTEGER,
                         categoria TEXT,
                         subcategoria TEXT,
                         FOREIGN KEY (id_usuario) REFERENCES usuarios(id))''')
    
    conn.commit()
    conn.close()

# Função para criar um novo usuário
def criar_usuario(nome, email, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, hashed_pw))
        conn.commit()
        sucesso = True
    except sqlite3.IntegrityError:
        sucesso = False
    finally:
        conn.close()
    return sucesso

# Função para verificar credenciais de login
def verificar_usuario(email, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[1]):
        return resultado[0]  # Retorna o ID do usuário se as credenciais estiverem corretas
    return None

# Função para iniciar sessão do usuário
def iniciar_sessao(id_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Encerra qualquer sessão anterior para o usuário
    cursor.execute("UPDATE sessao SET logado = 0 WHERE id_usuario = ?", (id_usuario,))
    # Inicia uma nova sessão
    cursor.execute("INSERT INTO sessao (id_usuario, logado) VALUES (?, 1)", (id_usuario,))
    conn.commit()
    conn.close()

# Função para encerrar a sessão do usuário
def encerrar_sessao(id_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Encerra a sessão do usuário específico
    cursor.execute("UPDATE sessao SET logado = 0 WHERE id_usuario = ?", (id_usuario,))
    conn.commit()
    conn.close()

# Função para obter o ID do usuário logado
def get_usuario_logado_id():
    conn = conectar_bd()
    cursor = conn.cursor()
    # Verifica se há uma sessão ativa para um usuário
    cursor.execute("SELECT id_usuario FROM sessao WHERE logado = 1 LIMIT 1")
    usuario = cursor.fetchone()
    conn.close()
    return usuario[0] if usuario else None

# Função para adicionar uma nova receita
def adicionar_receita(titulo, descricao, ingredientes, instrucoes, id_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Insira os dados da receita no banco de dados
    cursor.execute('''
        INSERT INTO receitas (titulo, descricao, ingredientes, instrucoes, id_usuario)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, descricao, ingredientes, instrucoes, id_usuario))

    conn.commit()
    conn.close()

# Função para obter receitas de um usuário
def get_receitas_usuario(id_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receitas WHERE id_usuario = ?", (id_usuario,))
    receitas = cursor.fetchall()
    conn.close()
    return receitas

# Função para obter as receitas mais recentes
def get_receitas_recentes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receitas ORDER BY id DESC LIMIT 5")
    receitas = cursor.fetchall()
    conn.close()
    return receitas

# Função para atualizar a senha do usuário
def atualizar_senha_usuario(id_usuario, senha_atual, nova_senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE id = ?", (id_usuario,))
    resultado = cursor.fetchone()
    if resultado and bcrypt.checkpw(senha_atual.encode('utf-8'), resultado[0]):
        hashed_pw = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (hashed_pw, id_usuario))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

# Função para pesquisar receitas com base no título
def pesquisar_receitas(id_usuario, consulta):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Pesquisar receitas pelo título para um usuário específico
    cursor.execute("""
        SELECT * FROM receitas
        WHERE id_usuario = ? AND titulo LIKE ?
        ORDER BY titulo ASC
    """, (id_usuario, f"%{consulta}%"))
    receitas = cursor.fetchall()
    conn.close()
    return receitas

# Função para apagar a receita
def delete_receita(id_receita):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receitas WHERE id = ?", (id_receita,))
    conn.commit()
    conn.close()
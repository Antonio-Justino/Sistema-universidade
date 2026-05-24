import sqlite3
import os

PASTA_ATUAL = os.path.dirname(__file__)
CAMINHO_BANCO = os.path.join(PASTA_ATUAL, "universidade.db")

PASTA_RAIZ = os.path.dirname(PASTA_ATUAL)
PASTA_ARQUIVOS = os.path.join(PASTA_RAIZ, "arquivos")
PASTA_TAREFAS = os.path.join(PASTA_ARQUIVOS, "tarefas")
PASTA_ENTREGAS = os.path.join(PASTA_ARQUIVOS, "entregas")


def criar_pastas():
    os.makedirs(PASTA_TAREFAS, exist_ok=True)
    os.makedirs(PASTA_ENTREGAS, exist_ok=True)


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabelas():
    criar_pastas()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cursos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        carga_horaria INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        telefone TEXT,
        especialidade TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        cpf TEXT UNIQUE,
        nome TEXT NOT NULL,
        nascimento TEXT,
        sexo TEXT,
        telefone TEXT,
        email TEXT,
        cep TEXT,
        rua TEXT,
        numero TEXT,
        complemento TEXT,
        bairro TEXT,
        cidade TEXT,
        uf TEXT,
        curso_id INTEGER,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(curso_id) REFERENCES cursos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        curso_id INTEGER NOT NULL,
        professor_id INTEGER,
        carga_horaria INTEGER,
        FOREIGN KEY(curso_id) REFERENCES cursos(id),
        FOREIGN KEY(professor_id) REFERENCES professores(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matriculas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        disciplina_id INTEGER,
        UNIQUE(aluno_id, disciplina_id),
        FOREIGN KEY(aluno_id) REFERENCES alunos(id),
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        disciplina_id INTEGER,
        nota1 REAL DEFAULT 0,
        nota2 REAL DEFAULT 0,
        media REAL DEFAULT 0,
        UNIQUE(aluno_id, disciplina_id),
        FOREIGN KEY(aluno_id) REFERENCES alunos(id),
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina_id INTEGER,
        titulo TEXT,
        descricao TEXT,
        data_entrega TEXT,
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas_pdf(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina_id INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_entrega TEXT,
        arquivo_pdf TEXT NOT NULL,
        data_upload TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entregas_pdf(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa_id INTEGER NOT NULL,
        aluno_id INTEGER NOT NULL,
        arquivo_pdf TEXT NOT NULL,
        data_envio TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(tarefa_id, aluno_id),
        FOREIGN KEY(tarefa_id) REFERENCES tarefas_pdf(id),
        FOREIGN KEY(aluno_id) REFERENCES alunos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        valor REAL,
        vencimento TEXT,
        status TEXT,
        FOREIGN KEY(aluno_id) REFERENCES alunos(id)
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios
    (id, nome, login, senha, tipo)
    VALUES (1, 'Administrador', 'admin', '123', 'admin')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios
    (id, nome, login, senha, tipo)
    VALUES (2, 'Antônio Justino', 'aluno', '123', 'aluno')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios
    (id, nome, login, senha, tipo)
    VALUES (3, 'Professor Teste', 'professor', '123', 'professor')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO cursos
    (id, nome, carga_horaria)
    VALUES (1, 'Análise e Desenvolvimento de Sistemas', 2000)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO professores
    (id, nome, email, telefone, especialidade)
    VALUES (1, 'Professor Teste', 'professor@email.com', '62999999999', 'Programação')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO alunos
    (id, usuario_id, cpf, nome, nascimento, sexo, telefone, email,
     cep, rua, numero, complemento, bairro, cidade, uf, curso_id)
    VALUES
    (1, 2, '11111111111', 'Antônio Justino', '20/08/2001', 'Masculino',
     '62977777777', 'antonio@email.com', '74000000', 'Rua A', '100',
     '', 'Centro', 'Goiânia', 'GO', 1)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO alunos
    (id, usuario_id, cpf, nome, nascimento, sexo, telefone, email,
     cep, rua, numero, complemento, bairro, cidade, uf, curso_id)
    VALUES
    (2, NULL, '22222222222', 'Maria Oliveira', '15/05/2002', 'Feminino',
     '62988888888', 'maria@email.com', '74000000', 'Rua B', '200',
     '', 'Setor Sul', 'Goiânia', 'GO', 1)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO alunos
    (id, usuario_id, cpf, nome, nascimento, sexo, telefone, email,
     cep, rua, numero, complemento, bairro, cidade, uf, curso_id)
    VALUES
    (3, NULL, '33333333333', 'João Silva', '10/01/2003', 'Masculino',
     '62999999999', 'joao@email.com', '74000000', 'Rua C', '300',
     '', 'Jardim Goiás', 'Goiânia', 'GO', 1)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO disciplinas
    (id, nome, curso_id, professor_id, carga_horaria)
    VALUES (1, 'Algoritmos', 1, 1, 80)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO disciplinas
    (id, nome, curso_id, professor_id, carga_horaria)
    VALUES (2, 'Banco de Dados', 1, 1, 80)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO disciplinas
    (id, nome, curso_id, professor_id, carga_horaria)
    VALUES (3, 'Estrutura de Dados', 1, 1, 80)
    """)

    for aluno_id in [1, 2, 3]:
        for disciplina_id in [1, 2, 3]:
            cursor.execute("""
            INSERT OR IGNORE INTO matriculas
            (aluno_id, disciplina_id)
            VALUES (?, ?)
            """, (aluno_id, disciplina_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso")
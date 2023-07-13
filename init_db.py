import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ratingsunb_db",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Criar tabela de usuários
cur.execute('DROP TABLE IF EXISTS Usuarios;')
cur.execute('CREATE TABLE Usuarios (usuario_id serial PRIMARY KEY,'
            'nome varchar (60) NOT NULL,'
            'matricula varchar (10) NOT NULL,'
            'email varchar(50) NOT NULL,'
            'senha varchar(50) NOT NULL,'
            'curso varchar(25) NOT NULL,'
            'role VARCHAR(10) NOT NULL'
            ');'
            )

# Criar tabela de Departamentos
cur.execute('DROP TABLE IF EXISTS Departamentos;')
cur.execute('CREATE TABLE Departamentos (departamento_id SERIAL PRIMARY KEY,'
            'nome VARCHAR(60) NOT NULL'
            ');'
            )

# Criar tabela de Professores
cur.execute('DROP TABLE IF EXISTS Professores;')
cur.execute('CREATE TABLE Professores (professor_id SERIAL PRIMARY KEY,'
            'nome VARCHAR(60) NOT NULL,'
            'departamento_id INT NOT NULL,'
            'FOREIGN KEY (departamento_id) REFERENCES Departamentos(departamento_id)'
            ');'
            )

# Criar tabela de Disciplinas
cur.execute('DROP TABLE IF EXISTS Disciplinas;')
cur.execute('CREATE TABLE Disciplinas (disciplina_id SERIAL PRIMARY KEY,'
            'nome VARCHAR(60) NOT NULL,'
            'departamento_id INT NOT NULL,'
            'FOREIGN KEY (departamento_id) REFERENCES Departamentos(departamento_id)'
            ');'
            )

# Criar tabela de Turmas
cur.execute('DROP TABLE IF EXISTS Turmas;')
cur.execute('CREATE TABLE Turmas (turma_id SERIAL PRIMARY KEY,'
            'disciplina_id INT NOT NULL,'
            'professor_id INT NOT NULL,'
            'nome VARCHAR(60) NOT NULL,'
            'periodo VARCHAR(10) NOT NULL,'
            'FOREIGN KEY (disciplina_id) REFERENCES Disciplinas(disciplina_id),'
            'FOREIGN KEY (professor_id) REFERENCES Professores(professor_id)'
            ');'
            )


# Criar tabela de Avaliacoes
cur.execute('DROP TABLE IF EXISTS Avaliacoes;')
cur.execute('CREATE TABLE Avaliacoes (avaliacao_id SERIAL PRIMARY KEY,'
            'usuario_id INT NOT NULL,'
            'professor_id INT,'
            'disciplina_id INT,'
            'nota INT NOT NULL,'
            'descricao TEXT,'
            'approved BOOLEAN DEFAULT FALSE,'
            'FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),'
            'FOREIGN KEY (disciplina_id) REFERENCES Disciplinas(disciplina_id),'
            'FOREIGN KEY (professor_id) REFERENCES Professores(professor_id)'
            ');'
            )

cur.execute('DROP TABLE IF EXISTS Denuncias;')
cur.execute('CREATE TABLE Denuncias (denuncia_id SERIAL PRIMARY KEY,'
            'usuario_id INT NOT NULL,'
            'avaliacao_id INT NOT NULL,'
            'descricao TEXT,'
            'FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),'
            'FOREIGN KEY (avaliacao_id) REFERENCES Avaliacoes(avaliacao_id)'
            ');'
            )



# Inserir administrador básico do sistema
cur.execute('INSERT INTO Usuarios (nome, matricula, email, senha, curso, role)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('Administrador',
             '01/0000000',
             'admin@email.com',
             '12345678',
             'Administração',
             'admin')
            )

conn.commit()

cur.close()
conn.close()

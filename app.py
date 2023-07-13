import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database="ratingsunb_db",
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/')
def index():
    if not session.get("email"):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Usuarios WHERE email = %s AND senha = %s',
                        (email, senha))
        user = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        if not email:
            flash('Email é obrigatorio!')
        elif not senha:
            flash('Senha é obrigatória!')
        elif not user:
            flash('Email ou senha incorreta, tente novamente')
            return redirect(url_for('login'))
        else:
            session['name'] = request.form.get("email")
            session['id'] = user[0][0]
            return render_template('index_turmas.html')
    return render_template('login.html')


@app.route("/logout")
def logout():
    session["name"] = None
    session["id"] = None
    return redirect("/")


@app.route('/usuarios/create', methods=('GET', 'POST'))
def create_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']
        curso = request.form['curso']
        role = request.form['role']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Usuarios (nome, matricula, email, senha, curso, role)'
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (nome, matricula, email, senha, curso, role)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_usuarios.html')


@app.route('/usuarios/index')
def index_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Usuarios_View')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index_usuarios.html', usuarios=usuarios)


@app.route('/usuarios/<usuario_id>/edit', methods=('GET', 'POST'))
def edit_usuario(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Usuarios\
                WHERE usuario_id = %s',
                (usuario_id, )
                )
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']
        curso = request.form['curso']
        role = request.form['role']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE Usuarios SET nome=%s, email=%s ,matricula=%s, senha=%s ,curso=%s, role=%s '
                    'WHERE usuario_id = %s',
                    (nome, email, matricula, senha, curso, role, usuario_id)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index_usuarios'))

    return render_template('edit_usuario.html', usuario=usuario)


@app.route('/usuarios/<usuario_id>/delete')
def delete_usuario(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Usuarios WHERE usuario_id=%s', (usuario_id, ))
    conn.commit()
    cur.close()
    conn.close()
    session["name"] = None
    session["id"] = None
    return redirect("/")


@app.route('/professores/create', methods=('GET', 'POST'))
def create_professor():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Departamentos;')
    departamentos = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        departamento = request.form['departamento']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Professores (nome, departamento_id)'
                    'VALUES (%s, %s)',
                    (nome, departamento)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_professores.html', departamentos=departamentos)


@app.route('/professores/index')
def index_professor():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Professores\
                LEFT JOIN Departamentos ON Departamentos.departamento_id = Professores.departamento_id')
    professores = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index_professores.html', professores=professores)


@app.route('/professores/<professor_id>/edit', methods=('GET', 'POST'))
def edit_professor(professor_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Professores'
                ' LEFT JOIN Departamentos ON Departamentos.departamento_id = Professores.departamento_id\
                WHERE professor_id = %s',
                (professor_id, )
                )
    professor = cur.fetchone()
    cur.execute('SELECT * FROM Departamentos;')
    departamentos = cur.fetchall()

    cur.close()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        departamento = request.form['departamento']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE Professores SET nome=%s, departamento_id=%s '
                    'WHERE professor_id = %s',
                    (nome, departamento, professor_id)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index_professor'))

    return render_template('edit_professor.html', professor=professor, departamentos=departamentos)


@app.route('/professores/<professor_id>/delete')
def delete_professor(professor_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Professores WHERE professor_id=%s', (professor_id, ))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index_professor'))


@app.route('/disciplinas/create', methods=('GET', 'POST'))
def create_disciplina():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Departamentos;')
    departamentos = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        departamento = request.form['departamento']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Disciplinas (nome, departamento_id)'
                    'VALUES (%s, %s)',
                    (nome, departamento)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_disciplina.html', departamentos=departamentos)


@app.route('/turmas/create', methods=('GET', 'POST'))
def create_turma():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Professores;')
    professores = cur.fetchall()
    cur.execute('SELECT * FROM Disciplinas;')
    disciplinas = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        disciplina = request.form['disciplina']
        professor = request.form['professor']
        nome = request.form['nome']
        periodo = request.form['periodo']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Turmas (disciplina_id, professor_id, nome, periodo)'
                    'VALUES (%s, %s, %s, %s)',
                    (disciplina, professor, nome, periodo)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create_turma.html', professores=professores, disciplinas=disciplinas)


@app.route('/turmas/index')
def index_turma():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Turmas\
                LEFT JOIN Professores ON Turmas.professor_id = Professores.professor_id\
                LEFT JOIN Disciplinas ON Turmas.disciplina_id = Disciplinas.disciplina_id'
                )
    turmas = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index_turmas.html', turmas=turmas)


@app.route('/turmas/<turma_id>/edit', methods=('GET', 'POST'))
def edit_turma(turma_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Turmas'
                ' LEFT JOIN Professores ON Turmas.professor_id = Professores.professor_id\
                LEFT JOIN Disciplinas ON Turmas.disciplina_id = Disciplinas.disciplina_id\
                WHERE turma_id = %s',
                (turma_id, )
                )
    turma = cur.fetchone()
    cur.execute('SELECT * FROM Professores;')
    professores = cur.fetchall()
    cur.execute('SELECT * FROM Disciplinas;')
    disciplinas = cur.fetchall()

    cur.close()
    conn.close()

    if request.method == 'POST':
        disciplina = request.form['disciplina']
        professor = request.form['professor']
        nome = request.form['nome']
        periodo = request.form['periodo']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE Turmas SET disciplina_id=%s, professor_id=%s, nome=%s, periodo=%s '
                    'WHERE turma_id = %s',
                    (disciplina, professor, nome, periodo, turma_id)
                    )

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index_turma'))

    return render_template('edit_turma.html', turma=turma, professores=professores, disciplinas=disciplinas)


@app.route('/turmas/<turma_id>/delete')
def delete_turma(turma_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Turmas WHERE turma_id=%s', (turma_id, ))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index_turma'))


if __name__ == "__main__":
    app.run()


@app.route('/avaliar_professor/<professor_id>', methods=('GET', 'POST'))
def create_avaliacao_professor(professor_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Professores WHERE professor_id=%s', (professor_id, ))
    professor = cur.fetchone()
    cur.close()
    conn.close()

    if request.method == 'POST':
        nota = request.form['nota']
        descricao = request.form['descricao']
        usuario = request.form['usuario']
        professor = request.form['professor']

        print("nota", nota)
        print("usuario", usuario)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO Avaliacoes (nota, descricao, professor_id, usuario_id)'
                    'VALUES (%s, %s, %s, %s)',
                    (nota, descricao, professor, usuario)
                    )



        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index_professor'))

    return render_template('create_avaliacao.html', professor=professor)

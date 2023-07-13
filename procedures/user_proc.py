import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ratingsunb_db",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()
cur.execute('CREATE or REPLACE PROCEDURE insert_usuario( '
            'varchar,'
            'varchar,'
            'varchar,'
            'varchar,'
            'varchar,'
            'varchar ) LANGUAGE "plpgsql" AS $$ '
            'BEGIN '
            'INSERT INTO Usuarios (nome, matricula, email, senha, curso, role) '
            'values($1,$2,$3,$4,$5,$6); '
            'COMMIT; END; $$;'
            )

conn.commit()
cur.close()
conn.close()


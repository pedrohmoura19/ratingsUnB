import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ratingsunb_db",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

cur = conn.cursor()
cur.execute('CREATE VIEW Usuarios_View AS '
            'SELECT * FROM Usuarios'
            )

conn.commit()
cur.close()
conn.close()


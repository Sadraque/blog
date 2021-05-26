from flask import Flask
from flask import request
from flask import render_template

import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/topicos/cadastrar', methods=['GET', 'POST'])
def topicos():

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        descricao = request.form['descricao']

        if descricao:
            insertTopico(titulo, autor, descricao)

    return listar()

@app.route('/', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect('database/db-blog.db')

        sql = '''SELECT titulo, autor, descricao FROM topicos'''

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()

        return render_template('topicos.html', regs=registros)

    except Error as e:
        print(e)
    finally:
        conn.close()

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

def insertTopico(titulo, autor, descricao):
    try:
        conn = connectDB()

        sql = ''' INSERT INTO topicos(titulo, autor, descricao) VALUES(?,?,?) '''

        cursor = conn.cursor()

        cursor.execute(sql, [titulo, autor, descricao])

        conn.commit()

    except Error as e:
        print(e)

    finally:
        disconnectDB(conn)

def connectDB():
    return sqlite3.connect('database/db-blog.db')

def disconnectDB(conn):
    conn.close()

if __name__ == '__main__':
    app.run()
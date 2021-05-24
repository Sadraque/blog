from flask import Flask
from flask import request
from flask import render_template

import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/topicos/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':
        descricao = request.form['descricao']

        if descricao:
            cadastarTopico(descricao)

    return render_template('cadastrar.html')

@app.route('/topicos/listar', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect('database/db-blog.db')

        sql = '''SELECT * FROM topicos'''

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()

        return render_template('listar.html', regs=registros)

    except Error as e:
        print(e)
    finally:
        conn.close()

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

def cadastarTopico(descricao):
    try:
        conn = sqlite3.connect('database/db-blog.db')

        sql = ''' INSERT INTO topicos(descricao) VALUES(?) '''

        cursor = conn.cursor()

        cursor.execute(sql, [descricao])

        conn.commit()

    except Error as e:
        print(e)

    finally:
        conn.close()


if __name__ == '__main__':
    app.run()
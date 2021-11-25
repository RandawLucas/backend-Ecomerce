from flask import Flask
from flask import request
from flask import jsonify

#instalar o flask_cors (pip3 install -U flask-cors)
from flask_cors import CORS


import sqlite3
from sqlite3 import Error


#######################################################
# Instancia da Aplicacao Flask

app = Flask(__name__)
CORS(app)

#######################################################

# 1. Cadastrar produtos
@app.route('/cadastrar', methods=['GET', 'POST'])

def cadastrar():

    if request.method == 'POST':
        dados = request.get_json()

        name = dados['name']
        price = dados['price']
        content = dados['content']
        imageUrl = dados['imageUrl']

        mensagem = 'Erro - nao cadastrado'


        if name and price and content and imageUrl:
            registro = (name, price, content, imageUrl)

            try:
                conn = sqlite3.connect('databases/produtos.db')

                sql = ''' INSERT INTO produtos(name, price, content, imageUrl)
                              VALUES(?,?,?,?) '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'
                print(mensagem)

            except Error as e:
               return e
            finally:
                conn.close()
        return mensagem


#######################################################

# 2. Listar produtos
@app.route('/listar', methods=['GET'])

def listar():
    try:
        conn = sqlite3.connect('databases/produtos.db')

        sql = '''SELECT * FROM produtos'''

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()

        if registros:
            columns = [x[0] for x in cur.description]
            dados = []
            for r in registros:
                dados.append(dict(zip(columns,r)))


        return jsonify(dados)

    except Error as e:
        return e
    finally:
        conn.close()



#######################################################

# rota deletar
@app.route('/deletar/<int:id>', methods=['DELETE'])

def deletar(id=None):
    if id == None:
        return jsonify({'menssagem': 'parametro invalido'})
    else:
        try:
            conn = sqlite3.connect('databases/produtos.db')

            sql = '''DELETE FROM produtos WHERE id = ''' + str(id)

            cur = conn.cursor()
            cur.execute(sql)

            conn.commit()

            return jsonify({"menssagem": 'registro excluido'})

        except Error as e:
            return jsonify({'menssagem': e})
        finally:
            conn.close()

#######################################################

# Rota de Alteração de dados
@app.route('/alterar/<int:id>', methods=['PUT'])

def alterar(id=None):
    if id == None:
        return jsonify({'mensagem': 'parametro invalido'})
    else:
        if request.method == 'PUT':
            dados = request.get_json()

            name = dados['name']
            price = dados['price']
            content = dados['content']
            imageUrl = dados['imageUrl']

            if name and price and content and imageUrl:
                registro = (name, price, content, imageUrl)

                try:
                    conn = sqlite3.connect('databases/produtos.db')
                    sql = '''UPDATE produtos SET name=?, price=?, content=?, imageUrl=? WHERE id =''' + str(id)
                    cur = conn.cursor()
                    cur.execute(sql, registro)
                    conn.commit()

                    if cur.rowcount > 0:
                        return jsonify({'mensagem': 'registro alterado com sucesso'})
                    else:
                        return jsonify({'mensagem': 'registro não encontrado'})

                    return jsonify({"menssagem": 'registro alterado'})
                except Error as e:
                    return jsonify({'menssagem': e})
                finally:
                    conn.close()
        else:
            return jsonify({'mensagem': 'campos <descricao>, <preco>, e <qtd> sao obrigatorios'})
#######################################################

# Rota de Erro
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return '404.html', 404


#######################################################
# Execucao da Aplicacao

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
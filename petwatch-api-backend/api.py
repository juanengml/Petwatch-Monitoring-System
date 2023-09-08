from flask import Flask, request, jsonify
import os
import shortuuid
from lmodel.vision import salvar_imagem_base64
from lmodel.database import DataBase
from lmodel.storage import Storage
import pendulum

now = pendulum.now("America/Sao_Paulo")

# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'

if not os.path.exists(image_directory):
    os.makedirs(image_directory)

app = Flask(__name__)

# Lista de gatos (simulando um banco de dados)
gatos = []

# Rota para cadastrar um gato
@app.route('/gatos', methods=['POST'])
def cadastrar_gato():
    data = request.get_json()
    nome = data['nome']
    data_nascimento = data['data_nascimento']
    foto_base64 = data['foto']

    # Decodificar a imagem Base64 e salvá-la no diretório
    foto_filename = salvar_imagem_base64(foto_base64, f"{nome}-{shortuuid.uuid()}")
    # pega esse arquivo e uma no miniIO
    
    s3_storage = Storage(uri='http://localhost:9000', access_key='minio_access_key', secret_key='minio_secret_key')

    bucket = f"client-{nome.lower()}-{str(shortuuid.uuid()).lower()}"

    s3_storage.upload(bucket, foto_filename, foto_filename)

    db = DataBase()

    gato = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'foto_name': foto_filename,
        'create_at': now.to_atom_string(),
        'bucket': bucket

    }
    db.insert("table_cats_information", gato)

    return jsonify({'message': 'Gato cadastrado com sucesso'}), 201

# Rota para listar todos os gatos
@app.route('/gatos', methods=['GET'])
def listar_gatos():
    for gato in gatos:
        print(gato)
    return jsonify(gatos)

# Rota para deletar um gato pelo nome
@app.route('/gatos/<string:nome>', methods=['DELETE'])
def deletar_gato(nome):
    for gato in gatos:
        if gato['nome'] == nome:
            gatos.remove(gato)
            return jsonify({'message': 'Gato deletado com sucesso'}), 200
    
    return jsonify({'message': 'Gato não encontrado'}), 404

# Rota para atualizar informações de um gato
@app.route('/gatos/<string:nome>', methods=['PUT'])
def atualizar_gato(nome):
    data = request.get_json()
    novo_nome = data.get('nome')
    nova_data_nascimento = data.get('data_nascimento')
    nova_foto = data.get('foto')
    
    for gato in gatos:
        if gato['nome'] == nome:
            if novo_nome:
                gato['nome'] = novo_nome
            if nova_data_nascimento:
                gato['data_nascimento'] = nova_data_nascimento
            if nova_foto:
                gato['foto'] = nova_foto
            return jsonify({'message': 'Gato atualizado com sucesso'}), 200
    
    return jsonify({'message': 'Gato não encontrado'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

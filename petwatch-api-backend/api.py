from flask import Flask, request, jsonify
import base64
import os
import shortuuid
from lmodel.vision import inference, salvar_imagem_base64, landmarks_similares

# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'

if not os.path.exists(image_directory):
    os.makedirs(image_directory)

app = Flask(__name__)

# Lista de gatos (simulando um banco de dados)
gatos = []

# Rota para verificar os dados do gato
@app.route('/verificar', methods=['POST'])
def verificar_gato():
    data = request.get_json()
    imagem_base64 = data['imagem_base64']
    foto_filename = salvar_imagem_base64(imagem_base64, "target")

    # Extrair landmarks da imagem usando a função inference (certifique-se de que esta função está implementada)
    # segmentar isso aqui para chamada de API
    bbox, landmark = inference(foto_filename)
    print(landmark)

    if not bbox or not landmark:
        return jsonify({'message': 'Não foi possível extrair os landmarks da imagem'}), 400

    # Iterar sobre os gatos no banco de dados e verificar se algum deles corresponde à imagem
    gato_encontrado = None
    for gato in gatos:
        if landmarks_similares(landmark, gato['landmark']):
            gato_encontrado = gato
            break

    if gato_encontrado:
        return jsonify({'message': 'Gato encontrado', 'gato': gato_encontrado}), 200
    else:
        return jsonify({'message': 'Gato não encontrado'}), 404

# Rota para cadastrar um gato
@app.route('/gatos', methods=['POST'])
def cadastrar_gato():
    data = request.get_json()
    nome = data['nome']
    data_nascimento = data['data_nascimento']
    foto_base64 = data['foto']

    # Decodificar a imagem Base64 e salvá-la no diretório
    foto_filename = salvar_imagem_base64(foto_base64, f"{nome}-{shortuuid.uuid()}")
    
    bbox, landmark = inference(foto_filename)
    
    # Verificar se o gato já está cadastrado
    #for gato in gatos:
    #    if gato['nome'] == nome:
    #        return jsonify({'message': 'Gato já cadastrado'}), 400

    gato = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'foto': foto_filename,  # Salva o caminho da imagem
        'bbox': bbox,
        'landmark': landmark

    }
    gatos.append(gato)

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

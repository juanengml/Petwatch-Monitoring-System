from flask import Flask, request, jsonify
import os
import shortuuid
from lmodel.database import DataBase
from lmodel.storage import Storage
import pendulum

now = pendulum.now("America/Sao_Paulo")

# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'

if not os.path.exists(image_directory):
    os.makedirs(image_directory)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista de gatos (simulando um banco de dados)
gatos = []

s3_storage = Storage(uri='http://localhost:9000', access_key='minio_access_key', secret_key='minio_secret_key')
db = DataBase()

# Rota para listar todos os gatos
@app.route('/gatos', methods=['GET'])
def listar_gatos():
    response = db.search("SELECT * FROM table_cats_information;")
    return jsonify(response)


# Rota para cadastrar um gato
@app.route('/gatos', methods=['POST'])
def cadastrar_gato():
    data = request.form
    nome = data['nome']
    data_nascimento = data['data_nascimento']
    db = DataBase()
    result = db.search(f"SELECT * FROM table_cats_information WHERE nome = '{nome}'")

    if len(result)> 0:
        return jsonify({"warning": 'Gato já cadastrado', "response": result})
    
    # Verifique se um arquivo de vídeo foi enviado
    if 'video' not in request.files or 'image' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de vídeo enviado'}), 400

    video = request.files['video']
    image = request.files['image']

    # Verifique se o arquivo de vídeo tem uma extensão válida, por exemplo, .mp4
    if not video.filename.endswith(('.mp4', '.avi', '.mov')):
        return jsonify({'error': 'Formato de vídeo não suportado'}), 400

    if not image.filename.endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Formato de image não suportado'}), 400

    # Salve o arquivo de vídeo no diretório configurado
    image_local = f'uploads/images/{nome}_{image.filename}'
    video_local = f'uploads/videos/{nome}_{video.filename}'

    target_video = f"{nome.lower()}/{video.filename}"
    target_image = f"{nome.lower()}/{image.filename}"

    video.save(video_local)
    image.save(image_local)
    bucket = f"{nome.lower()}-{str(shortuuid.uuid()).lower()}"

    s3_storage.upload(bucket, video_local, target_video)
    s3_storage.upload(bucket, image_local, target_image)

    # Agora você pode realizar as operações necessárias com os dados do gato e o caminho do vídeo
    db = DataBase()
    
    gato = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'video_path': target_video,
        'create_at': now.to_atom_string(),
        'bucket': bucket,
        'image': target_image
    }

    db.insert("table_cats_information", gato)

    return jsonify({'message': 'Gato cadastrado com sucesso'}), 201


@app.route('/gatos/<string:nome>', methods=['PUT'])
def atualizar_gato(nome):
    data = request.form  # Agora estamos recebendo dados do formulário
    novo_nome = data.get('nome')
    nova_data_nascimento = data.get('data_nascimento')

    if 'image' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de vídeo enviado'}), 400

    image = request.files['image']
   
    # Verifique se a foto foi enviada e salve-a no MinIO
    if image:
        # Certifique-se de que o nome do arquivo seja exclusivo (por exemplo, use um UUID)
        image_local = f'uploads/images/{nome}_{image.filename}'
        target_image = f"{nome.lower()}/{image.filename}"
        image.save(image_local)

        # Salve a imagem no MinIO
        result = db.search(f"SELECT * FROM table_cats_information WHERE nome='{nome}'")[0]
        s3_storage.upload(result['bucket'], image_local, target_image)

    query = f"UPDATE table_cats_information SET"
    if novo_nome:
        query += f" nome = '{novo_nome}',"
    if nova_data_nascimento:
        query += f" data_nascimento = '{nova_data_nascimento}',"
    if image:
        query += f" image = '{target_image}',"  # Use o caminho da imagem no MinIO

    # Remova a vírgula final e adicione a cláusula WHERE
    query = query.rstrip(',')
    query += f" WHERE nome = '{nome}'"

    db.query(query)
    return jsonify({'message': 'Gato atualizado com sucesso'}), 200

@app.route('/gatos/<string:nome>', methods=['DELETE'])
def deletar(nome):
    result = db.search(f"SELECT * FROM table_cats_information WHERE nome='{nome}'")
    if len(result) > 0:
        bucket = result[0]['bucket']
        s3_storage.delete_bucket(bucket)
        db.delete('table_cats_information', nome)
        return jsonify({"message": "Gato deletado"}), 200

    return jsonify({"message": "Gato não encontrado"}), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

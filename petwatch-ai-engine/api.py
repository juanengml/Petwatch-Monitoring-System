from flask import Flask, request, jsonify
import os
from lmodel.vision import salvar_imagem_base64
from lmodel.vision import inference_yolo, inferencia_cnn
from lmodel.database import DataBase
from lmodel.logger_status import logger_table
import pendulum

# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'
import cv2

if not os.path.exists(image_directory):
    os.makedirs(image_directory)

app = Flask(__name__)


# Rota para verificar os dados do gato
@app.route('/inferencia', methods=['POST'])
def verificar_gato():
    now = pendulum.now("America/Sao_Paulo")
    db = DataBase()
    data = request.get_json()
    imagem_base64 = data['imagem_base64']
    foto_filename = cv2.imread(salvar_imagem_base64(imagem_base64, "target"))

    result_inference = inference_yolo(foto_filename) 
    
    if result_inference != None:
        label = inferencia_cnn(result_inference)
        logger_table['message'] = 'Gato encontrado'
        logger_table['date'] = now.to_date_string()
        logger_table['hour'] = now.to_atom_string().split("T")[1]
        db.insert('request_log', logger_table)
        return jsonify({
            'message': 'Gato encontrado', 
            'nome': label, 
            'label': result_inference['label'],
            'bbox': result_inference['bbox']
        }), 200
    else:
        logger_table['message'] = 'Gato não encontrado'
        logger_table['status'] = 'error'
        logger_table['date'] = now.to_date_string()
        logger_table['hour'] = now.to_atom_string().split("T")[1]

        db.insert('request_log', logger_table)
        return jsonify({'message': 'Gato não encontrado'}), 404

@app.route('/inferencia/status', methods=['GET'])
def status_model():
    db = DataBase()
    # Consulta para buscar os últimos 10 registros com sucesso
    query = 'SELECT * FROM request_log WHERE status = "sucesso" ORDER BY id DESC LIMIT 500'
    success_logs = db.search(query)

    # Consulta para buscar os últimos 10 registros com erro
    query = 'SELECT * FROM request_log WHERE status = "erro" ORDER BY id DESC LIMIT 500'
    error_logs = db.search(query)
    # Consultar e contar solicitações bem-sucedidas
    success_count = db.search('SELECT COUNT(*) as count FROM request_log WHERE status = "sucesso"')

    # Consultar e contar solicitações com erro
    error_count = db.search('SELECT COUNT(*) as count FROM request_log WHERE status = "erro"')
    
    model_files = [file for file in os.listdir("lmodel") if file.endswith(".h5")]

    # Montar um dicionário com as estatísticas
    statistics = {
        'success_count': success_count[0] if len(success_count) > 0 else success_count,
        'success_logs': [dict(success) for success in success_logs],
        'error_count': error_count[0] if len(error_count) > 0 else error_count,
        'error_logs': [dict(error) for error in error_logs],
        "model": model_files
    }
    
    # Retornar as estatísticas como uma resposta JSON
    return jsonify(statistics)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

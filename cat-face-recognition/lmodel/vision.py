import cv2
from components.cat_frontal_face_detection import detect_cat_face
import base64
import os
import numpy as np

def montar_dict_landmarks(landmarks):
    pontos_de_interesse = {
        "Left Eye": landmarks[0],
        "Right Eye": landmarks[1],
        "Mouth": landmarks[2],
        "Left Ear-1": landmarks[3],
        "Left Ear-2": landmarks[4],
        "Left Ear-3": landmarks[5],
        "Right Ear-1": landmarks[6],
        "Right Ear-2": landmarks[7],
        "Right Ear-3": landmarks[8]
    }
    return pontos_de_interesse

def converter_dados_em_listas(retangulo, landmarks):
    # Converter o objeto de retângulo (bbox) em uma lista de coordenadas
    bbox = list()
    for ret in retangulo:
        bbox.append({
            "left":ret.left(), 
            "top":ret.top(), 
            "right":ret.right(), 
            "bottom": ret.bottom()
        })
        

    # Converter o array de landmarks em uma lista de listas de coordenadas
    lands = list()
    for landmark in landmarks:
        lands.append(montar_dict_landmarks(landmark.tolist()))

    return bbox, lands

def inference(foto_filename):
    cat_img = cv2.imread(foto_filename)
    cat_img = cv2.resize(cat_img, (720,480), interpolation = cv2.INTER_AREA)

    bbox, landmark = detect_cat_face(cat_img) 
    bbox, landmark = converter_dados_em_listas(bbox, landmark)

    print(bbox, landmark)
    return bbox, landmark


# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'


def salvar_imagem_base64(foto_base64, nome):
    foto_bytes = base64.b64decode(foto_base64)
    foto_filename = os.path.join(image_directory, f'{nome}.jpg')

    with open(foto_filename, 'wb') as foto_file:
        foto_file.write(foto_bytes)

    return foto_filename


def converter_landmark_para_lista(landmark):
    # Extrair as coordenadas dos dicionários e convertê-las em listas
    landmark_lista = list()
    for coord in landmark:
        landmark_lista = [[mark[0], mark[1]] for mark in coord.values()]

    return landmark_lista


def check_land(landmark,flag):
    print(f"{flag}: ",landmark, type(landmark), "convert-> ", converter_landmark_para_lista(landmark))


def landmarks_similares(landmark1, landmark2, limite=10.0):
    """
    Função para verificar se dois conjuntos de landmarks são similares.
    
    Args:
        landmark1 (list): Lista de landmarks do primeiro conjunto.
        landmark2 (list): Lista de landmarks do segundo conjunto.
        limite (float): Limite para considerar os landmarks como similares.
        
    Returns:
        bool: True se os landmarks são similares, False caso contrário.
    """
    # Certifique-se de que ambos os conjuntos de landmarks têm o mesmo número de pontos
    if len(landmark1) != len(landmark2):
        return False

    check_land(landmark1, "landmark1")
    #check_land(landmark2, "landmark2")

    landmark1 = converter_landmark_para_lista(landmark1)
    landmark2 = converter_landmark_para_lista(landmark2)

    # Calcular a distância Euclidiana média entre os landmarks
    distancias = [np.linalg.norm(np.array(p1) - np.array(p2)) for p1, p2 in zip(landmark1, landmark2)]
    distancia_media = np.mean(distancias)

    # Verificar se a distância média está abaixo do limite
    return distancia_media < limite

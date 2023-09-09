
import os
import base64
# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'

from PIL import Image

def resize_image(input_path, output_path, new_size):
    try:
        # Abre a imagem
        image = Image.open(input_path)

        # Redimensiona a imagem para as novas dimensões (new_size é uma tupla, por exemplo, (width, height))
        resized_image = image.resize(new_size)

        # Salva a imagem redimensionada no novo caminho
        resized_image.save(output_path)

        return output_path  # Retorna o caminho para a imagem redimensionada
    except Exception as e:
        return str(e)


def salvar_imagem_base64(foto_base64, nome):
    foto_bytes = base64.b64decode(foto_base64)
    foto_filename = os.path.join(image_directory, f'{nome}.jpg')

    with open(foto_filename, 'wb') as foto_file:
        foto_file.write(foto_bytes)

    return foto_filename

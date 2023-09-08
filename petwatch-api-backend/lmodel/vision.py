
import os
import base64
# Diretório para armazenar as imagens dos gatos
image_directory = 'imagens_gatos'


def salvar_imagem_base64(foto_base64, nome):
    foto_bytes = base64.b64decode(foto_base64)
    foto_filename = os.path.join(image_directory, f'{nome}.jpg')

    with open(foto_filename, 'wb') as foto_file:
        foto_file.write(foto_bytes)

    return foto_filename

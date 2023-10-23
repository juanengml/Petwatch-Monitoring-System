#from lmodel.database import DataBase

#db = DataBase()

#print(db.query("SELECT * FROM table_cats_information;"))
import argparse

from requests import get,post, put, delete

def cadastra():
    url = 'http://192.168.0.43:5001/gatos'
    files = {
        'video': open('/home/juannascimento/Documentos/Lora.mp4', 'rb'),
        'image': open('/home/juannascimento/Documentos/dataset/test/lora/cat_1385.jpg', 'rb')
    }
    data = {'nome': 'Lora', 'data_nascimento': '01/06/2019'}

    response = post(url, files=files, data=data)

    print(response.status_code)
    print(response.json())

    url = 'http://192.168.0.43:5001/gatos'
    files = {
        'video': open('/home/juannascimento/Documentos/Uly.mp4', 'rb'),
        'image': open('/home/juannascimento/Documentos/dataset/test/uly/cat_2.jpg', 'rb')
    }
    data = {'nome': 'Uly', 'data_nascimento': '01/11/2019'}

    response = post(url, files=files, data=data)

    print(response.status_code)
    print(response.json())


def status():
    url = 'http://192.168.0.43:5001/gatos'
  
    response = get(url).json()
    print(response)

def update():
    url = 'http://192.168.0.43:5001/gatos/Lora'
    files = {
        'image': open('/home/juannascimento/Documentos/dataset/lora/cat_818.jpg', 'rb')
    }
    data = {'nome': 'Lora', 'data_nascimento': '01/01/2019'}

    response = put(url, files=files, data=data)

    print(response.status_code)
    print(response.json())

def deleter():
    lista_nomes = ['Lora', 'Uly']
    for name in lista_nomes:
        url = f'http://192.168.0.43:5001/gatos/{name}'

        response = delete(url)

        print(response.status_code)
        print(response.json())

def abre_imagem():

    # URL base para a rota de obtenção de imagem
    base_url = 'http://192.168.0.43:5001/get_image/'

    # Dados dos gatos
    data = [
        {
            'bucket': 'lora-7hf2d6yj5rszg772hqtn3n',
            'image_path': 'lora/cat_818.jpg',
            'nome': 'Lora',
        },
        {
            'bucket': 'uly-kky4yrt9cg28mt58hspwns',
            'image_path': 'uly/cat_225.jpg',
            'nome': 'Uly',
        },
    ]

    for cat in data:
        bucket = cat['bucket']
        image_path = cat['image_path']
        nome = cat['nome']

        # Monta a URL completa
        url = f'{base_url}{bucket}/{image_path}'

        # Realiza a requisição GET
        print(url)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exemplo de CLI')
    parser.add_argument('--cadastra', action='store_true', help='Executa a função cadastra')
    parser.add_argument('--update', action='store_true', help='Executa a função update')
    parser.add_argument('--status', action='store_true', help='Executa a função status')
    parser.add_argument('--deletar', action='store_true', help='Executa a função deleter')
    parser.add_argument('--abre_imagem', action='store_true', help='Executa a função abre_imagem')

    args = parser.parse_args()

    if args.cadastra:
        cadastra()
    if args.update:
        update()
    if args.status:
        status()
    if args.deletar:
        deleter()
    if args.abre_imagem:
        abre_imagem()
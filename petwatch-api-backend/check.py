#from lmodel.database import DataBase

#db = DataBase()

#print(db.query("SELECT * FROM table_cats_information;"))

from requests import get,post, put, delete

def cadastra():
    url = 'http://localhost:5001/gatos'
    files = {
        'video': open('/home/juannascimento/Documentos/Lora.mp4', 'rb'),
        'image': open('/home/juannascimento/Documentos/dataset/lora/cat_964.jpg', 'rb')
    }
    data = {'nome': 'Lora', 'data_nascimento': '01/06/2019'}

    response = post(url, files=files, data=data)

    print(response.status_code)
    print(response.json())

    url = 'http://localhost:5001/gatos'
    files = {
        'video': open('/home/juannascimento/Documentos/Uly.mp4', 'rb'),
        'image': open('/home/juannascimento/Documentos/dataset/uly/cat_225.jpg', 'rb')
    }
    data = {'nome': 'Uly', 'data_nascimento': '01/11/2019'}

    response = post(url, files=files, data=data)

    print(response.status_code)
    print(response.json())


def status():
    url = 'http://localhost:5001/gatos'
  
    response = get(url).json()
    print(response)

def update():
    url = 'http://localhost:5001/gatos/Lora'
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
        url = f'http://localhost:5001/gatos/{name}'

        response = delete(url)

        print(response.status_code)
        print(response.json())

def abre_imagem():

    # URL base para a rota de obtenção de imagem
    base_url = 'http://localhost:5001/get_image/'

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
        

cadastra()

#update()
status()

#deleter()    

status()
# abre_imagem()

#http://localhost:5001/get_image/lora-vrhoxvhodvbnghee57oeyz/lora/cat_818.jpg
#http://localhost:5001/get_image/uly-f99sqagfruqxxvbrcacm2i/uly/cat_225.jpg
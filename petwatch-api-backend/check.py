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

cadastra()

update()
status()

#deleter()    

# status()
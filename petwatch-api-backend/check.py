#from lmodel.database import DataBase

#db = DataBase()

#print(db.query("SELECT * FROM table_cats_information;"))

from requests import get,post, put, delete

def cadastra():
    url = 'http://localhost:5000/gatos'
    files = {
        'video': open('/home/juannascimento/Documentos/Lora.mp4', 'rb'),
        'image': open('/home/juannascimento/Documentos/dataset/lora/cat_964.jpg', 'rb')
    }
    data = {'nome': 'Lora', 'data_nascimento': '01/01/2019'}

    response = post(url, files=files, data=data)

    print(response.status_code)
    print(response.json())

def status():
    url = 'http://localhost:5000/gatos'
  
    response = get(url).json()
    print(response)

def update():
    url = 'http://localhost:5000/gatos/Lora'
    files = {
        'image': open('/home/juannascimento/Documentos/dataset/lora/cat_818.jpg', 'rb')
    }
    data = {'nome': 'Lora', 'data_nascimento': '01/02/2019'}

    response = put(url, files=files, data=data)

    print(response.status_code)
    print(response.json())

def deleter():
    url = 'http://localhost:5000/gatos/Lora'

    response = delete(url)

    print(response.status_code)
    print(response.json())

cadastra()

update()
status()

deleter()    

status()
from requests import post

class Model():

    def __init__(self):
        self.endpoint = "http://192.168.0.43:5000/inferencia"     

    def recognize(self, img):
        data = {
            "imagem_base64": img 
        }
        response = post(self.endpoint, json=data).json()
        return response


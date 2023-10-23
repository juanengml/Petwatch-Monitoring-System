import cv2
import streamlit as st
import pandas as pd
from requests import post
import base64
from PIL import Image
import bbox_visualizer as bbv

# Função para ler a imagem em Base64 de um arquivo e convertê-la em uma string Base64
def ler_imagem_base64(nome_arquivo):
    with open(nome_arquivo, "rb") as imagem_file:
        imagem_base64 = base64.b64encode(imagem_file.read()).decode('utf-8')
    return imagem_base64

class Verify(object):

    @staticmethod
    def verificar_gato():
        st.sidebar.image("src/SamPoderoso.png")
        col1, col2 = st.columns(2)

        with col1:
            uploaded_image = st.file_uploader("Carregar uma imagem", type=["jpg", "png", "jpeg"])

            if st.button('Verificar') == True:
                try:
                    image = Image.open(uploaded_image)
                    image.save("src/imagem_salva.jpg")

                    data = {
                        "imagem_base64": ler_imagem_base64("src/imagem_salva.jpg")
                        }
                    endpoint = "http://192.168.0.43:5000/inferencia"
                    result = post(endpoint, json=data).json()
                    tabela = result.copy()
                    if 'bbox' in result:
                        tabela.pop('bbox')
                        st.table([tabela])

                    with col2:
                        if uploaded_image is not None:
                            #st.write(result)
                            if 'bbox' in result:
                                x1, y1, x2, y2 = result["bbox"]["x"], result["bbox"]["y"], result["bbox"]["x2"], result["bbox"]["y2"]
                                img = cv2.imread("src/imagem_salva.jpg")
                                bbox = [x1, y1, x2, y2]
                                label = result['nome'].upper().strip()

                                img = bbv.draw_rectangle(img, bbox)
                                img = bbv.add_label(img, label, bbox, top=False)

                                img_rgb = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (320,280))

                                st.image(img_rgb, caption=f"Imagem com {result['nome']}", use_column_width=True)

                                col2.success("Inferencia feita com sucesso !")
                        
                            #col2.error("Falha ao reconhecer gato na image")
                            #col2.image("src/sam.png")

                except AttributeError:  
                    st.warning("Faça upload de uma imagem para verificação verificação")

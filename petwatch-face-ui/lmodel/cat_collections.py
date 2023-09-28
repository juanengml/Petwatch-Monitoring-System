import streamlit as st
from requests import post, get, put, delete
from streamlit_option_menu import option_menu
import requests


class Collections(object):

    @staticmethod
    def cadastra():
        st.subheader("Cadastrar Gato")
        nome = st.text_input("Nome do Gato")
        data_nascimento = st.text_input("Data de Nascimento")
        video_file = st.file_uploader("Selecione um vídeo do gato")
        image_file = st.file_uploader("Selecione uma imagem do gato")

        if st.button("Cadastrar"):
            if not nome or not data_nascimento or not video_file or not image_file:
                st.error("Por favor, preencha todos os campos e selecione os arquivos.")
            else:
                url = 'http://192.168.0.43:5001/gatos'
                files = {'video': video_file, 'image': image_file}
                data = {'nome': nome, 'data_nascimento': data_nascimento}

                response = post(url, files=files, data=data)

                if response.status_code == 201:
                    st.success("Gato cadastrado com sucesso.")
                else:
                    st.error(f"Erro ao cadastrar o gato. Status Code: {response.status_code}")

    @staticmethod
    def status():
        css_style = f"""
<style>
    /* Seu CSS personalizado aqui */
    .rounded-image img {{
        border-radius: 50%;
        /* Outros estilos que você deseja aplicar à imagem */
    }}
</style>
"""
        st.title("Status dos Gatos")
        try:
            url = 'http://192.168.0.43:5001/gatos'
            response = get(url).json()
            if response:
                #st.write(response)
                count = 0
                for col_aux in st.columns(len(response)):
                    col_aux.subheader(response[count]['nome'])
                    image = response[count]['image']
                    bucket = response[count]['bucket']
                    link = f"http://192.168.0.43:9000/{bucket}/{image}"
                    col_aux.markdown(f'{css_style}<div class="rounded-image"><img src="{link}" /></div>', unsafe_allow_html=True)


                    col_aux.metric("Data Nascimento", value=response[count]['data_nascimento'])
                    col_aux.info(f"bucket - {bucket}")
                    
                    #st.metric(label="Total Error", value=response['error_count']['count'])


                    count = count + 1
                st.subheader("Registros")
                st.table(response)
            else:
                st.info("Nenhum gato encontrado.")
        except requests.exceptions.ConnectionError as error:
             st.warning("STATUS: 192.168.0.43 OFFLINE ", icon='🛑')

    @staticmethod
    def update():
        st.subheader("Atualizar Gato")
        nome = st.text_input("Nome do Gato")
        data_nascimento = st.text_input("Nova Data de Nascimento")
        image_file = st.file_uploader("Selecione uma nova imagem do gato")

        if st.button("Atualizar"):
            if not nome or (not data_nascimento and not image_file):
                st.error("Por favor, preencha o nome do gato e pelo menos um dos campos para atualização.")
            else:
                url = f'http://192.168.0.43:5001/gatos/{nome}'
                files = {'image': image_file} if image_file else None
                data = {'nome': nome, 'data_nascimento': data_nascimento} if data_nascimento else {'nome': nome}

                response = put(url, files=files, data=data)

                if response.status_code == 200:
                    st.success("Gato atualizado com sucesso.")
                else:
                    st.error(f"Erro ao atualizar o gato. Status Code: {response.status_code}")

    @staticmethod
    def deleter():
        st.subheader("Remover Gato")
        nome = st.text_input("Nome do Gato")

        if st.button("Deletar"):
            if not nome:
                st.error("Por favor, preencha o nome do gato para exclusão.")
            else:
                url = f'http://192.168.0.43:5001/gatos/{nome}'
                response = delete(url)

                if response.status_code == 200:
                    st.success("Gato deletado com sucesso.")
                else:
                    st.error(f"Erro ao deletar o gato. Status Code: {response.status_code}")


class CollectionSelector(object):
    @staticmethod
    def seletor():
        st.sidebar.markdown("![Alt Text](https://raw.githubusercontent.com/juanengml/Petwatch-Monitoring-System/main/petwatch-face-ui/src/ezgif-1-c06d2fccba.gif)")

    # Menu de opções
        menu = option_menu(None, ["Status", "Cadastrar", "Deletar", 'Atualizar'],
                        icons=['Status', 'Cadastrar', "Deletar", 'Atualizar'],
                        menu_icon="cast", default_index=0, orientation="horizontal")

        if menu == "Cadastrar":
            Collections.cadastra()
        elif menu == "Status":
            Collections.status()
        elif menu == "Atualizar":
            Collections.update()
        elif menu == "Deletar":
            Collections.deleter()
# Use a imagem base do Python 3.8
FROM python:3.8

# Define o diretório de trabalho no container
WORKDIR /app

RUN apt update
RUN apt-get install libgl1-mesa-glx -y

# Copie os arquivos do diretório local para o diretório de trabalho no container
COPY lmodel /app/lmodel
COPY api.py /app/api.py
RUN mkdir /app/imagens_gatos/
COPY imagens_gatos/target.jpg /app/imagens_gatos/target.jpg

COPY requirements.txt /app/requirements.txt
# Instale as dependências da sua API Flask
RUN pip install -r requirements.txt

# Expõe a porta em que a sua aplicação Flask irá rodar (ajuste conforme necessário)
EXPOSE 5000

# Comando para executar a sua aplicação Flask
CMD ["python", "api.py"]

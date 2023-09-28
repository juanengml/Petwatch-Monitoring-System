# Use a imagem oficial do Python como imagem base
FROM python:3.8

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

RUN apt update
RUN apt-get install libgl1-mesa-glx -y
# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do diretório atual para o contêiner no diretório de trabalho
COPY . .

# Exponha a porta 8501 para o Streamlit
EXPOSE 8501

# Comando para executar o aplicativo Streamlit
CMD ["streamlit", "run", "app.py"]

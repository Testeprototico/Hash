# Use uma imagem base que inclui Python
FROM python:3.11-slim

# Instala o Hashcat
RUN apt-get update && \
    apt-get install -y hashcat

# Cria um diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Define o comando para executar seu aplicativo
CMD ["python", "app.py"]

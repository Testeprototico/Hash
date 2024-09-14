# Use uma imagem base de Python
FROM python:3.9-slim

# Instala as dependências do sistema, incluindo o Hashcat
RUN apt-get update && \
    apt-get install -y hashcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY . /app

# Instala as dependências
RUN pip install Flask

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]



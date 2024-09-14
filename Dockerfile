# Use uma imagem base com Python e o sistema operacional adequado
FROM python:3.11-slim

# Instala as dependências do sistema, incluindo o Hashcat
RUN apt-get update && \
    apt-get install -y hashcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cria um diretório de trabalho para o aplicativo
WORKDIR /app

# Copia os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Exponha a porta em que o Flask irá rodar
EXPOSE 5000

# Define o comando para iniciar a aplicação Flask
CMD ["python", "app.py"]

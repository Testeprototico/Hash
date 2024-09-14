# Use uma imagem base com Ubuntu
FROM ubuntu:20.04

# Instale as dependências necessárias
RUN apt-get update && \
    apt-get install -y hashcat libopencl-dev ocl-icd-libopencl1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /data

# Adicione o arquivo hash.txt ao contêiner
COPY hash.txt /data/hash.txt

# Comando para verificar a instalação do Hashcat
CMD ["hashcat", "--version"]

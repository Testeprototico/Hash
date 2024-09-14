# Use uma imagem base com Ubuntu
FROM ubuntu:20.04

# Defina a variável de ambiente TZ para o fuso horário desejado
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo  # Substitua pelo seu fuso horário

# Atualize e instale pacotes necessários
RUN apt-get update && \
    apt-get install -y \
    tzdata \
    hashcat \
    opencl-headers \
    ocl-icd-libopencl1 \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure o fuso horário
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Defina o diretório de trabalho
WORKDIR /data

# Adicione o arquivo hash.txt ao contêiner
COPY hash.txt /data/hash.txt

# Comando para verificar a instalação do Hashcat
CMD ["hashcat", "--version"]

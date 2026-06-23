FROM ubuntu:24.04

# Evitar prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Metadados
LABEL maintainer="Web Security Scanner"
LABEL description="Automated Web Security Scanner with Nuclei, Nikto, and Katana"
LABEL org.opencontainers.image.source="https://github.com/USERNAME/web-security-scanner"

# Instalar dependências básicas
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    unzip \
    perl \
    python3 \
    python3-pip \
    python3-venv \
    jq \
    chromium-browser \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar Go (necessário para Nuclei e Katana)
ENV GO_VERSION=1.22.1
RUN wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_VERSION}.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin:/root/go/bin

# Instalar Nuclei
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Instalar Katana
RUN go install github.com/projectdiscovery/katana/cmd/katana@latest

# Instalar Nikto
RUN git clone https://github.com/sullo/nikto.git /opt/nikto && \
    ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto

# Configurar ambiente Python para scripts de relatório
WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiar scripts
COPY src/run-scan.sh .
COPY src/generate_report.py .
RUN chmod +x run-scan.sh

# Atualizar templates do Nuclei
RUN nuclei -update-templates

ENTRYPOINT ["/app/run-scan.sh"]

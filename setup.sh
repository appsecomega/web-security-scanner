#!/bin/bash

# Setup local para o Web Security Scanner
# Este script facilita o build e teste local do repositório

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Setup Local do Web Security Scanner ===${NC}"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[!] Docker não encontrado. Por favor instale o Docker primeiro.${NC}"
    exit 1
fi

echo -e "${YELLOW}[*] Construindo a imagem Docker localmente...${NC}"
docker build -t web-security-scanner:local .

echo -e "${GREEN}[+] Imagem construída com sucesso!${NC}"
echo ""
echo -e "Para testar o scanner, execute:"
echo -e "${YELLOW}docker run --rm -v \$(pwd)/results:/app/output web-security-scanner:local -u https://example.com${NC}"
echo ""
echo -e "Ou use o docker-compose:"
echo -e "${YELLOW}TARGET=https://example.com docker-compose up${NC}"

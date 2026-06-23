#!/bin/bash

# Script de orquestração para scan de segurança

set -e

# Variáveis
TARGET=""
OUTPUT_DIR="/app/output"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Cores para logs CLI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função de ajuda
usage() {
    echo -e "${YELLOW}Uso: $0 -u <url_alvo> [-o <diretorio_saida>]${NC}"
    echo -e "Exemplo: $0 -u https://example.com -o /resultados"
    exit 1
}

# Parse argumentos
while getopts "u:o:h" opt; do
    case ${opt} in
        u ) TARGET=$OPTARG ;;
        o ) OUTPUT_DIR=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

if [ -z "$TARGET" ]; then
    echo -e "${RED}[!] Erro: URL alvo não especificada.${NC}"
    usage
fi

# Preparar diretório de saída
mkdir -p "$OUTPUT_DIR"
WORK_DIR="${OUTPUT_DIR}/scan_${TIMESTAMP}"
mkdir -p "$WORK_DIR"

echo -e "${GREEN}[+] Iniciando Scan de Segurança Web${NC}"
echo -e "${GREEN}[+] Alvo: ${TARGET}${NC}"
echo -e "${GREEN}[+] Diretório de trabalho: ${WORK_DIR}${NC}"
echo "---------------------------------------------------"

# 1. Katana (Spider)
echo -e "${YELLOW}[*] Fase 1: Executando Katana (Web Spider)...${NC}"
katana -u "$TARGET" -jc -hl -silent -o "$WORK_DIR/katana_endpoints.txt" -j | jq -c '.' > "$WORK_DIR/katana_results.json"
ENDPOINTS_COUNT=$(wc -l < "$WORK_DIR/katana_endpoints.txt" 2>/dev/null || echo 0)
echo -e "${GREEN}[+] Katana finalizado. Encontrados $ENDPOINTS_COUNT endpoints.${NC}"

# 2. Nikto
echo -e "${YELLOW}[*] Fase 2: Executando Nikto (Server Scanner)...${NC}"
# Extrair host para o Nikto
HOST=$(echo "$TARGET" | awk -F/ '{print $3}')
nikto -h "$HOST" -Format json -output "$WORK_DIR/nikto_results.json" > /dev/null 2>&1 || true
echo -e "${GREEN}[+] Nikto finalizado.${NC}"

# 3. Nuclei
echo -e "${YELLOW}[*] Fase 3: Executando Nuclei (Vulnerability Scanner)...${NC}"
# Usar os endpoints encontrados pelo Katana se houver, caso contrário usar o alvo direto
if [ "$ENDPOINTS_COUNT" -gt 0 ]; then
    nuclei -l "$WORK_DIR/katana_endpoints.txt" -j -o "$WORK_DIR/nuclei_results.json" -silent
else
    nuclei -u "$TARGET" -j -o "$WORK_DIR/nuclei_results.json" -silent
fi
echo -e "${GREEN}[+] Nuclei finalizado.${NC}"

# 4. Geração de Relatório
echo -e "${YELLOW}[*] Fase 4: Gerando Relatórios (HTML/PDF)...${NC}"
/app/venv/bin/python3 /app/generate_report.py \
    --target "$TARGET" \
    --katana "$WORK_DIR/katana_results.json" \
    --nikto "$WORK_DIR/nikto_results.json" \
    --nuclei "$WORK_DIR/nuclei_results.json" \
    --output "$WORK_DIR/report"

echo "---------------------------------------------------"
echo -e "${GREEN}[+] Scan Completo!${NC}"
echo -e "${GREEN}[+] Relatórios salvos em: ${WORK_DIR}${NC}"
echo -e "    - Relatório HTML: ${WORK_DIR}/report.html"
echo -e "    - Relatório PDF:  ${WORK_DIR}/report.pdf"
echo -e "    - Endpoints:      ${WORK_DIR}/katana_endpoints.txt"

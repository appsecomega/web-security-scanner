#!/usr/bin/env python3

import json
import argparse
import os
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML, CSS

# Template HTML para o relatório
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Segurança Web - {{ target }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .metadata {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .metadata-item {
            padding: 10px;
        }
        
        .metadata-item strong {
            color: #667eea;
            display: block;
            margin-bottom: 5px;
        }
        
        .section {
            margin-bottom: 40px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .section h2 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 4px solid #667eea;
        }
        
        .summary-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .summary-card .label {
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        table thead {
            background-color: #667eea;
            color: white;
        }
        
        table th, table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        table tbody tr:hover {
            background-color: #f0f0f0;
        }
        
        .severity-critical {
            background-color: #fee;
            color: #c00;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .severity-high {
            background-color: #fef3cd;
            color: #856404;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .severity-medium {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .severity-low {
            background-color: #d4edda;
            color: #155724;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }
        
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 Relatório de Segurança Web</h1>
            <p>Análise Completa de Vulnerabilidades e Configurações</p>
        </header>
        
        <div class="metadata">
            <div class="metadata-item">
                <strong>Alvo:</strong>
                {{ target }}
            </div>
            <div class="metadata-item">
                <strong>Data do Scan:</strong>
                {{ scan_date }}
            </div>
            <div class="metadata-item">
                <strong>Hora do Scan:</strong>
                {{ scan_time }}
            </div>
            <div class="metadata-item">
                <strong>Ferramentas Utilizadas:</strong>
                Nuclei, Nikto, Katana
            </div>
        </div>
        
        <!-- RESUMO EXECUTIVO -->
        <div class="section">
            <h2>📊 Resumo Executivo</h2>
            <div class="summary">
                <div class="summary-card">
                    <div class="number">{{ endpoints_count }}</div>
                    <div class="label">Endpoints Descobertos</div>
                </div>
                <div class="summary-card">
                    <div class="number">{{ nuclei_count }}</div>
                    <div class="label">Vulnerabilidades Nuclei</div>
                </div>
                <div class="summary-card">
                    <div class="number">{{ nikto_count }}</div>
                    <div class="label">Problemas Nikto</div>
                </div>
                <div class="summary-card">
                    <div class="number">{{ total_issues }}</div>
                    <div class="label">Total de Problemas</div>
                </div>
            </div>
        </div>
        
        <!-- ENDPOINTS DESCOBERTOS -->
        <div class="section">
            <h2>🔍 Endpoints Descobertos (Katana)</h2>
            {% if endpoints %}
                <p>Total de endpoints encontrados: <strong>{{ endpoints_count }}</strong></p>
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>Status</th>
                            <th>Content-Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for endpoint in endpoints[:50] %}
                        <tr>
                            <td><code>{{ endpoint.url }}</code></td>
                            <td>{{ endpoint.status_code | default('N/A') }}</td>
                            <td>{{ endpoint.content_type | default('N/A') }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% if endpoints_count > 50 %}
                <p style="margin-top: 10px; color: #666;"><em>Mostrando 50 de {{ endpoints_count }} endpoints. Veja o arquivo completo para a lista completa.</em></p>
                {% endif %}
            {% else %}
                <div class="empty-state">Nenhum endpoint foi descoberto</div>
            {% endif %}
        </div>
        
        <div class="page-break"></div>
        
        <!-- VULNERABILIDADES NUCLEI -->
        <div class="section">
            <h2>⚠️ Vulnerabilidades Detectadas (Nuclei)</h2>
            {% if nuclei_findings %}
                <p>Total de vulnerabilidades encontradas: <strong>{{ nuclei_count }}</strong></p>
                <table>
                    <thead>
                        <tr>
                            <th>Severidade</th>
                            <th>Template ID</th>
                            <th>Nome</th>
                            <th>URL Afetada</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for finding in nuclei_findings %}
                        <tr>
                            <td>
                                {% if finding.severity == 'critical' %}
                                    <span class="severity-critical">CRÍTICA</span>
                                {% elif finding.severity == 'high' %}
                                    <span class="severity-high">ALTA</span>
                                {% elif finding.severity == 'medium' %}
                                    <span class="severity-medium">MÉDIA</span>
                                {% else %}
                                    <span class="severity-low">BAIXA</span>
                                {% endif %}
                            </td>
                            <td><code>{{ finding.template_id }}</code></td>
                            <td>{{ finding.name }}</td>
                            <td><code>{{ finding.url }}</code></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="empty-state">Nenhuma vulnerabilidade foi detectada pelo Nuclei</div>
            {% endif %}
        </div>
        
        <!-- PROBLEMAS NIKTO -->
        <div class="section">
            <h2>🛡️ Problemas de Configuração (Nikto)</h2>
            {% if nikto_findings %}
                <p>Total de problemas encontrados: <strong>{{ nikto_count }}</strong></p>
                <table>
                    <thead>
                        <tr>
                            <th>Severidade</th>
                            <th>Descrição</th>
                            <th>Referência</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for finding in nikto_findings %}
                        <tr>
                            <td>
                                {% if finding.severity == 'CRITICAL' %}
                                    <span class="severity-critical">CRÍTICA</span>
                                {% elif finding.severity == 'HIGH' %}
                                    <span class="severity-high">ALTA</span>
                                {% elif finding.severity == 'MEDIUM' %}
                                    <span class="severity-medium">MÉDIA</span>
                                {% else %}
                                    <span class="severity-low">BAIXA</span>
                                {% endif %}
                            </td>
                            <td>{{ finding.description }}</td>
                            <td>{{ finding.reference | default('N/A') }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="empty-state">Nenhum problema foi detectado pelo Nikto</div>
            {% endif %}
        </div>
        
        <footer>
            <p>Relatório gerado automaticamente em {{ scan_date }} às {{ scan_time }}</p>
            <p>Ferramentas: Nuclei v3, Nikto v2.6.0+, Katana</p>
        </footer>
    </div>
</body>
</html>
"""

def parse_katana_results(file_path):
    """Parse resultados do Katana"""
    endpoints = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    endpoints.append({
                        'url': data.get('url', ''),
                        'status_code': data.get('status_code', ''),
                        'content_type': data.get('content_type', '')
                    })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return endpoints

def parse_nikto_results(file_path):
    """Parse resultados do Nikto"""
    findings = []
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Nikto retorna em estrutura específica
            if 'vulnerabilities' in data:
                for vuln in data['vulnerabilities']:
                    findings.append({
                        'severity': vuln.get('severity', 'LOW').upper(),
                        'description': vuln.get('title', ''),
                        'reference': vuln.get('id', '')
                    })
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return findings

def parse_nuclei_results(file_path):
    """Parse resultados do Nuclei"""
    findings = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    findings.append({
                        'severity': data.get('severity', 'info').lower(),
                        'template_id': data.get('template_id', ''),
                        'name': data.get('info', {}).get('name', ''),
                        'url': data.get('matched_at', '')
                    })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return findings

def generate_report(target, katana_file, nikto_file, nuclei_file, output_prefix):
    """Gera relatório HTML e PDF"""
    
    # Parse resultados
    endpoints = parse_katana_results(katana_file)
    nikto_findings = parse_nikto_results(nikto_file)
    nuclei_findings = parse_nuclei_results(nuclei_file)
    
    # Preparar dados para template
    now = datetime.now()
    context = {
        'target': target,
        'scan_date': now.strftime('%d/%m/%Y'),
        'scan_time': now.strftime('%H:%M:%S'),
        'endpoints': endpoints,
        'endpoints_count': len(endpoints),
        'nikto_findings': nikto_findings,
        'nikto_count': len(nikto_findings),
        'nuclei_findings': nuclei_findings,
        'nuclei_count': len(nuclei_findings),
        'total_issues': len(nikto_findings) + len(nuclei_findings)
    }
    
    # Renderizar template
    template = Template(HTML_TEMPLATE)
    html_content = template.render(**context)
    
    # Salvar HTML
    html_file = f"{output_prefix}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] Relatório HTML salvo: {html_file}")
    
    # Gerar PDF
    try:
        pdf_file = f"{output_prefix}.pdf"
        HTML(string=html_content).write_pdf(pdf_file)
        print(f"[+] Relatório PDF salvo: {pdf_file}")
    except Exception as e:
        print(f"[-] Erro ao gerar PDF: {e}")

def main():
    parser = argparse.ArgumentParser(description='Gera relatório de segurança web')
    parser.add_argument('--target', required=True, help='URL alvo do scan')
    parser.add_argument('--katana', required=True, help='Arquivo JSON de resultados do Katana')
    parser.add_argument('--nikto', required=True, help='Arquivo JSON de resultados do Nikto')
    parser.add_argument('--nuclei', required=True, help='Arquivo JSON de resultados do Nuclei')
    parser.add_argument('--output', required=True, help='Prefixo do arquivo de saída')
    
    args = parser.parse_args()
    
    generate_report(args.target, args.katana, args.nikto, args.nuclei, args.output)

if __name__ == '__main__':
    main()

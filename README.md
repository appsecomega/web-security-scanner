<div align="center">
  <h1>🛡️ Web Security Scanner</h1>
  <p><strong>Automated Web Security Scanner with Nuclei, Nikto, and Katana</strong></p>

  [![Build Status](https://img.shields.io/github/actions/workflow/status/USERNAME/web-security-scanner/docker-publish.yml?branch=main&style=for-the-badge)](https://github.com/USERNAME/web-security-scanner/actions)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
  [![Docker Pulls](https://img.shields.io/docker/pulls/USERNAME/web-security-scanner?style=for-the-badge)](https://hub.docker.com/r/USERNAME/web-security-scanner)
</div>

<br>

A fully automated, containerized web security scanning solution that orchestrates three specialized tools to provide a comprehensive analysis of your web application's attack surface, generating structured PDF and HTML reports.

## ✨ Features

- 🕷️ **Deep Crawling**: Uses Katana (with headless support for SPAs) to discover endpoints
- 🖥️ **Server Scanning**: Leverages Nikto to find misconfigurations and default files
- 🎯 **Vulnerability Scanning**: Uses Nuclei with 12,000+ community templates for CVEs
- 📊 **Beautiful Reports**: Automatically generates executive HTML and PDF reports
- 🐳 **Docker Ready**: Run anywhere with zero dependencies (just Docker)
- 🤖 **CI/CD Integration**: Easy to integrate into your existing pipelines

## 🚀 Quick Start

The easiest way to use the scanner is via Docker Compose or directly with `docker run`.

### Using Docker Run

```bash
# Create an output directory
mkdir -p $(pwd)/results

# Run the scanner against a target
docker run --rm -v $(pwd)/results:/app/output ghcr.io/USERNAME/web-security-scanner:latest -u https://example.com
```

### Using Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/USERNAME/web-security-scanner.git
cd web-security-scanner
```

2. Run the scan:
```bash
TARGET=https://example.com docker-compose up
```

## 📂 Output Structure

After the scan completes, you'll find the results in your output directory:

```
results/scan_YYYYMMDD_HHMMSS/
├── report.html              ← Interactive HTML report
├── report.pdf               ← Printable PDF report
├── katana_endpoints.txt     ← Discovered URLs
├── katana_results.json      ← Raw spider data (JSONL)
├── nikto_results.json       ← Raw server scan data (JSON)
└── nuclei_results.json      ← Raw vulnerability data (JSONL)
```

## 🛠️ Architecture

The container orchestrates the tools in an optimized pipeline:

1. **Katana** runs first to discover all possible endpoints, forms, and JavaScript files.
2. **Nikto** runs in parallel against the base host to find server-level misconfigurations.
3. **Nuclei** consumes Katana's output to perform targeted vulnerability scanning.
4. **Python Generator** aggregates all JSON outputs into final HTML/PDF reports.

## 💻 Local Development

To build the image locally:

```bash
git clone https://github.com/USERNAME/web-security-scanner.git
cd web-security-scanner
docker build -t web-security-scanner:local .
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*Note: This container bundles Nikto (GPL-2.0), Katana (MIT), and Nuclei (MIT). Ensure you comply with their respective licenses when distributing.*

## ⚠️ Disclaimer

This tool is designed for security professionals and system administrators to test their own systems. **Do not use this tool against targets you do not have explicit permission to test.** The authors are not responsible for any misuse or damage caused by this program.

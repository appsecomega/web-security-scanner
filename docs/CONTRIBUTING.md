# Contributing to Web Security Scanner

First off, thank you for considering contributing to Web Security Scanner! It's people like you that make open source such a great community.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](../../issues) first. If you don't see it there, feel free to open a new issue.

## Pull Requests

When you're ready to contribute code, please follow these steps:

1. **Fork the repo** and create your branch from `main`.
2. **If you've added code** that should be tested, add tests.
3. **If you've changed APIs**, update the documentation.
4. **Ensure the test suite passes**.
5. **Make sure your code lints**.

### Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/web-security-scanner.git
   cd web-security-scanner
   ```

2. Build the Docker image locally to test your changes:
   ```bash
   docker build -t web-security-scanner:dev .
   ```

3. Run a test scan:
   ```bash
   docker run --rm -v $(pwd)/test-output:/app/output web-security-scanner:dev -u http://example.com
   ```

### Changing the Report Template

If you want to modify the HTML/PDF report:

1. Edit `src/generate_report.py`
2. Look for the `HTML_TEMPLATE` variable
3. The template uses Jinja2 syntax
4. Rebuild the Docker image to test your changes

### Changing the Orchestration Script

If you want to modify how the tools run:

1. Edit `src/run-scan.sh`
2. Ensure you handle errors gracefully (use `|| true` for non-critical failures)
3. Ensure JSON outputs are properly formatted for the report generator
4. Run `shellcheck src/run-scan.sh` to verify syntax

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

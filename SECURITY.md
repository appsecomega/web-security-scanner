# Security Policy

## Supported Versions

Currently, only the latest version of the Web Security Scanner on the `main` branch is supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please DO NOT open a public issue.

Instead, please send an email to the maintainer or use GitHub's private vulnerability reporting feature if enabled on the repository.

Please include the following information in your report:
- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

We will try to acknowledge receipt of your vulnerability report within 48 hours and strive to send you regular updates about our progress.

## Base Image Security

This container is built on top of `ubuntu:24.04`. We rely on GitHub Actions Dependabot and regular rebuilds to ensure OS-level vulnerabilities are patched. The `docker-publish.yml` workflow is designed to rebuild the image periodically or on pushes to `main`.

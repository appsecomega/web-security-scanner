# GitHub Actions Setup Guide

Este guia explica como configurar o GitHub Actions para publicar automaticamente a imagem Docker no Docker Hub e GitHub Container Registry (GHCR).

## Pré-requisitos

1. Uma conta no [Docker Hub](https://hub.docker.com/)
2. Um repositório GitHub criado (vazio ou com os arquivos)
3. Acesso às configurações do repositório GitHub

## Passo 1: Criar Token no Docker Hub

1. Faça login no [Docker Hub](https://hub.docker.com/)
2. Vá para **Account Settings** → **Security** → **New Access Token**
3. Dê um nome ao token (ex: `github-actions`)
4. Selecione as permissões: **Read, Write, Delete**
5. Clique em **Generate**
6. **Copie o token** (você não poderá vê-lo novamente)

## Passo 2: Adicionar Secrets ao GitHub

1. Vá para seu repositório no GitHub
2. Clique em **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**

Adicione os seguintes secrets:

| Nome | Valor |
|------|-------|
| `DOCKERHUB_USERNAME` | Seu username do Docker Hub |
| `DOCKERHUB_TOKEN` | Token gerado no Passo 1 |

## Passo 3: Verificar os Workflows

Os workflows estão em `.github/workflows/`:

- **docker-publish.yml**: Constrói e publica a imagem em Docker Hub e GHCR
- **test.yml**: Executa testes automaticamente

### O que acontece automaticamente:

1. **Em cada push para `main`**:
   - A imagem é construída
   - A imagem é publicada como `latest` em ambos os registros
   - Testes são executados

2. **Em cada tag (ex: `v1.0.0`)**:
   - A imagem é publicada com a tag de versão
   - Exemplo: `ghcr.io/USERNAME/web-security-scanner:v1.0.0`

3. **Em Pull Requests**:
   - A imagem é construída para teste
   - Testes são executados
   - A imagem NÃO é publicada

## Passo 4: Fazer Push para GitHub

Após adicionar os secrets, faça push dos arquivos:

```bash
git init
git add .
git commit -m "Initial commit: Web Security Scanner"
git branch -M main
git remote add origin https://github.com/USERNAME/web-security-scanner.git
git push -u origin main
```

## Passo 5: Monitorar o Build

1. Vá para a aba **Actions** do seu repositório
2. Você verá o workflow `Docker Build and Publish` em execução
3. Clique nele para ver os logs detalhados

## Passo 6: Verificar as Imagens Publicadas

### Docker Hub

1. Vá para `https://hub.docker.com/r/USERNAME/web-security-scanner`
2. Você deve ver a imagem com a tag `latest`

### GitHub Container Registry

1. Vá para `https://github.com/USERNAME/web-security-scanner/pkgs/container/web-security-scanner`
2. Você deve ver a imagem com a tag `latest`

## Usar a Imagem Publicada

Após o build bem-sucedido, você pode usar a imagem:

```bash
# Do Docker Hub
docker run --rm -v $(pwd)/results:/app/output USERNAME/web-security-scanner:latest -u https://example.com

# Do GitHub Container Registry
docker run --rm -v $(pwd)/results:/app/output ghcr.io/USERNAME/web-security-scanner:latest -u https://example.com
```

## Troubleshooting

### Build falha com "authentication required"

Verifique se os secrets `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN` estão configurados corretamente.

### Imagem não aparece no Docker Hub

1. Verifique se o workflow completou com sucesso (aba Actions)
2. Verifique se o token do Docker Hub tem permissões de escrita
3. Tente fazer push novamente

### Erro "permission denied" no GHCR

O GitHub cria automaticamente o repositório no GHCR. Se receber erro de permissão, verifique se o `GITHUB_TOKEN` tem as permissões corretas (deve estar automático).

## Próximos Passos

1. **Criar uma Release**: Crie uma tag (ex: `v1.0.0`) para criar uma release no GitHub
2. **Adicionar Badges**: Adicione badges ao README.md para mostrar o status dos builds
3. **Documentar Versões**: Crie um CHANGELOG.md para rastrear mudanças

## Recursos Adicionais

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

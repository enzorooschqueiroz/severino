# Passo 1: API Básica com Health Check

Vamos começar criando uma API Flask simples com endpoint de health check e configuração Docker.

## 🎯 Objetivo deste Passo

Criar a base da aplicação com:
- ✅ Flask app básica
- ✅ Endpoint `/health` funcionando 
- ✅ Configuração Docker completa
- ✅ Docker Compose para dev e produção
- ✅ Makefile para facilitar comandos
- ✅ Logging configurado
- ✅ Error handlers básicos

## 📁 Estrutura do Projeto

Crie esta estrutura de pastas:

```
auth-service/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── docker-compose.yml    # Produção
├── docker-compose.dev.yml # Desenvolvimento  
├── .env                  # Variáveis de ambiente
├── .env.example          # Exemplo de variáveis
├── Makefile             # Comandos úteis
├── .dockerignore        # Arquivos ignorados pelo Docker
├── .gitignore          # Arquivos ignorados pelo Git
└── logs/               # Diretório de logs (criar vazio)
```

## 🚀 Como Testar

### 1. Configurar Ambiente

```bash
# Clone ou crie o diretório
mkdir auth-service && cd auth-service

# Copie todos os arquivos dos artifacts acima
# Crie o diretório de logs
mkdir logs

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações
```

### 2. Executar em Desenvolvimento

```bash
# Opção 1: Com Make (recomendado)
make run-dev

# Opção 2: Docker Compose direto
docker-compose -f docker-compose.dev.yml up --build

# Ver logs em tempo real
make logs
```

### 3. Testar os Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Deve retornar:
{
  "status": "healthy",
  "timestamp": "2025-07-21T...",
  "service": "auth-api", 
  "version": "1.0.0"
}

# Endpoint raiz
curl http://localhost:5000/

# Teste 404
curl http://localhost:5000/inexistente
```

### 4. Executar em Produção

```bash
# Subir em modo produção
make run-prod

# Ou manualmente
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f auth-service
```

## 🔧 Comandos Úteis

```bash
# Ver todos os comandos disponíveis
make help

# Build da imagem
make build

# Parar containers
make stop

# Limpar tudo
make clean

# Shell do container
make shell

# Teste rápido
make test
```

## 📝 Arquivos Auxiliares

Crie estes arquivos também:

### `.dockerignore`
```
.git
.gitignore
README.md
Makefile
.env
*.pyc
__pycache__
.pytest_cache
.coverage
*.log
```

### `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
.env

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## ✅ Validação do Passo 1

Confirme que tudo está funcionando:

1. **Container sobe sem erro**: `docker-compose ps` mostra status "Up"
2. **Health check funciona**: `curl http://localhost:5000/health` retorna 200
3. **Logs aparecem**: `make logs` mostra logs da aplicação
4. **Desenvolvimento funciona**: Hot reload no modo dev
5. **Produção funciona**: Gunicorn em produção

## 🎯 Próximo Passo

Após validar que tudo está funcionando, vamos para o **Passo 2**:
- Adicionar conexão com Supabase
- Criar modelos de dados
- Implementar repositório básico

## 🐛 Troubleshooting

### Port já está em uso
```bash
# Ver o que está usando a porta 5000
lsof -i :5000

# Matar processo se necessário
sudo kill -9 PID

# Ou usar outra porta
PORT=5001 make run-dev
```

### Permission denied no Docker
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Logout e login novamente
```

### Container não encontra arquivos
```bash
# Verificar .dockerignore
# Certificar que app.py está no diretório

# Rebuild completo
make clean
make build
```

Está pronto para continuar? Confirme que o health check está funcionando e podemos seguir para o Passo 2!
# 🚀 Guia de Início Rápido

Começe com o Python CRUD em 5 minutos!

## ⚡ Pré-requisitos

- Python 3.13 ou superior
- PostgreSQL rodando
- pip atualizado

## 📦 Passo 1: Configurar Ambiente

### Windows PowerShell
```powershell
# Criar ambiente virtual
py -3.13 -m venv .venv

# Ativar ambiente virtual
.venv/Scripts/activate

# Instalar dependências
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Linux/Mac
```bash
# Criar ambiente virtual
python3.13 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## 🔧 Passo 2: Configurar Banco de Dados

### 1. Criar banco de dados PostgreSQL
```sql
CREATE DATABASE python_crud_db ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C';
```

### 2. Atualizar `.env`
```bash
# Copiar exemplo
cp .env.example .env

# Editar .env com suas credenciais PostgreSQL
# DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/python_crud_db
```

## 🎯 Passo 3: Iniciar a Aplicação

```bash
python -m app.main
```

Você verá:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **Aplicação rodando!**

## 👤 Passo 4: Criar Primeiro Usuário

Em outro terminal:

```bash
curl -X POST http://127.0.0.1:9001/admin/init/create-first-user \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "Admin@123456",
    "full_name": "Administrator"
  }'
```

Resposta esperada:
```json
{
  "code": 201,
  "status": "Created",
  "message": "First user created successfully",
  "validationErrors": {
    "id": "uuid-do-usuario",
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Administrator"
  }
}
```

## 🔑 Passo 5: Fazer Login

```bash
curl -X POST http://127.0.0.1:9001/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123456"
  }'
```

Resposta (copie o `access_token`):
```json
{
  "code": 200,
  "status": "Ok",
  "validationErrors": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
}
```

## 🧪 Passo 6: Testar Endpoints

```bash
# Salve o token em uma variável
TOKEN="seu_token_aqui"

# Listar usuários
curl -X GET http://127.0.0.1:9001/user/ \
  -H "Authorization: Bearer $TOKEN"

# Criar novo usuário
curl -X POST http://127.0.0.1:9001/user/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@example.com",
    "password": "Joao@123456",
    "full_name": "João Silva"
  }'

# Listar roles
curl -X GET http://127.0.0.1:9001/role/ \
  -H "Authorization: Bearer $TOKEN"

# Listar permissões
curl -X GET http://127.0.0.1:9001/permissions/ \
  -H "Authorization: Bearer $TOKEN"
```

## 🌐 Passo 7: Acessar Documentação Interativa

Abra seu navegador:
- **Swagger UI**: http://127.0.0.1:9001/docs
- **ReDoc**: http://127.0.0.1:9001/redoc

Aqui você pode testar todos os endpoints diretamente!

## 🧪 Bonus: Executar Script de Teste

```bash
python test_endpoints.py
```

Isso vai validar todos os endpoints automaticamente:
```
✓ Testing GET /health
  Status: 200
  Response: {'status': 'healthy'}

✓ Testing POST /admin/init/create-first-user
  Status: 201 (ou 403 se já existe usuário)

✓ Testing POST /user/login
  Status: 200

✓ Testing GET /user/ (with authentication)
  Status: 200

✓ Testing GET /permissions/ (with authentication)
  Status: 200

Test Results Summary
Health Check............................... ✅ PASS
...
Total: 6/6 tests passed
```

## 📚 Próximos Passos

1. Leia [ENDPOINTS.md](./ENDPOINTS.md) para documentação completa
2. Consulte [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) se tiver problemas
3. Confira [README.md](./README.md) para informações do projeto

## ✅ Checklist Rápido

- [ ] Python 3.13+ instalado
- [ ] PostgreSQL rodando
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas
- [ ] `.env` configurado com banco de dados correto
- [ ] Aplicação inicia: `python -m app.main`
- [ ] Primeiro usuário criado via `/admin/init/create-first-user`
- [ ] Login funciona e retorna token JWT
- [ ] Endpoints funcionam com o token

## 🆘 Problemas Comuns

### ❌ "Database connection failed"
```bash
# Verifique se PostgreSQL está rodando
# Verifique DATABASE_URL no .env
# Verifique se o banco existe
```

### ❌ "Cannot connect to server"
```bash
# Verifique se a porta 9001 não está em uso
# Verifique se Uvicorn iniciou corretamente
```

### ❌ "Invalid credentials"
```bash
# Certifique-se de usar username: "admin" e password: "Admin@123456"
# Ou crie um novo usuário primeiro
```

Veja [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) para mais detalhes!

## 📞 Suporte

- Documentação: [ENDPOINTS.md](./ENDPOINTS.md)
- Troubleshooting: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- FastAPI Docs: http://127.0.0.1:9001/docs (quando rodando)

---

**Pronto para começar? Execute: `python -m app.main` 🚀**

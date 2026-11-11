# 🔧 Troubleshooting - Por que você não conseguia acessar os endpoints

## Problemas Identificados

### 1. ❌ **CORS Configurado Incorretamente**
**Problema**: O CORS estava limitado a apenas o método `POST`
```python
# ❌ ANTES
allow_methods=["POST"],
```

**Solução**: Permitir todos os métodos HTTP
```python
# ✅ DEPOIS
allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
```

**Impacto**: Você receberia erros CORS ao tentar fazer requisições GET, PUT, DELETE, etc.

---

### 2. ❌ **Falta de Ponto de Entrada para `python -m app.main`**
**Problema**: O arquivo `app/main.py` não tinha um bloco `if __name__ == "__main__":`

**Solução**: Adicionado ponto de entrada Uvicorn
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Impacto**: O comando `python -m app.main` não funcionava conforme esperado.

---

### 3. ❌ **Autenticação JWT Obrigatória em Todos os Endpoints**
**Problema**: Endpoints de criação de usuário, roles e permissões requeriam `Depends(ServiceUser.get_current_user)`, mas não havia forma de obter um token sem fazer login primeiro.

```python
# ❌ ANTES - Ciclo infinito de dependências
@user.post("/")
async def create_user(
    request: DTOUserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(ServiceUser.get_current_user),  # ❌ Requer autenticação
):
    ...
```

**Solução**: Adicionado endpoint de inicialização sem autenticação
```python
# ✅ DEPOIS - Endpoint público para criar primeiro usuário
@admin.post("/init/create-first-user", status_code=status.HTTP_201_CREATED)
async def create_first_user(request: DTOUserCreate, db: Session = Depends(get_db)):
    """Create the first admin user (no authentication required)"""
    ...
```

**Impacto**: Impossível bootstrap do sistema (criar o primeiro usuário).

---

### 4. ❌ **Banco de Dados Não Configurado Adequadamente**
**Problema**: Valor `DATABASE_URL` incompleto no `.env`
```
DATABASE_URL=postgres://localhost:5432/meu_banco_db  # ❌ Falta driver e credenciais
```

**Solução**: Formato correto do PostgreSQL
```
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
```

**Impacto**: Conexão ao banco falha, todos os endpoints retornam erro 500.

---

### 5. ❌ **Documentação Incompleta**
**Problema**: README.md não listava os endpoints disponíveis e como acessá-los.

**Solução**: Criado arquivo `ENDPOINTS.md` com documentação completa.

**Impacto**: Usuários não sabiam como usar a API.

---

## ✅ Soluções Implementadas

### Alterações no Código

1. **app/main.py**
   - ✅ Adicionado bloco `if __name__ == "__main__":` com Uvicorn
   - ✅ CORS atualizado para aceitar todos os métodos HTTP

2. **app/routers/admin.py**
   - ✅ Adicionado endpoint `POST /admin/init/create-first-user` (sem autenticação)
   - ✅ Endpoint só funciona se não houver usuários no banco

### Documentação Criada

1. **ENDPOINTS.md** (novo arquivo)
   - Documentação completa de todos os endpoints
   - Exemplos com cURL
   - Guia de troubleshooting

2. **test_endpoints.py** (novo arquivo)
   - Script Python para testar todos os endpoints
   - Valida fluxo completo (health → criar usuário → login → listar)

3. **README.md** (atualizado)
   - Lista de endpoints principais
   - Referência para `ENDPOINTS.md`

---

## 🚀 Fluxo de Uso Correto

### 1️⃣ Primeira Vez - Inicializar o Sistema

```bash
# Terminal 1: Inicie o servidor
python -m app.main
# Servidor rodando em http://127.0.0.1:9001

# Terminal 2: Crie o primeiro usuário
curl -X POST http://127.0.0.1:9001/admin/init/create-first-user \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "Admin@123456",
    "full_name": "Administrator"
  }'
```

### 2️⃣ Fazer Login e Obter Token

```bash
curl -X POST http://127.0.0.1:9001/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123456"
  }'

# Resposta contém o token JWT
# Copie o valor de "access_token"
```

### 3️⃣ Usar os Endpoints com Autenticação

```bash
TOKEN="seu_token_jwt_aqui"

# Listar usuários
curl -X GET http://127.0.0.1:9001/user/ \
  -H "Authorization: Bearer $TOKEN"

# Criar novo usuário
curl -X POST http://127.0.0.1:9001/user/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novo_user",
    "email": "novo@example.com",
    "password": "SecurePass123!",
    "full_name": "Novo Usuário"
  }'
```

---

## 🧪 Teste Automático

Execute o script de teste para validar tudo:

```bash
python test_endpoints.py
```

Isso vai:
1. ✅ Verificar saúde da API
2. ✅ Criar primeiro usuário
3. ✅ Fazer login
4. ✅ Listar usuários
5. ✅ Listar permissões

---

## 📋 Checklist de Configuração

- [ ] PostgreSQL está instalado e rodando
- [ ] Banco de dados foi criado
- [ ] `.env` contém `DATABASE_URL` correto
- [ ] `.env` contém `JWT_SECRET_KEY` configurado
- [ ] Dependências foram instaladas: `python -m pip install -e ".[dev]"`
- [ ] Aplicação inicia: `python -m app.main`
- [ ] Endpoint de saúde responde: `GET /health`
- [ ] Primeiro usuário foi criado: `POST /admin/init/create-first-user`
- [ ] Login funciona: `POST /user/login`
- [ ] Endpoints autenticados funcionam com o token JWT

---

## 🔗 Links Úteis

- [Documentação Completa de Endpoints](./ENDPOINTS.md)
- [FastAPI Docs](http://127.0.0.1:9001/docs) ← Acesse quando a app estiver rodando
- [Arquivo .env.example](./.env.example)

---

## ⚡ Resumo Rápido

| Problema | Causa | Solução |
|----------|-------|---------|
| `CORS error` ao chamar endpoints | Métodos HTTP não permitidos | ✅ Corrigido no CORS middleware |
| `python -m app.main` não funciona | Sem ponto de entrada | ✅ Adicionado `if __name__ == "__main__"` |
| Não consegue criar primeiro usuário | Autenticação obrigatória | ✅ Criado endpoint `/admin/init/create-first-user` |
| Endpoints retornam erro 500 | Banco de dados desconectado | ✅ Verifique `DATABASE_URL` no `.env` |
| Não sabe quais endpoints existem | Documentação faltando | ✅ Criado `ENDPOINTS.md` |

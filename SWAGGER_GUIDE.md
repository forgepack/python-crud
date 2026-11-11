# 📖 Swagger/OpenAPI Guide

A aplicação FastAPI inclui documentação interativa automática via Swagger UI e ReDoc. Nenhuma configuração adicional é necessária!

## 🚀 Como Acessar

### 1. Inicie a Aplicação
```bash
python -m app.main
```

### 2. Abra o Swagger UI
Navegue até: **http://127.0.0.1:9001/docs**

Você verá uma interface interativa com todos os endpoints da API.

### 3. Alternativa - ReDoc
Para uma documentação alternativa (somente leitura): **http://127.0.0.1:9001/redoc**

---

## 🎯 Usando o Swagger UI

### Passo 1: Explorar Endpoints

A página do Swagger mostra todos os endpoints organizados por categoria:

- 🟦 **Health** - Verificação de saúde
- 🟩 **Admin** - Inicialização do sistema
- 🟥 **Users** - Gerenciamento de usuários
- 🟦 **Roles** - Gerenciamento de funções
- 🟨 **Permissions** - Gerenciamento de permissões

### Passo 2: Testar um Endpoint

#### Exemplo 1: Health Check (sem autenticação)
1. Clique em `GET /health`
2. Clique no botão **"Try it out"**
3. Clique em **"Execute"**
4. Veja a resposta no console

**Resposta esperada:**
```json
{
  "status": "healthy"
}
```

#### Exemplo 2: Criar Primeiro Usuário (sem autenticação)
1. Clique em `POST /admin/init/create-first-user`
2. Clique em **"Try it out"**
3. Modifique o Request Body:
   ```json
   {
     "username": "admin",
     "email": "admin@example.com",
     "password": "Admin@123456",
     "full_name": "Administrator"
   }
   ```
4. Clique em **"Execute"**
5. Veja a resposta com o usuário criado

**Resposta esperada (201):**
```json
{
  "code": 201,
  "status": "Created",
  "message": "First user created successfully",
  "validationErrors": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Administrator"
  }
}
```

#### Exemplo 3: Fazer Login (obter token JWT)
1. Clique em `POST /user/login`
2. Clique em **"Try it out"**
3. Modifique o Request Body:
   ```json
   {
     "username": "admin",
     "password": "Admin@123456"
   }
   ```
4. Clique em **"Execute"**
5. Copie o valor de `access_token` da resposta

**Resposta esperada (200):**
```json
{
  "code": 200,
  "status": "Ok",
  "message": "Ok",
  "validationErrors": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

#### Exemplo 4: Usar Token em Endpoints Autenticados

1. Clique em `GET /user/` (listar usuários)
2. Clique em **"Try it out"**
3. **Importante:** Clique no botão 🔒 **"Authorize"** no topo da página
4. Selecione **"BearerAuth"**
5. Cole o token obtido no passo anterior:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
6. Clique em **"Authorize"**
7. Agora clique em **"Execute"** no endpoint
8. Veja a lista de usuários retornada

**Resposta esperada (200):**
```json
{
  "code": 200,
  "status": "Ok",
  "message": "Finded all",
  "validationErrors": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Administrator"
    }
  ]
}
```

---

## 🔐 Autenticação via Bearer Token

### Como Funciona

1. Endpoints **públicos** (sem 🔒) não requerem autenticação
2. Endpoints **autenticados** (com 🔒) requerem um token JWT no header

### Adicionando Token via Swagger

#### Método 1: Usar o Botão "Authorize"
1. Clique em **"Authorize"** (ícone 🔒 no topo)
2. Selecione **"BearerAuth"**
3. Cole seu token
4. Clique em **"Authorize"**
5. Agora todos os endpoints autenticados funcionarão

#### Método 2: Manual (se o Método 1 não funcionar)
1. Ao clicar em "Try it out", procure por um campo **"Authorization"**
2. Insira: `Bearer seu_token_aqui`

---

## 📋 Guia de Endpoints Principais

### 🟢 Públicos (sem autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Verificar saúde |
| GET | `/` | Home |
| POST | `/user/login` | Fazer login |
| POST | `/admin/init/create-first-user` | Criar primeiro usuário |

### 🔵 Autenticados (com token)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/user/` | Criar usuário |
| GET | `/user/` | Listar usuários |
| GET | `/user/{id}` | Obter usuário |
| PUT | `/user/` | Atualizar usuário |
| DELETE | `/user/{id}` | Deletar usuário |
| POST | `/role/` | Criar role |
| GET | `/role/` | Listar roles |
| GET | `/permissions/` | Listar permissões |

---

## 💡 Dicas Úteis

### 1. **Expandir/Colapsar Seções**
Clique no nome da seção (ex: "Users") para expandir/colapsar todos os endpoints daquela tag.

### 2. **Ver Exemplo de Schema**
Clique em um tipo de schema para ver a estrutura dos dados:
```
DTOUserCreate {
  username (string)
  email (string)
  password (string)
  full_name (string)
}
```

### 3. **Copiar curl do Swagger**
No topo de cada resposta de teste, há um ícone que permite copiar o comando curl equivalente.

### 4. **Ver Headers da Resposta**
Role para baixo na seção de resposta para ver headers HTTP retornados:
```
Content-Type: application/json
X-Process-Time: 0.123
```

### 5. **Testar com Valores Diferentes**
Cada vez que clica em "Try it out", o Swagger mantém os valores anteriores. Modifique conforme necessário para testar diferentes cenários.

---

## 🔄 Fluxo Completo de Teste

Siga estes passos para testar a aplicação completa via Swagger:

### 1️⃣ Verificar Saúde
```
GET /health
→ Resposta: {"status": "healthy"}
```

### 2️⃣ Criar Primeiro Usuário
```
POST /admin/init/create-first-user
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "Admin@123456",
  "full_name": "Administrator"
}
→ Resposta: 201 Created com user object
```

### 3️⃣ Fazer Login
```
POST /user/login
{
  "username": "admin",
  "password": "Admin@123456"
}
→ Resposta: 200 OK com access_token
```

### 4️⃣ Autorizar (copiar token)
```
Clique em "Authorize" no topo
Cole o access_token
Clique em "Authorize"
```

### 5️⃣ Listar Usuários
```
GET /user/
→ Resposta: 200 OK com lista de usuários
```

### 6️⃣ Criar Novo Usuário
```
POST /user/
{
  "username": "joao",
  "email": "joao@example.com",
  "password": "Joao@123456",
  "full_name": "João Silva"
}
→ Resposta: 201 Created
```

### 7️⃣ Atualizar Usuário
```
PUT /user/
{
  "id": "user-uuid-aqui",
  "email": "novo@example.com",
  "full_name": "João Silva Novo"
}
→ Resposta: 202 Accepted
```

### 8️⃣ Obter Usuário por ID
```
GET /user/{id}
→ Resposta: 200 OK com dados do usuário
```

### 9️⃣ Deletar Usuário
```
DELETE /user/{id}
→ Resposta: 204 No Content
```

---

## 🐛 Troubleshooting

### ❌ Erro "401 Unauthorized"
**Causa:** Token ausente ou inválido
**Solução:**
1. Clique em "Authorize"
2. Verifique se o token foi colado corretamente
3. Verifique se não está expirado (padrão: 30 minutos)
4. Faça login novamente para obter novo token

### ❌ Erro "403 Forbidden"
**Causa:** Usuário já existe
**Solução:**
- `/admin/init/create-first-user` só funciona quando o banco está vazio
- Use `/user/login` para autenticar com usuário existente

### ❌ Erro "Connection refused"
**Causa:** Aplicação não está rodando
**Solução:**
```bash
python -m app.main
```

### ❌ Swagger UI não carrega
**Causa:** Aplicação rodando em porta diferente
**Solução:**
- Verifique `.env` para `UVICORN_PORT`
- Acesse `http://127.0.0.1:<porta>/docs`

---

## 📚 Recursos Adicionais

- **OpenAPI Spec (JSON)**: http://127.0.0.1:9001/openapi.json
- **ReDoc (alternativa)**: http://127.0.0.1:9001/redoc
- **FastAPI Docs**: https://fastapi.tiangolo.com/features/#automatic-docs
- **Swagger Docs**: https://swagger.io/tools/swagger-ui/

---

## ✅ Checklist de Teste

- [ ] Acessei http://127.0.0.1:9001/docs
- [ ] Testei GET /health
- [ ] Criei primeiro usuário via POST /admin/init/create-first-user
- [ ] Fiz login e obtive token via POST /user/login
- [ ] Autorizei via botão "Authorize"
- [ ] Testei GET /user/ com autenticação
- [ ] Criei novo usuário via POST /user/
- [ ] Atualizei usuário via PUT /user/
- [ ] Consultei usuário via GET /user/{id}
- [ ] Deletei usuário via DELETE /user/{id}
- [ ] Testei endpoints de roles
- [ ] Testei endpoints de permissões

---

**Documentação completa sempre disponível em: http://127.0.0.1:9001/docs**

Bom teste! 🚀

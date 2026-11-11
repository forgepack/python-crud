# 📚 API Endpoints - Python CRUD

Esta é uma aplicação FastAPI para gerenciar **Users, Roles e Permissions** (Usuários, Funções e Permissões).

## 🚀 Começando

### 1. Inicie a Aplicação

```bash
python -m app.main
```

A aplicação estará disponível em `http://127.0.0.1:9001` (confira a porta no `.env`)

### 2. Acesse a Documentação Interativa

- **Swagger UI**: http://127.0.0.1:9001/docs
- **ReDoc**: http://127.0.0.1:9001/redoc

## ⚙️ Configuração Pré-requisitos

### Variáveis de Ambiente (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
DATABASE_SCHEMA=public
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Banco de Dados
Certifique-se de que o PostgreSQL está rodando e que o banco de dados existe.

## 📋 Endpoints Disponíveis

### 🔓 Endpoints Públicos (Sem Autenticação)

#### Health Check
```bash
GET http://127.0.0.1:9001/health
```
**Response:**
```json
{"status": "healthy"}
```

#### Home
```bash
GET http://127.0.0.1:9001/
```
**Response:**
```json
{"message": "Welcome Fast API by Gadelha TI", "status": "success"}
```

#### Login (Obter Token JWT)
```bash
POST http://127.0.0.1:9001/user/login
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Response:**
```json
{
  "code": 200,
  "status": "Ok",
  "message": "Ok",
  "validationErrors": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
}
```

#### Criar Primeiro Usuário Admin (Inicialização)
```bash
POST http://127.0.0.1:9001/admin/init/create-first-user
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@example.com",
  "password": "SecurePassword123!",
  "full_name": "Administrator"
}
```

**⚠️ Nota**: Este endpoint só funciona se o banco está vazio (sem usuários).

### 🔐 Endpoints Autenticados (Requer JWT Token)

Todos os endpoints abaixo requerem o header:
```
Authorization: Bearer <seu_token_jwt>
```

#### Listar Usuários
```bash
GET http://127.0.0.1:9001/user/?page=1&limit=20
Authorization: Bearer <token>
```

#### Criar Novo Usuário
```bash
POST http://127.0.0.1:9001/user/
Content-Type: application/json
Authorization: Bearer <token>

{
  "username": "novo_usuario",
  "email": "novo@example.com",
  "password": "SecurePassword123!",
  "full_name": "Novo Usuário"
}
```

#### Obter Usuário por ID
```bash
GET http://127.0.0.1:9001/user/{user_id}
Authorization: Bearer <token>
```

#### Atualizar Usuário
```bash
PUT http://127.0.0.1:9001/user/
Content-Type: application/json
Authorization: Bearer <token>

{
  "id": "uuid-do-usuario",
  "full_name": "Novo Nome",
  "email": "novo@example.com"
}
```

#### Deletar Usuário
```bash
DELETE http://127.0.0.1:9001/user/{user_id}
Authorization: Bearer <token>
```

---

### 👥 Endpoints de Roles (Funções)

#### Listar Roles
```bash
GET http://127.0.0.1:9001/role/?page=1&limit=20
Authorization: Bearer <token>
```

#### Criar Role
```bash
POST http://127.0.0.1:9001/role/
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Admin",
  "description": "Administrator role"
}
```

#### Obter Role por ID
```bash
GET http://127.0.0.1:9001/role/{role_id}
Authorization: Bearer <token>
```

#### Atualizar Role
```bash
PUT http://127.0.0.1:9001/role/
Content-Type: application/json
Authorization: Bearer <token>

{
  "id": "uuid-da-role",
  "name": "SuperAdmin",
  "description": "Super Administrator role"
}
```

#### Deletar Role
```bash
DELETE http://127.0.0.1:9001/role/{role_id}
Authorization: Bearer <token>
```

#### Atribuir Permissões a uma Role
```bash
PATCH http://127.0.0.1:9001/role/{role_id}/permissions
Content-Type: application/json
Authorization: Bearer <token>

{
  "permission_ids": ["uuid-permission-1", "uuid-permission-2"]
}
```

---

### 🔑 Endpoints de Permissions (Permissões)

#### Listar Permissões
```bash
GET http://127.0.0.1:9001/permissions/?page=1&limit=20
Authorization: Bearer <token>
```

#### Obter Permissão por ID
```bash
GET http://127.0.0.1:9001/permissions/{permission_id}
Authorization: Bearer <token>
```

#### Listar Permissões por Ação
```bash
GET http://127.0.0.1:9001/permissions/by-action/{action}
Authorization: Bearer <token>
```

Valores válidos para `action`: `CREATE`, `READ`, `UPDATE`, `DELETE`, `EXECUTE`

#### Sincronizar Permissões com Enum
```bash
POST http://127.0.0.1:9001/permissions/sync
Authorization: Bearer <token>
```

#### Deletar Permissão
```bash
DELETE http://127.0.0.1:9001/permissions/{permission_id}
Authorization: Bearer <token>
```

#### Soft Delete (Marcar como Deletado)
```bash
PATCH http://127.0.0.1:9001/permissions/{permission_id}/soft-delete
Authorization: Bearer <token>
```

#### Restaurar Permissão
```bash
PATCH http://127.0.0.1:9001/permissions/{permission_id}/restore
Authorization: Bearer <token>
```

---

## 🧪 Testando com cURL

### 1. Verificar Saúde da API
```bash
curl -X GET http://127.0.0.1:9001/health
```

### 2. Criar Primeiro Usuário
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

### 3. Fazer Login
```bash
curl -X POST http://127.0.0.1:9001/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123456"
  }'
```

### 4. Listar Usuários (com token)
```bash
curl -X GET http://127.0.0.1:9001/user/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔍 Troubleshooting

### ❌ Erro: "Database connection failed"
- Verifique se PostgreSQL está rodando
- Verifique a `DATABASE_URL` no `.env`
- Certifique-se de que o banco de dados existe

### ❌ Erro: "No users found" ou "Cannot authenticate"
- Execute o endpoint de inicialização: `POST /admin/init/create-first-user`
- Após criar o primeiro usuário, faça login para obter o token JWT

### ❌ Erro: "Invalid token" ao chamar endpoints autenticados
- Verifique se o token JWT está sendo enviado no header `Authorization: Bearer <token>`
- Tokens expiram após o tempo definido em `ACCESS_TOKEN_EXPIRE_MINUTES`
- Faça login novamente para obter um novo token

### ❌ Erro: "CORS error" ao chamar da frontend
- Verifique se a origem está configurada em `allow_origins` no `app/main.py`
- Atualize a URL da frontend no arquivo se necessário

---

## 📝 Notas Importantes

1. **Primeira Execução**: Use o endpoint `/admin/init/create-first-user` para criar o usuário administrador
2. **Autenticação**: A maioria dos endpoints requer um token JWT válido
3. **Documentação Interativa**: Acesse http://127.0.0.1:9001/docs para testar os endpoints diretamente
4. **Soft Delete**: Algumas entidades suportam soft delete (marcar como deletado sem remover do banco)
5. **Paginação**: Endpoints de listagem suportam `page` e `limit` query parameters

---

## 🔗 Links Úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT Authentication](https://fastapi.tiangolo.com/advanced/security/oauth2-jwt/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

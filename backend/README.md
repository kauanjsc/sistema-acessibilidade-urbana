# Teresina Acessível — Backend API

Backend REST em **FastAPI** para a plataforma colaborativa de mapeamento de acessibilidade urbana.

## Stack

| Tecnologia | Versão | Uso |
|---|---|---|
| FastAPI | 0.111 | Framework REST |
| SQLAlchemy | 2.0 | ORM |
| PostgreSQL | 14+ | Banco de dados |
| Pydantic v2 | 2.7 | Validação e schemas |
| python-jose | 3.3 | Tokens JWT |
| passlib/bcrypt | 1.7 | Hash de senhas |
| Alembic | 1.13 | Migrações |

---

## Estrutura do projeto

```
backend/
├── app/
│   ├── main.py          # Aplicação FastAPI + CORS + routers
│   ├── config.py        # Variáveis de ambiente (pydantic-settings)
│   ├── database.py      # Engine, SessionLocal, Base
│   ├── security.py      # bcrypt, JWT, dependência get_current_user
│   ├── models/
│   │   ├── usuario.py   # Tabela usuarios
│   │   ├── local.py     # Tabela locais
│   │   └── avaliacao.py # Tabela avaliacoes
│   ├── schemas/
│   │   ├── usuario.py   # Pydantic: register, login, response
│   │   ├── local.py     # Pydantic: LocalResponse (compatível com frontend)
│   │   └── avaliacao.py # Pydantic: create, response, estatísticas
│   ├── routers/
│   │   ├── auth.py      # POST /auth/register, /login · GET /auth/me
│   │   ├── locais.py    # GET /locais, /locais/{id}
│   │   └── avaliacoes.py# POST /avaliacoes · GET /avaliacoes/local/{id}
│   └── services/
│       ├── usuario_service.py
│       ├── local_service.py
│       └── avaliacao_service.py
├── seed.py              # Popula banco com dados iniciais
├── requirements.txt
├── .env.example
└── README.md
```

---

## Instalação e execução

### 1. Pré-requisitos
- Python 3.11+
- PostgreSQL rodando localmente

### 2. Criar banco de dados no PostgreSQL
```sql
CREATE DATABASE teresina_acessivel;
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com sua DATABASE_URL e SECRET_KEY
```

### 4. Instalar dependências
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Popular banco com dados iniciais
```bash
python seed.py
```

### 6. Iniciar servidor
```bash
uvicorn app.main:app --reload
# API disponível em: http://localhost:8000
# Documentação em:   http://localhost:8000/docs
```

---

## Endpoints

### Autenticação

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/auth/register` | ❌ | Cadastrar novo usuário |
| POST | `/auth/login` | ❌ | Login → retorna JWT |
| GET | `/auth/me` | 🔒 JWT | Dados do usuário logado |

### Locais

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/locais` | ❌ | Listar todos os locais |
| GET | `/locais/{id}` | ❌ | Detalhe de um local |

### Avaliações

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/avaliacoes` | 🔒 JWT | Enviar avaliação |
| GET | `/avaliacoes/local/{id}` | ❌ | Listar avaliações de um local |

---

## Exemplos de uso

### Registrar usuário
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "email": "joao@email.com", "senha": "minhasenha"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "joao@email.com", "senha": "minhasenha"}'
```

### Enviar avaliação (com token)
```bash
curl -X POST http://localhost:8000/avaliacoes \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"local_id": 4, "acessivel": true, "comentario": "Ótima acessibilidade no local!"}'
```

---

## Credenciais de teste (após seed.py)

| Nome | E-mail | Senha | Perfil |
|---|---|---|---|
| Kauan Santos | kauan@teresina.gov.br | senha123 | cidadão |
| Maria Oliveira | maria@email.com | maria2024 | cidadão |
| Admin Sistema | admin@teresina.gov.br | admin123 | admin |

---

## Integração com o frontend Vue

O frontend já está configurado com autenticação mock. Para conectar à API real:

1. Atualize `authService.js` para usar `fetch` no endpoint `/auth/login`
2. Salve o token JWT retornado no `localStorage`
3. Inclua `Authorization: Bearer <token>` nas chamadas a `/avaliacoes`
4. Substitua `acessibilidadeService.js` para buscar de `/locais`
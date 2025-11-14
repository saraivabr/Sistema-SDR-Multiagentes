# Arquitetura Python - Sistema SDR Multi-Agentes

## 🎯 Visão Geral

Migração completa do sistema n8n para Python, mantendo toda a funcionalidade e melhorando:
- ✅ Testabilidade
- ✅ Versionamento de código
- ✅ Performance
- ✅ Escalabilidade
- ✅ Manutenibilidade

## 🏗️ Stack Tecnológica Proposta

### Backend & Framework
- **Python 3.11+**: Linguagem principal
- **FastAPI**: Framework web assíncrono para webhooks e APIs
- **Uvicorn**: ASGI server de alta performance

### Orquestração de Agentes
- **LangChain**: Framework para construção de aplicações com LLMs
- **LangGraph**: Para grafos de estados e roteamento complexo
- **OpenAI SDK**: Integração com GPT-4

### Banco de Dados & Storage
- **SQLAlchemy 2.0**: ORM assíncrono para PostgreSQL
- **Alembic**: Migrações de banco de dados
- **Supabase Python SDK**: Vector store e embeddings
- **Redis**: Cache e gerenciamento de sessões (opcional)

### Processamento de Mídia
- **Pillow (PIL)**: Processamento de imagens
- **pytesseract**: OCR para documentos
- **openai-whisper**: Transcrição de áudio
- **ffmpeg-python**: Conversão de formatos de áudio

### Utilitários
- **Pydantic**: Validação de dados e settings
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **httpx**: Cliente HTTP assíncrono
- **celery**: Tarefas assíncronas em background (opcional)
- **structlog**: Logging estruturado

### Desenvolvimento & Testes
- **pytest**: Framework de testes
- **pytest-asyncio**: Testes assíncronos
- **black**: Formatação de código
- **ruff**: Linting moderno e rápido
- **mypy**: Type checking
- **poetry**: Gerenciamento de dependências

## 📁 Estrutura de Diretórios

```
sistema-sdr-python/
├── .env.example                  # Template de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados
├── pyproject.toml               # Configuração Poetry + ferramentas
├── README.md                     # Documentação do projeto Python
├── Dockerfile                    # Container da aplicação
├── docker-compose.yml           # Orquestração de serviços
│
├── alembic/                     # Migrações de banco de dados
│   ├── versions/
│   └── env.py
│
├── src/                         # Código fonte principal
│   ├── __init__.py
│   │
│   ├── main.py                  # Entry point FastAPI
│   ├── config.py                # Configurações (Pydantic Settings)
│   ├── dependencies.py          # FastAPI dependencies
│   │
│   ├── api/                     # Rotas FastAPI
│   │   ├── __init__.py
│   │   ├── webhooks.py          # Webhook Evolution API
│   │   ├── health.py            # Health check endpoints
│   │   └── admin.py             # Endpoints administrativos
│   │
│   ├── agents/                  # Sistema de agentes
│   │   ├── __init__.py
│   │   ├── base.py              # Classe base para agentes
│   │   ├── supervisor.py        # Agente supervisor (router)
│   │   ├── geral.py             # Agente geral (triage)
│   │   ├── loteamentos.py       # Agente loteamentos
│   │   ├── construtora.py       # Agente construtora
│   │   └── schemas.py           # Schemas Pydantic para agentes
│   │
│   ├── tools/                   # Ferramentas dos agentes
│   │   ├── __init__.py
│   │   ├── base.py              # Classe base para tools
│   │   ├── database.py          # Tools de database (leads)
│   │   ├── rag.py               # Tools de RAG (vector search)
│   │   ├── media.py             # Tools de busca de mídia
│   │   └── thinking.py          # Think tool
│   │
│   ├── services/                # Serviços de integração
│   │   ├── __init__.py
│   │   ├── openai_service.py    # Wrapper OpenAI
│   │   ├── supabase_service.py  # Wrapper Supabase
│   │   ├── evolution_api.py     # Cliente Evolution API
│   │   ├── message_processor.py # Processamento de mensagens
│   │   └── media_processor.py   # OCR, transcrição, etc.
│   │
│   ├── db/                      # Camada de banco de dados
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── session.py           # Sessão de banco
│   │   ├── repositories/        # Padrão Repository
│   │   │   ├── __init__.py
│   │   │   ├── leads.py
│   │   │   └── chat_memory.py
│   │
│   ├── core/                    # Core business logic
│   │   ├── __init__.py
│   │   ├── router.py            # Lógica de roteamento
│   │   ├── memory.py            # Gerenciamento de memória
│   │   ├── message_buffer.py    # Buffer de 10 segundos
│   │   └── exceptions.py        # Exceções customizadas
│   │
│   ├── prompts/                 # Prompts dos agentes
│   │   ├── __init__.py
│   │   ├── supervisor.py        # Prompt do supervisor
│   │   ├── geral.py             # Prompt agente geral
│   │   ├── loteamentos.py       # Prompt loteamentos
│   │   └── construtora.py       # Prompt construtora
│   │
│   └── utils/                   # Utilitários
│       ├── __init__.py
│       ├── logger.py            # Configuração de logging
│       ├── validators.py        # Validadores customizados
│       └── helpers.py           # Funções auxiliares
│
├── tests/                       # Testes
│   ├── __init__.py
│   ├── conftest.py              # Fixtures pytest
│   ├── unit/                    # Testes unitários
│   │   ├── test_agents.py
│   │   ├── test_tools.py
│   │   └── test_services.py
│   ├── integration/             # Testes de integração
│   │   ├── test_api.py
│   │   └── test_workflows.py
│   └── e2e/                     # Testes end-to-end
│       └── test_conversation_flows.py
│
└── scripts/                     # Scripts utilitários
    ├── seed_database.py         # Popular banco de dados
    ├── migrate_n8n_data.py      # Migrar dados do n8n
    └── run_dev.sh               # Script para desenvolvimento
```

## 🔄 Fluxo de Dados

### 1. Recebimento de Mensagem
```python
WhatsApp → Evolution API → FastAPI Webhook → MessageProcessor
```

### 2. Processamento Inicial
```python
MessageProcessor:
  ├─ Classificar tipo (texto/áudio/imagem)
  ├─ Processar mídia (OCR/transcrição)
  ├─ Aplicar buffer (10s)
  └─ Sanitizar input
```

### 3. Roteamento Inteligente
```python
SupervisorAgent:
  ├─ Carregar memória (PostgreSQL)
  ├─ Think Tool (análise)
  ├─ Decidir agente
  └─ Chamar agente específico
```

### 4. Execução do Agente
```python
Agent (Geral/Loteamentos/Construtora):
  ├─ Carregar contexto
  ├─ Executar LLM
  ├─ Usar tools conforme necessário
  ├─ Gerar resposta
  └─ Salvar na memória
```

### 5. Envio de Resposta
```python
Response → EvolutionAPIClient → WhatsApp
```

## 🎨 Arquitetura de Agentes (LangChain)

### Agente Base
```python
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.memory import PostgresChatMessageHistory

class BaseAgent:
    def __init__(self, name: str, tools: list, prompt: str):
        self.name = name
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        self.tools = tools
        self.prompt = prompt
        self.memory = None  # Configurado por sessão

    async def execute(self, input: str, session_id: str) -> str:
        # Configurar memória para sessão
        # Criar agent executor
        # Executar e retornar resposta
        pass
```

### Supervisor (Router)
```python
from langgraph.graph import StateGraph, END

class SupervisorAgent:
    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        # Define estados: ANALYZE → ROUTE → EXECUTE
        # Think tool obrigatório no ANALYZE
        # Routing rules em ROUTE
        # Fallback sempre para Agente Geral
        pass

    async def route(self, message: str, session_id: str) -> str:
        # Executa grafo e retorna resposta
        pass
```

## 🗄️ Modelos de Dados (SQLAlchemy)

### Lead Model
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    telefone = Column(String(20), unique=True, nullable=False, index=True)
    nome = Column(String(100))
    interesse = Column(String(50), index=True)
    qualificado = Column(Boolean, default=False, index=True)
    notas = Column(String(250))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

### Chat Memory
```python
class ChatMessage(Base):
    __tablename__ = "chat_memory"

    id = Column(UUID, primary_key=True, default=uuid4)
    session_id = Column(String(50), nullable=False, index=True)
    message = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # user/assistant/system
    timestamp = Column(DateTime, server_default=func.now())
```

## 🔌 Integrações

### Evolution API Client
```python
class EvolutionAPIClient:
    async def send_message(self, phone: str, text: str) -> dict
    async def send_media(self, phone: str, media_url: str) -> dict
    async def get_instance_status(self) -> dict
```

### Supabase Service (Vector Store)
```python
class SupabaseService:
    async def search_loteamentos(self, query: str, top_k: int = 5) -> list
    async def search_construtora(self, query: str, top_k: int = 4) -> list
    async def upsert_documents(self, documents: list) -> None
```

## 🛠️ Configuração (Pydantic Settings)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # PostgreSQL
    DATABASE_URL: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Evolution API
    EVOLUTION_API_URL: str
    EVOLUTION_INSTANCE: str
    EVOLUTION_API_KEY: str

    # Buffer
    MESSAGE_BUFFER_SECONDS: int = 10

    # Limits
    MAX_CONTEXT_TOKENS: int = 1000
    MAX_RESPONSE_LINES: int = 3

    class Config:
        env_file = ".env"
```

## 🚀 API Endpoints

### Webhooks
```python
POST /webhook/evolution
  - Recebe mensagens do WhatsApp
  - Valida origem
  - Enfileira processamento

GET /health
  - Status da aplicação
  - Conexões com serviços
```

### Admin (opcional)
```python
POST /admin/leads
  - Listar/filtrar leads

GET /admin/metrics
  - Métricas do sistema

POST /admin/test-agent/{agent_name}
  - Testar agente específico
```

## 🧪 Testes

### Testes Unitários
```python
# tests/unit/test_agents.py
async def test_supervisor_routes_to_geral_on_first_message()
async def test_supervisor_routes_to_loteamentos_on_keyword()
async def test_agente_geral_collects_name()
```

### Testes de Integração
```python
# tests/integration/test_workflows.py
async def test_full_conversation_flow_loteamentos()
async def test_media_request_returns_links()
async def test_context_preserved_across_messages()
```

## 🐳 Docker & Deploy

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema (tesseract, ffmpeg)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copiar código
COPY . .

# Comando de execução
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - postgres
    volumes:
      - ./logs:/app/logs

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: lemans_sdr
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:  # Opcional, para cache
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 🔄 Migração do n8n

### Estratégia de Migração

1. **Fase 1: Desenvolvimento Paralelo**
   - Criar sistema Python completo
   - Testar extensivamente
   - Manter n8n em produção

2. **Fase 2: Teste Beta**
   - Redirecionar 10% do tráfego para Python
   - Monitorar métricas
   - Ajustar conforme necessário

3. **Fase 3: Migração Gradual**
   - Aumentar gradualmente para 50%, 75%, 100%
   - Manter n8n como fallback
   - Comparar performance

4. **Fase 4: Deprecação n8n**
   - Desativar workflows n8n
   - Manter apenas para referência
   - Documentar lições aprendidas

### Script de Migração de Dados
```python
# scripts/migrate_n8n_data.py
async def migrate_chat_memory():
    # Exportar memória do n8n
    # Importar para novo formato
    pass

async def migrate_leads():
    # Verificar consistência
    # Migrar dados se necessário
    pass
```

## 📊 Métricas & Monitoramento

### Logs Estruturados
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "message_received",
    session_id=session_id,
    message_type=msg_type,
    agent="supervisor"
)
```

### Métricas (Prometheus - opcional)
```python
from prometheus_client import Counter, Histogram

messages_received = Counter('messages_received_total', 'Total messages received')
response_time = Histogram('response_time_seconds', 'Response time')
agent_calls = Counter('agent_calls_total', 'Agent calls', ['agent_name'])
```

## 🎯 Vantagens da Nova Arquitetura

### ✅ Testabilidade
- Testes unitários para cada componente
- Testes de integração end-to-end
- Mocking fácil de dependências

### ✅ Versionamento
- Código fonte versionado no Git
- Rollback fácil de mudanças
- Code review antes de deploy

### ✅ Performance
- Assíncrono por padrão (FastAPI + async/await)
- Conexões pooling com PostgreSQL
- Cache inteligente com Redis

### ✅ Escalabilidade
- Horizontal: múltiplas instâncias atrás de load balancer
- Vertical: otimização de recursos
- Celery para tarefas pesadas em background

### ✅ Manutenibilidade
- Código organizado e modular
- Type hints para autocomplete e validação
- Logs estruturados para debugging

### ✅ Developer Experience
- IDE support completo (VSCode, PyCharm)
- Type checking com mypy
- Linting e formatação automatizados
- Hot reload em desenvolvimento

## 📝 Próximos Passos

1. **Setup Inicial**
   - [ ] Criar estrutura de diretórios
   - [ ] Configurar Poetry e dependências
   - [ ] Setup Docker e docker-compose

2. **Core Development**
   - [ ] Implementar modelos de dados
   - [ ] Criar serviços de integração
   - [ ] Desenvolver sistema de agentes

3. **API & Webhooks**
   - [ ] Implementar endpoints FastAPI
   - [ ] Configurar processamento de mensagens
   - [ ] Integrar Evolution API

4. **Testes**
   - [ ] Escrever testes unitários
   - [ ] Criar testes de integração
   - [ ] Testes end-to-end

5. **Deploy**
   - [ ] Configurar CI/CD
   - [ ] Deploy em staging
   - [ ] Migração gradual de produção

---

**Desenvolvido para**: Le Mans Loteamentos e Construtora
**Stack**: Python 3.11+ | FastAPI | LangChain | PostgreSQL | Supabase
**Status**: 🚧 Em Planejamento

# Sistema SDR Multi-Agentes - Python

Sistema de automação de atendimento via WhatsApp usando múltiplos agentes especializados de IA para qualificação e gestão de leads da Le Mans Loteamentos e Construtora.

## 🚀 Stack Tecnológica

- **Python 3.11+**: Linguagem principal
- **FastAPI**: Framework web assíncrono
- **LangChain**: Orquestração de agentes com LLMs
- **PostgreSQL**: Banco de dados principal
- **Supabase**: Vector store para RAG
- **OpenAI GPT-4**: Modelo de linguagem
- **Evolution API**: Integração WhatsApp

## 📦 Instalação

### Requisitos
- Python 3.11+
- Poetry
- PostgreSQL 15+
- Redis (opcional)
- Tesseract OCR
- FFmpeg

### Setup

1. **Clone o repositório**
```bash
git clone <repo-url>
cd sistema-sdr-python
```

2. **Instale dependências**
```bash
poetry install
```

3. **Configure variáveis de ambiente**
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

4. **Execute migrações**
```bash
poetry run alembic upgrade head
```

5. **Inicie o servidor**
```bash
poetry run uvicorn src.main:app --reload
```

## 🏗️ Arquitetura

### Fluxo de Dados
```
WhatsApp → Evolution API → FastAPI Webhook → Message Processor
    ↓
Supervisor Agent (Router)
    ↓
    ├─→ Agente Geral (Triage)
    ├─→ Agente Loteamentos (Specialist)
    └─→ Agente Construtora (Specialist)
        ↓
    Tools (Database, RAG, Media)
        ↓
Response → Evolution API → WhatsApp
```

### Componentes Principais

- **API Layer**: FastAPI endpoints para webhooks
- **Agents**: Sistema multi-agente com LangChain
- **Tools**: Ferramentas para database, RAG, mídia
- **Services**: Integrações com APIs externas
- **Core**: Lógica de roteamento e memória

## 🧪 Testes

```bash
# Executar todos os testes
poetry run pytest

# Com cobertura
poetry run pytest --cov

# Apenas testes unitários
poetry run pytest tests/unit/

# Testes específicos
poetry run pytest tests/unit/test_agents.py -v
```

## 🐳 Docker

```bash
# Build
docker-compose build

# Run
docker-compose up

# Run em background
docker-compose up -d
```

## 📝 Desenvolvimento

### Code Quality

```bash
# Formatação
poetry run black src/ tests/

# Linting
poetry run ruff check src/ tests/

# Type checking
poetry run mypy src/
```

### Pre-commit Hooks

```bash
poetry run pre-commit install
```

## 📚 Documentação

- **Arquitetura**: Ver `ARQUITETURA_PYTHON.md`
- **API Docs**: Acesse `/docs` quando servidor estiver rodando
- **Prompts**: Documentação em `src/prompts/`

## 🔧 Configuração

Todas as configurações são gerenciadas via variáveis de ambiente (`.env`).

Ver `.env.example` para lista completa de configurações disponíveis.

## 📊 Monitoramento

- **Logs**: Estruturados com structlog em formato JSON
- **Health Check**: `GET /health`
- **Metrics**: Prometheus metrics em `/metrics` (opcional)

## 🚀 Deploy

### Produção

1. Configure variáveis de ambiente de produção
2. Execute migrações: `alembic upgrade head`
3. Inicie com: `uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4`

### Docker

```bash
docker build -t lemans-sdr:latest .
docker run -p 8000:8000 --env-file .env lemans-sdr:latest
```

## 📄 Licença

Propriedade de Le Mans Loteamentos e Construtora

## 👥 Contato

**Desenvolvido por**: Fellipe Saraiva
**Empresa**: Le Mans Loteamentos e Construtora

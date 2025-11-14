# Instalação e Configuração - Sistema SDR Le Mans

## 🚀 Pré-requisitos

### Infraestrutura Necessária
- **n8n**: Versão 1.0+ (self-hosted ou cloud)
- **PostgreSQL**: Base de dados para memória e leads
- **Supabase**: Vector store para RAG
- **OpenAI API**: GPT-4 e Embeddings
- **Evolution API**: Integração WhatsApp

### Credenciais Requeridas
- OpenAI API Key
- Supabase Project URL + API Key
- PostgreSQL connection string
- Evolution API webhook URL

## 📦 Instalação dos Workflows

### 1. Importação dos Workflows
```bash
# Navegar até a pasta workflows
cd workflows/

# Importar workflow principal
# Importar via n8n interface: principal/whatsapp-sara.json

# Importar agentes especializados
# workflows/agentes/agente-supervisor.json
# workflows/agentes/agente-geral.json
# workflows/agentes/agente-loteamentos.json
# workflows/agentes/agente-construtora.json

# Importar sub-workflows
# workflows/sub-workflows/envio-midia-construtora.json
# workflows/sub-workflows/envio-midia-loteamentos.json
```

### 2. Ordem de Importação
1. **Sub-workflows** (primeiro, para obter IDs)
2. **Agentes especializados**
3. **Agente Supervisor**
4. **Workflow principal WhatsApp**

## ⚙️ Configuração de Credenciais

### OpenAI Configuration
```json
{
  "name": "Le Mans",
  "apiKey": "sk-...",
  "organization": "org-..."
}
```

### PostgreSQL Configuration
```json
{
  "name": "Le Mans",
  "host": "localhost",
  "database": "lemans_sdr",
  "user": "postgres",
  "password": "***",
  "port": 5432,
  "ssl": false
}
```

### Supabase Configuration
```json
{
  "name": "Le Mans",
  "host": "https://your-project.supabase.co",
  "serviceRole": "eyJ...",
  "table": "documents"
}
```

## 🗄️ Configuração do Banco de Dados

### Estrutura da Tabela Leads
```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    telefone VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(100),
    interesse VARCHAR(50),
    qualificado BOOLEAN DEFAULT FALSE,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_leads_telefone ON leads(telefone);
CREATE INDEX idx_leads_qualificado ON leads(qualificado);
CREATE INDEX idx_leads_interesse ON leads(interesse);
```

### Configuração de Memória (Chat Memory)
```sql
-- Tabela automática criada pelo n8n
-- Configurar context window: 1000 tokens
-- Session ID: usar número do telefone
```

## 📊 Configuração do Vector Store

### Base rag_loteamentos
```sql
-- Estrutura de documentos esperada
{
  "content": "MÍDIAS" | "INFORMAÇÕES",
  "metadata": {
    "loteamento": "Nome do Loteamento",
    "tipo": "mídia" | "info",
    "links": ["url1", "url2", ...]
  }
}
```

### Base rag_construtora
```sql
-- Estrutura de documentos esperada
{
  "content": "MÍDIAS" | "PORTFÓLIO",
  "metadata": {
    "tipo": "mídia" | "portfolio",
    "categoria": "residencial" | "comercial",
    "links": ["url1", "url2", ...]
  }
}
```

## 🔧 Configuração dos Workflows

### 1. Workflow Principal (WhatsApp Sara)
```yaml
Configurações:
  - Webhook URL: /webhook/whatsapp
  - Evolution API connection
  - Buffer timeout: 10 segundos
  - OCR service integration
  - Audio transcription service
```

### 2. Agente Supervisor
```yaml
Configurações:
  - Workflow IDs dos agentes especializados
  - Timeout para respostas: 5 segundos
  - Fallback sempre para Agente Geral
  - Log de decisões habilitado
```

### 3. Agentes Especializados
```yaml
Configurações Comuns:
  - Memory context window: 1000 tokens
  - Session ID: {{ $json.sessionId }}
  - Timeout: 30 segundos
  - Error handling: return to supervisor

Específicas por Agente:
  - Agente Geral: Tools básicas
  - Agente Loteamentos: RAG + Mídia loteamentos
  - Agente Construtora: RAG + Mídia construtora
```

### 4. Sub-workflows de Mídia
```yaml
Configurações:
  - Vector store connections
  - Output limit: 5 links máximo
  - Link cleaning regex patterns
  - Metadata filtering rules
```

## 🔗 Configuração da Evolution API

### Webhook Configuration
```json
{
  "webhook": {
    "url": "https://your-n8n.com/webhook/whatsapp",
    "events": ["messages.upsert"],
    "headers": {
      "Authorization": "Bearer your-token"
    }
  }
}
```

### Instance Settings
```json
{
  "instanceName": "lemans-sdr",
  "qrcode": true,
  "markMessagesRead": true,
  "delayMessage": 1000,
  "alwaysOnline": true
}
```

## 🎯 Configuração de Prompts

### Personalização por Cliente
```bash
# Editar prompts em: prompts/system-messages/
# Ajustar informações específicas:
# - Nome da empresa
# - Telefones de contato
# - Produtos/serviços
# - Políticas de atendimento
```

### Variáveis de Ambiente
```bash
# Context variables disponíveis:
{{ $json.sessionId }}          # Telefone do usuário
{{ $json.chatInput }}          # Mensagem atual
{{ $json.instancia }}          # Instância Evolution API
{{ new Date().toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' }) }}
```

## 🔍 Testes e Validação

### 1. Teste de Conectividade
```bash
# Testar webhook Evolution API
curl -X POST https://your-n8n.com/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{"test": "connectivity"}'
```

### 2. Teste de Agentes
```bash
# Usar chat de teste em cada agente
# Verificar:
# - Respostas adequadas
# - Tools funcionando
# - Memória persistindo
# - RAG retornando resultados
```

### 3. Teste de Fluxo Completo
```bash
# Simular conversa completa:
# 1. Primeira mensagem
# 2. Roteamento correto
# 3. Qualificação
# 4. Envio de mídia
# 5. Conexão com especialista
```

## 📊 Monitoramento

### Logs Importantes
- Decisões do Agente Supervisor
- Erros de roteamento
- Performance de RAG queries
- Timeouts de agentes

### Métricas de Performance
```bash
# Configurar alertas para:
# - Tempo de resposta > 5s
# - Taxa de erro > 1%
# - Falhas de webhook
# - Timeouts de OpenAI
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Agente não responde
```bash
# Verificar:
# - Credenciais OpenAI válidas
# - Limite de tokens não excedido
# - Conexão com PostgreSQL
# - Workflow ativo
```

#### 2. RAG não retorna resultados
```bash
# Verificar:
# - Vector store populado
# - Embeddings corretos
# - Filtros de metadata
# - Similarity threshold
```

#### 3. Webhook não recebe mensagens
```bash
# Verificar:
# - Evolution API configurada
# - URL webhook correta
# - Instância conectada ao WhatsApp
# - Firewall/proxy
```

#### 4. Memória não persiste
```bash
# Verificar:
# - PostgreSQL connection
# - Session ID consistency
# - Tabela chat_memory criada
# - Permissions adequadas
```

## 🔄 Backup e Versionamento

### Backup dos Workflows
```bash
# Exportar workflows regularmente
# Versionar prompts no Git
# Backup do banco PostgreSQL
# Backup do vector store Supabase
```

### Estratégia de Deploy
```bash
# 1. Testar em ambiente de dev
# 2. Validar com dados de teste
# 3. Deploy incremental em produção
# 4. Monitorar métricas pós-deploy
```

---

**Importante**: Sempre testar em ambiente de desenvolvimento antes de aplicar em produção. Manter backups atualizados e logs de auditoria habilitados.
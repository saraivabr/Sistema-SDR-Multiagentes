# Arquitetura do Sistema SDR Multi-Agentes

## 🏛️ Visão Geral da Arquitetura

O sistema SDR da Le Mans utiliza uma arquitetura de múltiplos agentes especializados orquestrados por um agente supervisor central. Cada componente tem responsabilidades específicas e bem definidas.

## 🔄 Fluxo de Dados

### 1. Entrada de Mensagens
```
WhatsApp User → Evolution API → Webhook → n8n Workflow Principal
```

### 2. Processamento Inicial
```
Webhook → Classificação de Mensagem → Buffer 10s → Agente Supervisor
```

### 3. Roteamento Inteligente
```
Agente Supervisor → [Think Tool] → Decisão → Agente Especializado
```

### 4. Processamento Especializado
```
Agente Específico → [Tools + RAG] → Resposta → Evolution API → WhatsApp
```

## 🧠 Componentes da Arquitetura

### Workflow Principal: WhatsApp Sara
**Responsabilidades:**
- Receber webhooks da Evolution API
- Classificar tipo de mensagem (texto/áudio/imagem/documento)
- Processar áudio com transcrição
- Aplicar OCR em imagens/documentos
- Implementar buffer de 10 segundos
- Chamar Agente Supervisor

**Tecnologias:**
- Webhook trigger
- Conditional logic
- Audio processing
- OCR integration
- Timer/delay functions

### Agente Supervisor
**Responsabilidades:**
- Analisar contexto completo da conversa
- Decidir qual agente especializado acionar
- Implementar fallback para Agente Geral
- Manter log de decisões

**Processo de Decisão:**
1. **Think Tool**: Reflexão obrigatória
2. **Análise de Contexto**: Histórico + mensagem atual
3. **Classificação de Intenção**: Loteamentos/Construção/Geral
4. **Roteamento**: Chamada do agente apropriado

### Agentes Especializados

#### Agente Geral
- **Função**: Atendimento inicial e triagem
- **Especialidade**: Direcionamento para canais corretos
- **Tools**: cadastro_lead, anotacao_lead, Think_tool

#### Agente Loteamentos
- **Função**: Consultoria em terrenos e loteamentos
- **Especialidade**: Qualificação e apresentação de terrenos
- **Tools**: rag_loteamentos, envio_midia_loteamentos, interesse_lead, lead_qualificado

#### Agente Construtora
- **Função**: Consultoria em projetos de construção
- **Especialidade**: Projetos personalizados e portfólio
- **Tools**: rag_construtora, envio_midia_construtora, interesse_lead, lead_qualificado

## 🗄️ Camada de Dados

### PostgreSQL
- **Memória Compartilhada**: Histórico de conversas entre agentes
- **Leads Database**: Cadastro, anotações, qualificação
- **Session Management**: Controle de sessões ativas

### Supabase Vector Store
- **rag_loteamentos**: Base de conhecimento de loteamentos
- **rag_construtora**: Base de conhecimento de construções
- **Embeddings**: OpenAI para busca semântica

## 🔧 Ferramentas (Tools)

### Categoria: Banco de Dados
- **cadastro_lead**: Registro inicial de leads
- **anotacao_lead**: Anotações para vendedores
- **interesse_lead**: Classificação de interesse
- **lead_qualificado**: Marcação para especialistas

### Categoria: Consulta
- **rag_loteamentos**: Busca em base de loteamentos
- **rag_construtora**: Busca em base de construções
- **Think_tool**: Ferramenta de reflexão interna

### Categoria: Mídia
- **envio_midia_loteamentos**: Sub-workflow para mídias de loteamentos
- **envio_midia_construtora**: Sub-workflow para mídias de construções

## 🔀 Sub-workflows

### Envio de Mídia Construtora
```
Input: query → Vector Search → Filter Links → Clean URLs → Return Top 5
```

### Envio de Mídia Loteamentos
```
Input: query + loteamento → Filtered Vector Search → Filter Links → Clean URLs → Return Top 5
```

## 🔐 Segurança e Controle

### Validação de Entrada
- Sanitização de mensagens
- Validação de tipos de arquivo
- Controle de tamanho de uploads

### Rate Limiting
- Buffer de 10 segundos para evitar spam
- Controle de sessões simultâneas
- Timeout de inatividade

### Fallback Strategy
1. **Primeiro nível**: Agente específico
2. **Segundo nível**: Agente Geral
3. **Terceiro nível**: Direcionamento manual para (19) 2533-0370

## 📊 Monitoramento

### Métricas Coletadas
- Tempo de resposta por agente
- Taxa de acerto de roteamento
- Conversão de leads qualificados
- Volume de mensagens por período

### Logs Estruturados
- Decisões do Agente Supervisor
- Uso de ferramentas por agente
- Erros e exceções
- Performance de sub-workflows

## 🚀 Escalabilidade

### Horizontal
- Múltiplas instâncias de n8n
- Load balancing de webhooks
- Distribuição de workload

### Vertical
- Otimização de prompts
- Cache de respostas RAG
- Melhoria de embeddings

## 🔄 Manutenibilidade

### Modularização
- Agentes independentes
- Prompts centralizados
- Tools reutilizáveis

### Versionamento
- Controle de mudanças em prompts
- Rollback de configurações
- A/B testing de comportamentos

---

Esta arquitetura garante flexibilidade, escalabilidade e manutenibilidade, permitindo ajustes finos em cada componente sem impactar o sistema completo.
# CLAUDE.md - AI Assistant Guide for Sistema SDR Multiagentes

> **Purpose**: This document provides comprehensive guidance for AI assistants (like Claude, GPT-4, etc.) working with this codebase. It explains the architecture, conventions, workflows, and best practices for modifying and maintaining this multi-agent SDR system.

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & System Design](#architecture--system-design)
3. [Directory Structure](#directory-structure)
4. [Core Components](#core-components)
5. [Development Workflows](#development-workflows)
6. [Key Conventions](#key-conventions)
7. [Common Tasks & Patterns](#common-tasks--patterns)
8. [Testing & Validation](#testing--validation)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Critical Rules](#critical-rules)

---

## Project Overview

**Sistema SDR Multi-Agentes** is a multi-agent AI system for WhatsApp-based lead qualification and sales automation, specifically designed for Le Mans (a real estate company handling both land lots and construction projects).

### Business Context
- **Target**: Real estate sales (loteamentos - land lots, and construtora - construction projects)
- **Platform**: WhatsApp Business via Evolution API
- **Technology**: n8n workflow automation + OpenAI GPT-4 + PostgreSQL + Supabase Vector Store
- **Goal**: Automate 80% of SDR activities, qualify leads 24/7, increase conversion rates

### Key Metrics & Impact
- 80% reduction in response time
- +35% qualified leads per month
- +60% response rate vs manual WhatsApp
- R$40k+ monthly savings in SDR payroll
- 3x faster conversion velocity

---

## Architecture & System Design

### High-Level Flow

```
WhatsApp User
    ↓
Evolution API (Webhook)
    ↓
n8n Workflow Principal: "WhatsApp Sara"
    ↓ (processes message, applies buffer, transcribes audio/OCR)
Agente Supervisor (Router)
    ↓ (Think Tool → analyzes context → decides routing)
    ├─→ Agente Geral (Initial triage, general questions)
    ├─→ Agente Loteamentos (Land/lot specialist)
    └─→ Agente Construtora (Construction specialist)
        ↓ (uses tools: RAG, database ops, media workflows)
Response sent back to WhatsApp
```

### Core Architecture Principles

1. **Modular Multi-Agent Design**: Each agent has specific responsibilities
2. **Shared Memory**: All agents access same PostgreSQL chat memory (session_id = phone number)
3. **Intelligent Routing**: Supervisor agent uses Think Tool for decision-making
4. **RAG-Enhanced Responses**: Vector search in Supabase for accurate information
5. **Fallback Strategy**: Always falls back to Agente Geral if uncertain
6. **Natural Communication**: All agents use "Sara" persona for consistency

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Orchestration | n8n (self-hosted/cloud) | Workflow automation and agent coordination |
| LLM | OpenAI GPT-4 | Agent reasoning and response generation |
| Vector Store | Supabase + OpenAI Embeddings | RAG knowledge base for lots and construction |
| Database | PostgreSQL | Lead management and chat memory |
| WhatsApp | Evolution API | Message sending/receiving |
| Message Processing | OCR + Audio Transcription | Multi-modal input handling |

---

## Directory Structure

```
Sistema-SDR-Multiagentes/
├── README.md                          # Business-focused project overview
├── CLAUDE.md                          # This file - AI assistant guide
├── .gitignore                         # Git ignore patterns
│
├── docs/                              # Technical documentation
│   ├── arquitetura-sistema.md         # System architecture deep-dive
│   ├── fluxo-atendimento.md          # Customer journey and agent flows
│   └── instalacao-configuracao.md     # Setup and configuration guide
│
├── workflows/                         # n8n workflow JSON files
│   ├── principal/
│   │   └── whatsapp-sara.json        # Main webhook workflow (entry point)
│   ├── agentes/
│   │   ├── agente-supervisor.json    # Router agent (Think Tool required)
│   │   ├── agente-geral.json         # General/triage agent
│   │   ├── agente-loteamentos.json   # Land/lots specialist
│   │   └── agente-construtora.json   # Construction specialist
│   └── sub-workflows/
│       ├── envio-midia-loteamentos.json    # Media search for lots
│       └── envio-midia-construtora.json    # Media search for construction
│
├── prompts/                           # All prompt engineering content
│   ├── README.md                      # Prompt organization and patterns
│   ├── system-messages/               # Agent system prompts
│   │   ├── agente-supervisor.md
│   │   ├── agente-geral.md
│   │   ├── agente-loteamentos.md
│   │   └── agente-construtora.md
│   ├── tools/                         # Tool descriptions for agents
│   │   ├── database-operations.md
│   │   ├── rag-queries.md
│   │   ├── media-workflows.md
│   │   └── thinking-tools.md
│   └── sub-workflows/                 # Sub-workflow prompts
│       ├── envio-midia-loteamentos.md
│       └── envio-midia-construtora.md
│
└── assets/
    └── diagramas/
        └── fluxo-sistema.txt          # ASCII system flow diagram
```

### File Naming Conventions
- **Workflows**: kebab-case JSON files (`agente-loteamentos.json`)
- **Documentation**: kebab-case Markdown files (`arquitetura-sistema.md`)
- **Agents**: Prefix with `agente-` for clarity
- **Sub-workflows**: Prefix with `envio-` for media workflows

---

## Core Components

### 1. Workflow Principal: WhatsApp Sara

**File**: `workflows/principal/whatsapp-sara.json`

**Responsibilities**:
- Receive webhooks from Evolution API
- Classify message type (text/audio/image/document)
- Process audio with transcription
- Apply OCR to images/documents
- Implement 10-second buffer to group fragmented messages
- Call Agente Supervisor

**Key Features**:
- Multi-modal message processing
- Buffer prevents spam and groups rapid messages
- Sanitizes input before forwarding

### 2. Agente Supervisor (Router)

**Files**:
- Workflow: `workflows/agentes/agente-supervisor.json`
- Prompt: `prompts/system-messages/agente-supervisor.md`

**Critical Functions**:
- **ALWAYS** uses Think Tool before routing decisions
- Analyzes conversation context from shared memory
- Routes to appropriate specialist agent
- Maintains routing decision logs

**Routing Priority Rules** (in order):
1. **New conversation** → Agente Geral (always)
2. **Continuation with same topic** → Keep current agent
3. **Specific interest detected** → Route to specialist
   - Keywords: "terreno", "lote", "loteamento" → Agente Loteamentos
   - Keywords: "construir", "casa", "projeto" → Agente Construtora
4. **Uncertain/other topics** → Agente Geral (fallback)

### 3. Agente Geral (Triage)

**Files**:
- Workflow: `workflows/agentes/agente-geral.json`
- Prompt: `prompts/system-messages/agente-geral.md`

**Responsibilities**:
- Initial greeting and name collection
- Identify customer needs
- Direct to appropriate channels
- For out-of-scope: Provide contact (19) 2533-0370

**Tools Available**:
- `cadastro_lead`: Register new lead with phone and name
- `anotacao_lead`: Add notes for sales team (max 250 chars)
- `Think_tool`: Internal reflection for decisions

**Typical Flow**:
1. Greet + collect name
2. Identify need
3. Either transition to specialist OR provide contact info
4. Log annotations

### 4. Agente Loteamentos (Land/Lots Specialist)

**Files**:
- Workflow: `workflows/agentes/agente-loteamentos.json`
- Prompt: `prompts/system-messages/agente-loteamentos.md`

**Responsibilities**:
- Consult on land lots and real estate investments
- Qualify leads gradually (ONE question at a time)
- Present relevant options with media
- Transition to human specialist when ready

**Tools Available**:
- `rag_loteamentos`: Search knowledge base (TopK=5)
- `envio_midia_loteamentos`: Fetch media (query + loteamento name)
- `interesse_lead`: Mark interest category
- `lead_qualificado`: Flag for human specialist follow-up
- `Think_tool`: Internal reflection

**Qualification Questions** (gradual):
- Preferred region
- Desired lot size
- Purpose (live/invest)
- Decision timeline

**Interest Signals**:
- 🟢 Active interest: Continue qualifying
- 🟡 Apparent satisfaction: Ask if questions remain
- 🔴 Disinterest: Pause and wait

### 5. Agente Construtora (Construction Specialist)

**Files**:
- Workflow: `workflows/agentes/agente-construtora.json`
- Prompt: `prompts/system-messages/agente-construtora.md`

**Responsibilities**:
- Consult on construction projects
- Qualify technical requirements
- Present portfolio of completed projects
- Transition to human specialist

**Tools Available**:
- `rag_construtora`: Search construction knowledge base (TopK=4)
- `envio_midia_construtora`: Fetch portfolio media (query only)
- `interesse_lead`: Mark interest category
- `lead_qualificado`: Flag for specialist
- `Think_tool`: Internal reflection

**Similar to Agente Loteamentos** but focused on construction-specific questions:
- Project type
- House size
- Land situation
- Preferred style

### 6. Sub-Workflows (Media)

**Envio Mídia Loteamentos**:
- **File**: `workflows/sub-workflows/envio-midia-loteamentos.json`
- **Input**: `query` (e.g., "fotos") + `loteamento` (specific name)
- **Process**: Vector search → Filter by loteamento → Extract links → Clean URLs → Return top 5
- **Output**: Up to 5 relevant media links

**Envio Mídia Construtora**:
- **File**: `workflows/sub-workflows/envio-midia-construtora.json`
- **Input**: `query` (e.g., "fotos de casas")
- **Process**: Vector search (general portfolio) → Extract links → Clean URLs → Return top 5
- **Output**: Up to 5 project examples

---

## Development Workflows

### Adding a New Agent

1. **Create Prompt** in `prompts/system-messages/agente-[name].md`
   - Define Role, Goal, Backstory
   - Specify Core Instructions
   - Define Communication Protocol
   - List Tools Usage patterns
   - Add Quality Control rules

2. **Create Workflow** in `workflows/agentes/agente-[name].json`
   - Import base n8n AI Agent structure
   - Configure OpenAI credentials
   - Set up PostgreSQL chat memory (session_id: phone number)
   - Add tools as needed
   - Configure error handling → fallback to Agente Geral

3. **Update Supervisor** in `prompts/system-messages/agente-supervisor.md`
   - Add routing keywords for new agent
   - Update priority rules if needed
   - Add to Think Tool decision process

4. **Test Isolation**
   - Use n8n's test chat interface
   - Verify tool calls work correctly
   - Check memory persistence
   - Validate responses match persona

5. **Integration Test**
   - Test via actual WhatsApp messages
   - Verify Supervisor routes correctly
   - Check context preservation across agents
   - Monitor for edge cases

### Modifying Existing Agents

**CRITICAL**: Always test in dev/staging before production

1. **Read Current Prompt** in `prompts/system-messages/`
2. **Understand Context**: Review docs/fluxo-atendimento.md for flows
3. **Make Changes**: Edit prompt markdown file
4. **Update Workflow**: Copy prompt into n8n workflow system message
5. **Test Thoroughly**:
   - Unit test: Agent alone
   - Integration test: Full flow through Supervisor
   - Regression test: Old scenarios still work
6. **Document Changes**: Update relevant docs/ files if behavior changes significantly

### Adding New Tools

1. **Define Tool** in `prompts/tools/[category].md`
   - Clear description of purpose
   - Parameter specifications
   - When to use / when NOT to use
   - Examples

2. **Implement in n8n**:
   - Create workflow or function
   - Test independently
   - Return structured output

3. **Add to Agents**:
   - Update agent workflows with new tool
   - Update agent prompts with tool guidance
   - Test agent knows when to use it

### Updating Vector Store (RAG)

**Loteamentos Knowledge Base** (`rag_loteamentos`):
```json
{
  "content": "MÍDIAS" or "INFORMAÇÕES",
  "metadata": {
    "loteamento": "Nome do Loteamento",
    "tipo": "mídia" | "info",
    "links": ["url1", "url2"]
  }
}
```

**Construtora Knowledge Base** (`rag_construtora`):
```json
{
  "content": "MÍDIAS" or "PORTFÓLIO",
  "metadata": {
    "tipo": "mídia" | "portfolio",
    "categoria": "residencial" | "comercial",
    "links": ["url1", "url2"]
  }
}
```

**Process**:
1. Prepare documents in proper JSON structure
2. Generate embeddings using OpenAI
3. Upload to Supabase vector store
4. Test RAG queries return expected results
5. Adjust similarity thresholds if needed

---

## Key Conventions

### Prompt Engineering Standards

**Universal Structure** for all agent prompts:
```markdown
# Role
Clear definition of agent's function

# Goal
Specific objective

# Backstory
Context about Le Mans

# Core Instructions
Fundamental behaviors

# Communication Protocol
Tone, style, response format

# Tools Usage
When and how to use each tool

# Quality Control
Rules to maintain quality

# Additional Context
Dynamic variables
```

**Critical Prompt Principles**:
1. **Naturalness**: Agents speak like real people, not bots
2. **Consistency**: All agents are "Sara" persona
3. **Conciseness**: Maximum 3 lines per response
4. **One Question at a Time**: Avoid interrogation feel
5. **Think Tool Mandatory**: For important decisions
6. **Never Invent**: If info not in RAG, direct to human contact

### System Variables

Available in all n8n workflows:
```javascript
{{ $json.sessionId }}    // Phone number (chat memory key)
{{ $json.chatInput }}    // Current message from user
{{ $json.instancia }}    // Evolution API instance name
{{ new Date().toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' }) }}
```

### Coding Style (n8n JSON)

- **Naming**: Use Portuguese for agent/workflow names (matches business language)
- **Comments**: Add descriptions in node names for clarity
- **Error Handling**: Always include fallback paths
- **Timeouts**: Set reasonable timeouts (30s for agents, 5s for supervisor)
- **Credentials**: Use n8n credential management, never hardcode

### Git Workflow

- **Branch Naming**: Feature branches like `feature/new-agent-name`
- **Commit Messages**: Portuguese, descriptive (e.g., "Adiciona Agente Imobiliário para vendas")
- **PR Process**: Test before merging, document changes in PR description

---

## Common Tasks & Patterns

### Task: Add New Qualification Question to Agent

**Example**: Add "budget" question to Agente Loteamentos

1. **Edit Prompt** (`prompts/system-messages/agente-loteamentos.md`):
   ```markdown
   ## Qualification Questions
   - Preferred region
   - Desired lot size
   - Purpose (live/invest)
   - Budget range  ← NEW
   - Decision timeline
   ```

2. **Update Workflow System Message**: Copy updated prompt to n8n workflow

3. **Test**: Ensure agent asks question naturally in conversation flow

### Task: Change Routing Logic

**Example**: Route "investimento" keyword to Agente Loteamentos

1. **Edit Supervisor Prompt** (`prompts/system-messages/agente-supervisor.md`):
   ```markdown
   ##### Loteamentos → agente_loteamentos
   - "quero comprar terreno"
   - "loteamentos disponíveis"
   - "investimento em terrenos"  ← NEW
   ```

2. **Update Supervisor Workflow**: Copy prompt to n8n

3. **Test Routing**: Send message with "investimento" → verify goes to Loteamentos

### Task: Add New Media Category

**Example**: Add "videos" category to construction media

1. **Update Vector Store**: Add documents with proper metadata
   ```json
   {
     "content": "MÍDIAS - VÍDEOS",
     "metadata": {
       "tipo": "mídia",
       "categoria": "videos",
       "links": ["url1", "url2"]
     }
   }
   ```

2. **Update Agent Guidance**: In `prompts/tools/media-workflows.md`, add video examples

3. **Test**: Agent query with "vídeos" returns video links

### Task: Modify Response Tone

**All agents share "Sara" persona**. To change tone:

1. **Edit Communication Protocol** in agent prompt:
   ```markdown
   # Communication Protocol
   - Tone: Warm, professional, empathetic  ← Adjust here
   - Style: Natural conversation, not salesy
   - Length: Maximum 3 lines
   ```

2. **Test Across Agents**: Ensure consistency if changing globally

### Task: Add Database Field to Leads

**Example**: Add "source" field to track lead origin

1. **Update PostgreSQL Schema**:
   ```sql
   ALTER TABLE leads ADD COLUMN source VARCHAR(50);
   CREATE INDEX idx_leads_source ON leads(source);
   ```

2. **Update Tools**: Modify `cadastro_lead` or `anotacao_lead` to accept new field

3. **Update Agent Prompts**: Instruct agents when to collect this info

4. **Test**: Verify data persists correctly

---

## Testing & Validation

### Pre-Deployment Checklist

Before deploying changes to production:

- [ ] **Unit Tests**: Individual agent responds correctly
- [ ] **Tool Tests**: All tools work in isolation
- [ ] **Routing Tests**: Supervisor routes correctly for each scenario
- [ ] **Memory Tests**: Context persists across messages
- [ ] **RAG Tests**: Vector searches return relevant results
- [ ] **Edge Cases**: Handle unknown requests gracefully
- [ ] **Fallback Tests**: System falls back to Agente Geral on errors
- [ ] **Integration Tests**: Full flow from WhatsApp → response works

### Test Scenarios

**Scenario 1: New Lead - General Interest**
```
User: "Oi"
Expected: Agente Geral → Greets → Asks name
User: "João"
Expected: Confirms name → Asks how to help
User: "Quero informações"
Expected: Asks what about → Offers options
```

**Scenario 2: New Lead - Specific Interest (Lots)**
```
User: "Oi, quero comprar terreno"
Expected: Agente Geral (first message) → Collects name → Transitions
Next: Agente Loteamentos → Starts qualification
```

**Scenario 3: Continuation - Context Preserved**
```
[Previous conversation about lots]
User: "E o preço?"
Expected: Agente Loteamentos → Uses context → Provides pricing info
```

**Scenario 4: Topic Change**
```
[Talking about lots]
User: "Na verdade quero construir uma casa"
Expected: Supervisor detects change → Routes to Agente Construtora
```

**Scenario 5: Out of Scope**
```
User: "Vocês alugam casas?"
Expected: Agente Geral → Provides contact (19) 2533-0370
```

**Scenario 6: RAG Query**
```
[In Agente Loteamentos]
User: "Tem terrenos no Terra Nova?"
Expected: Uses rag_loteamentos → Returns info about Terra Nova
```

**Scenario 7: Media Request**
```
[In Agente Loteamentos]
User: "Quero ver fotos do Terra Nova"
Expected: Calls envio_midia_loteamentos(query="fotos", loteamento="Terra Nova")
         → Returns up to 5 photo links
```

### Performance Benchmarks

Target metrics:
- **First response time**: < 3 seconds
- **Routing accuracy**: > 95%
- **Tool success rate**: > 98%
- **RAG relevance**: > 90%
- **Context preservation**: 100%

### Monitoring & Logging

**Key Logs to Monitor**:
- Supervisor routing decisions (Think Tool output)
- Tool usage per agent
- Errors and exceptions
- RAG query performance
- OpenAI API response times

**Alerts to Configure**:
- Response time > 5 seconds
- Error rate > 1%
- Webhook failures
- OpenAI timeouts
- Database connection issues

---

## Troubleshooting Guide

### Agent Not Responding

**Symptoms**: No response after user message

**Check**:
1. OpenAI API credentials valid?
2. Token limits not exceeded?
3. PostgreSQL connection working?
4. Workflow activated in n8n?
5. Evolution API receiving webhooks?

**Debug**:
- Check n8n execution logs
- Verify webhook received message
- Test OpenAI connection independently
- Check PostgreSQL chat_memory table

### RAG Returns No Results

**Symptoms**: Agent says "don't have that information"

**Check**:
1. Vector store populated with documents?
2. Embeddings generated correctly?
3. Metadata filters too restrictive?
4. Similarity threshold too high?
5. Query too specific or using wrong terms?

**Debug**:
- Test vector search directly in Supabase
- Lower similarity threshold temporarily
- Check document metadata structure
- Verify embedding model consistency

### Wrong Agent Routing

**Symptoms**: Supervisor routes to incorrect agent

**Check**:
1. Supervisor Think Tool output (check logs)
2. Keywords in message match routing rules?
3. Context from memory confusing decision?
4. Routing priority rules configured correctly?

**Debug**:
- Read Supervisor's Think Tool reasoning
- Test message in isolation (new session)
- Verify routing keywords in supervisor prompt
- Check if fallback triggered unintentionally

### Memory Not Persisting

**Symptoms**: Agent forgets previous context

**Check**:
1. PostgreSQL connection stable?
2. Session ID consistent (should be phone number)?
3. Chat memory table created?
4. Permissions adequate?
5. Context window size appropriate?

**Debug**:
- Query chat_memory table directly
- Verify session_id in workflow matches phone
- Check n8n memory node configuration
- Increase context window if too small

### Webhook Not Receiving Messages

**Symptoms**: WhatsApp messages not triggering workflow

**Check**:
1. Evolution API configured correctly?
2. Webhook URL correct and accessible?
3. Instance connected to WhatsApp?
4. Firewall/proxy blocking?
5. SSL certificate valid?

**Debug**:
- Test webhook URL with curl/Postman
- Check Evolution API dashboard
- Verify instance QR code scanned
- Review Evolution API logs

### Media Links Not Returning

**Symptoms**: Sub-workflow doesn't return media

**Check**:
1. Vector store has documents with links?
2. Metadata.links field populated?
3. Link cleaning regex working?
4. Output limit (5) appropriate?
5. Query matching document content?

**Debug**:
- Test sub-workflow independently
- Check vector store documents manually
- Verify links array structure
- Test with known query/loteamento

---

## Critical Rules

### ⚠️ NEVER DO THIS

1. **Never hardcode credentials** in workflows or prompts
2. **Never skip Think Tool** in Supervisor routing decisions
3. **Never invent information** - always use RAG or direct to human
4. **Never change Supervisor fallback** - must always fall back to Agente Geral
5. **Never exceed 3 lines** per agent response (except when providing media links)
6. **Never break session ID** - always use phone number for consistency
7. **Never deploy to production** without testing in dev/staging
8. **Never modify PostgreSQL schema** without backing up first
9. **Never use multiple tools** when only one is needed (e.g., don't call both interesse_lead and lead_qualificado simultaneously unless appropriate)
10. **Never change persona name** - all agents are "Sara" for consistency

### ✅ ALWAYS DO THIS

1. **Always use Think Tool** before important decisions (especially Supervisor)
2. **Always test in isolation** before testing integration
3. **Always check RAG** before saying "I don't have that information"
4. **Always maintain context** - use shared PostgreSQL memory
5. **Always be natural** - agents should sound human, not robotic
6. **Always log decisions** - especially routing decisions in Supervisor
7. **Always have fallback** - every error path should lead somewhere useful
8. **Always qualify gradually** - ONE question at a time
9. **Always monitor interest signals** - don't oversell or push when user is disinterested
10. **Always document changes** - update docs/ when behavior changes

### 🎯 Best Practices

**Prompt Engineering**:
- Be specific and unambiguous
- Provide examples of desired behavior
- Include edge case handling
- Use consistent formatting across all agents
- Test prompts iteratively

**Workflow Design**:
- Keep workflows modular and reusable
- Use descriptive node names
- Implement proper error handling
- Add timeouts to prevent hanging
- Log important intermediate data

**Database Operations**:
- Use indexes for frequently queried fields
- Keep session IDs consistent
- Backup before schema changes
- Monitor query performance
- Sanitize inputs

**RAG & Vector Search**:
- Maintain consistent document structure
- Use clear, searchable content
- Keep metadata accurate and complete
- Test queries for relevance
- Monitor similarity scores

**Testing**:
- Test each layer independently
- Use realistic test data
- Cover happy paths and edge cases
- Validate context preservation
- Check performance under load

---

## Quick Reference

### Key Files for Common Tasks

| Task | Primary Files to Edit |
|------|----------------------|
| Change agent behavior | `prompts/system-messages/agente-[name].md` → Copy to workflow |
| Change routing logic | `prompts/system-messages/agente-supervisor.md` → Copy to workflow |
| Add/modify tools | `prompts/tools/[category].md` + workflow configuration |
| Update knowledge base | Supabase vector store (rag_loteamentos / rag_construtora) |
| Change database schema | PostgreSQL leads table + update tools |
| Add new agent | Create files in prompts/ and workflows/agentes/ + update supervisor |
| Modify media workflow | `workflows/sub-workflows/envio-midia-*.json` |

### Contact Information Used in System

- **Out-of-scope contact**: (19) 2533-0370 (Le Mans Imóveis)
- **Company**: Le Mans Loteamentos e Construtora
- **Agent name**: Sara (consistent across all agents)

### Important Constants

- **Buffer time**: 10 seconds (groups fragmented messages)
- **Max response length**: 3 lines (except media links)
- **RAG TopK**: 5 for loteamentos, 4 for construtora
- **Media output limit**: 5 links maximum
- **Session ID format**: Phone number (e.g., "5519999999999")
- **Timezone**: America/Sao_Paulo

---

## Additional Resources

### Documentation Files

- **Architecture**: `docs/arquitetura-sistema.md` - Deep dive into system design
- **Flows**: `docs/fluxo-atendimento.md` - Customer journey and agent interactions
- **Setup**: `docs/instalacao-configuracao.md` - Installation and configuration guide
- **Prompts Index**: `prompts/README.md` - Complete prompt catalog
- **Flow Diagram**: `assets/diagramas/fluxo-sistema.txt` - ASCII architecture diagram

### External Dependencies Documentation

- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Supabase Vector Guide](https://supabase.com/docs/guides/ai)
- [Evolution API Docs](https://doc.evolution-api.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-14 | Initial CLAUDE.md creation - comprehensive guide for AI assistants |

---

**Maintained by**: Fellipe Saraiva
**Last Updated**: November 2025
**Status**: Production-ready system with active maintenance

---

## Notes for AI Assistants

When working with this codebase:

1. **Start with docs/**: Always read `arquitetura-sistema.md` and `fluxo-atendimento.md` first to understand the business context
2. **prompts/ is source of truth**: The markdown files in prompts/ directory represent the desired agent behavior
3. **Test before deploying**: This is a production system handling real customer interactions
4. **Maintain persona consistency**: All agents are "Sara" - never break this
5. **Think like a user**: This system serves real estate customers, so responses must be natural and helpful
6. **Ask if unsure**: When routing or behavior logic is unclear, ask the human developer for clarification

**Remember**: This system directly impacts Le Mans' sales pipeline and customer experience. Quality and reliability are paramount.

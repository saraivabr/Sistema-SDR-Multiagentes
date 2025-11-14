# Sistema SDR Multi-Agentes - Le Mans

## 📋 Visão Geral

Sistema inteligente de SDR (Sales Development Representative) desenvolvido para a Le Mans utilizando múltiplos agentes de IA especializados em n8n. O sistema processa mensagens via WhatsApp através da Evolution API e distribui automaticamente para agentes especializados em loteamentos, construção ou atendimento geral.

## 🏗️ Arquitetura do Sistema

### Fluxo Principal
```
WhatsApp → Evolution API → Agente Supervisor → Agentes Especializados
```

### Componentes Principais

#### 🎯 **Agente Supervisor**
Router inteligente que analisa o contexto e direciona mensagens para o agente apropriado

#### 👥 **Agentes Especializados**
- **Agente Geral**: Atendimento inicial e direcionamento
- **Agente Loteamentos**: Especialista em terrenos e loteamentos  
- **Agente Construtora**: Especialista em projetos de construção

#### 🔧 **Sub-workflows**
- **Envio de Mídia Construtora**: Busca e envia materiais de portfólios
- **Envio de Mídia Loteamentos**: Busca e envia materiais por loteamento específico

## 📁 Estrutura do Repositório

```
├── docs/                           # Documentação técnica
├── workflows/                      # Workflows n8n organizados
│   ├── principal/                  # Workflow principal WhatsApp
│   ├── agentes/                    # Agentes especializados
│   └── sub-workflows/              # Sub-workflows de apoio
├── prompts/                        # Prompts organizados por categoria
│   ├── system-messages/            # Prompts dos agentes principais
│   ├── tools/                      # Prompts das ferramentas
│   └── sub-workflows/              # Prompts dos sub-workflows
└── assets/                         # Recursos e diagramas
```

## 🚀 Funcionalidades

### ✨ **Atendimento Inteligente**
- Roteamento automático baseado em intenção
- Memória compartilhada entre agentes
- Classificação de mensagens (texto/áudio/imagem/documento)
- Buffer de 10 segundos para mensagens quebradas

### 🎯 **Especialização por Área**
- **Loteamentos**: Consulta de terrenos, condições, localização
- **Construção**: Projetos personalizados, orçamentos, processos
- **Geral**: Triagem inicial, direcionamento para outros canais

### 📊 **Gestão de Leads**
- Cadastro automático de leads
- Classificação de interesse
- Anotações para vendedores
- Qualificação para especialistas

### 🎥 **Envio Inteligente de Mídia**
- Busca contextual em portfólios
- Filtragem por tipo de mídia (foto/vídeo)
- Máximo 5 itens por solicitação
- Segmentação por loteamento específico

## 🛠️ Tecnologias Utilizadas

- **n8n**: Automação de workflows
- **OpenAI GPT-4**: Modelos de linguagem
- **PostgreSQL**: Memória e armazenamento de leads
- **Supabase**: Vector store para RAG
- **Evolution API**: Integração WhatsApp
- **Embeddings OpenAI**: Busca semântica

## 📖 Documentação

- [Arquitetura do Sistema](docs/arquitetura-sistema.md)
- [Fluxo de Atendimento](docs/fluxo-atendimento.md)
- [Instalação e Configuração](docs/instalacao-configuracao.md)

## 🎯 Casos de Uso

### **Atendimento Típico - Loteamentos**
1. Cliente envia mensagem: "Quero comprar um terreno"
2. Agente Supervisor direciona para Agente Loteamentos
3. Agente coleta informações (região, tamanho, finalidade)
4. Envia materiais visuais do loteamento de interesse
5. Qualifica e conecta com especialista humano

### **Atendimento Típico - Construção**
1. Cliente: "Quero construir uma casa personalizada"
2. Direcionamento para Agente Construtora
3. Coleta de requisitos (tamanho, estilo, terreno)
4. Apresenta portfólio de projetos similares
5. Agenda conversa com especialista técnico

## 🔍 Prompts e Engenharia

Todos os prompts foram cuidadosamente desenvolvidos e estão organizados na pasta `prompts/` para fácil consulta e manutenção:

- **System Messages**: Personalidade e comportamento dos agentes
- **Tools**: Descrições das ferramentas disponíveis
- **Sub-workflows**: Lógica dos processos auxiliares

## 📊 Métricas e Performance

- **Tempo de resposta**: < 3 segundos para classificação
- **Precisão de roteamento**: > 95% para intenções claras
- **Retenção de contexto**: Memória completa da conversa
- **Qualificação**: Leads direcionados com contexto preservado

---

**Desenvolvido por**: [Seu Nome]  
**Data**: Agosto 2025  
**Versão**: 1.0
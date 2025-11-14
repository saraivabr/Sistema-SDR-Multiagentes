# 📝 Índice Completo de Prompts - Sistema SDR Le Mans

## 🎯 Visão Geral

Este diretório contém todos os prompts utilizados no sistema SDR da Le Mans, organizados por categoria para facilitar consulta, manutenção e análise. Cada prompt foi cuidadosamente desenvolvido para garantir comportamento específico e eficaz dos agentes.

## 📁 Estrutura de Organização

```
prompts/
├── system-messages/     # Prompts principais dos agentes
├── tools/              # Prompts das ferramentas
└── sub-workflows/      # Prompts dos sub-workflows
```

## 🤖 System Messages - Agentes Principais

### [Agente Supervisor](system-messages/agente-supervisor.md)
**Função**: Router inteligente que distribui mensagens  
**Características**:
- Análise obrigatória com Think Tool
- 4 níveis de prioridade de roteamento
- Fallback robusto para Agente Geral
- Protocolo de tratamento de erros

**Palavras-chave de roteamento**:
- Loteamentos: "terreno", "lote", "loteamento"
- Construção: "construir", "casa", "projeto"
- Geral: primeira mensagem, outros assuntos

---

### [Agente Geral](system-messages/agente-geral.md)
**Função**: Atendimento inicial e direcionamento  
**Persona**: Sara - acolhedora, profissional, empática  
**Características**:
- Coleta nome do usuário
- Direciona para canais apropriados
- Script específico para WhatsApp (19) 2533-0370
- Transição suave para agentes especializados

**Fluxo típico**:
1. Saudação + coleta de nome
2. Identificação de necessidade
3. Direcionamento ou transição

---

### [Agente Loteamentos](system-messages/agente-loteamentos.md)
**Função**: Consultoria especializada em terrenos  
**Persona**: Sara - consultiva, natural, não vendedora  
**Características**:
- UMA pergunta por vez
- Reconhecimento de sinais de interesse
- Transição natural para especialista
- Máximo 3 linhas por resposta

**Sinais de controle**:
- 🟢 Interesse ativo: continuar qualificando
- 🟡 Satisfação aparente: verificar dúvidas
- 🔴 Desinteresse: pausar e aguardar

---

### [Agente Construtora](system-messages/agente-construtora.md)
**Função**: Consultoria especializada em construção  
**Persona**: Sara - consultiva, técnica, orientadora  
**Características**:
- Mesmo padrão do Agente Loteamentos
- Foco em projetos personalizados
- Qualificação técnica específica
- Apresentação de portfólio

## 🛠️ Tools - Ferramentas do Sistema

### [Operações de Banco de Dados](tools/database-operations.md)
**Ferramentas incluídas**:
- `cadastro_lead`: Registro inicial do usuário
- `anotacao_lead`: Anotações para vendedores (250 chars)
- `interesse_lead`: Classificação de interesse
- `lead_qualificado`: Marcação para especialistas

**Uso crítico**: Apenas uma ferramenta por situação específica

---

### [Consultas RAG](tools/rag-queries.md)
**Bases de conhecimento**:
- `rag_loteamentos`: TopK=5, informações de terrenos
- `rag_construtora`: TopK=4, informações técnicas

**Diretrizes importantes**:
- NUNCA inventar informações
- Direcionar para (19) 2533-0370 quando não encontrar
- Usar para embasar respostas precisas

---

### [Workflows de Mídia](tools/media-workflows.md)
**Sub-workflows disponíveis**:
- `envio_midia_construtora`: Portfolio geral (query)
- `envio_midia_loteamentos`: Por loteamento (query + loteamento)

**Limitações**:
- Máximo 5 links por consulta
- Filtragem automática por relevância
- Limpeza de URLs automática

---

### [Ferramentas de Pensamento](tools/thinking-tools.md)
**Think Tool**:
- Pausa obrigatória para reflexão
- Invisível ao usuário
- Processo estruturado de análise
- Fundamental para qualidade

**Quando usar**:
- Supervisor: SEMPRE antes de rotear
- Agentes: Antes de cada resposta importante

## 🔄 Sub-workflows - Processamento de Mídia

### [Envio de Mídia Construtora](sub-workflows/envio-midia-construtora.md)
**Processo**:
1. Busca em `rag_construtora`
2. Acesso a `metadata.links`
3. Limpeza de prefixos e comentários
4. Filtragem por query do usuário
5. Retorno de até 5 links

**Exemplos de query**: "vídeos", "fotos de fachada", "todas as mídias"

---

### [Envio de Mídia Loteamentos](sub-workflows/envio-midia-loteamentos.md)
**Processo específico**:
1. Busca filtrada por loteamento
2. Filtros: `content='MÍDIAS'` + `loteamento=específico`
3. Mesmo processo de limpeza
4. Máximo 5 links segmentados

**Diferencial**: Precisão por empreendimento específico

## 🎨 Padrões de Engenharia de Prompt

### Estrutura Comum dos Agentes
```markdown
# Role: Definição clara da função
# Goal: Objetivo específico
# Backstory: Contexto da Le Mans
# Core Instructions: Comportamentos fundamentais
# Communication Protocol: Tom e estilo
# Tools Usage: Quando e como usar ferramentas
# Quality Control: Regras de qualidade
# Additional Context: Variáveis dinâmicas
```

### Diretrizes Universais
- **Naturalidade**: Falar como pessoa real
- **Consistência**: Manter contexto entre agentes
- **Eficiência**: Respostas concisas e diretas
- **Qualidade**: Think Tool para decisões importantes
- **Segurança**: Nunca inventar informações

### Variáveis de Sistema
```javascript
{{ $json.sessionId }}    // Telefone do usuário
{{ $json.chatInput }}    // Mensagem atual
{{ $json.instancia }}    // Instância Evolution API
{{ new Date().toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' }) }}
```

## 📊 Análise de Qualidade dos Prompts

### Métricas de Avaliação
- **Clareza**: Instruções inequívocas
- **Completude**: Cobertura de cenários
- **Especificidade**: Comportamentos precisos
- **Flexibilidade**: Adaptação a contextos
- **Robustez**: Tratamento de exceções

### Pontos Fortes Identificados
✅ **Segmentação clara** por especialidade  
✅ **Protocolo de fallback** bem definido  
✅ **Controle de fluxo** com sinais de usuário  
✅ **Integração** entre agentes preservando contexto  
✅ **Qualidade técnica** com Think Tool obrigatório  

### Características Avançadas
🎯 **Roteamento inteligente** com 4 níveis de prioridade  
🎭 **Personas consistentes** mantendo "Sara" como identidade  
🔄 **Workflows modulares** com sub-processos especializados  
📊 **Métricas integradas** para avaliação contínua  
🛡️ **Tratamento de erro** robusto em todos os níveis  

## 🔧 Manutenção e Evolução

### Diretrizes para Modificação
1. **Testar isoladamente** antes de deploy
2. **Manter consistência** de persona e tom
3. **Documentar mudanças** e razões
4. **Validar integração** entre agentes
5. **Monitorar performance** pós-mudança

### Versionamento
- Controle de versão dos prompts
- Log de modificações com justificativa
- Backup antes de alterações significativas
- A/B testing para otimizações

---

**📍 Localização**: Este índice serve como ponto central para consulta de todos os prompts do sistema. Para detalhes específicos, consulte os arquivos individuais em cada categoria.
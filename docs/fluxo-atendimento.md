# Fluxo de Atendimento - Sistema SDR Le Mans

## 🎯 Visão Geral do Atendimento

O sistema SDR da Le Mans implementa um fluxo de atendimento inteligente que processa automaticamente as mensagens dos clientes e os direciona para especialistas adequados, mantendo uma experiência natural e consultiva.

## 📱 Jornada do Cliente

### 1. Primeiro Contato
```
Cliente envia mensagem → WhatsApp → Evolution API → Sistema SDR
```

**Processamento Inicial:**
- Recepção via webhook
- Classificação do tipo de mensagem
- Processamento de áudio/imagem se necessário
- Buffer de 10 segundos para mensagens fragmentadas

### 2. Roteamento Inteligente
```
Mensagem processada → Agente Supervisor → Análise → Decisão de roteamento
```

**Critérios de Decisão:**
- **Nova conversa**: Sempre → Agente Geral
- **Continuação**: Manter agente atual (se apropriado)
- **Mudança de assunto**: Novo roteamento
- **Interesse específico**: Agente especializado

### 3. Atendimento Especializado
```
Agente escolhido → Análise + Contexto → Resposta personalizada → Cliente
```

## 🎭 Fluxos por Tipo de Agente

### 🔄 Agente Supervisor - Router
**Processo de Decisão:**

1. **Think Tool Obrigatório**
   - Análise da mensagem atual
   - Revisão do histórico
   - Identificação do contexto

2. **Classificação de Intenção**
   - Primeira mensagem → Agente Geral
   - "terreno", "loteamento" → Agente Loteamentos
   - "construir", "casa", "projeto" → Agente Construtora
   - Outros assuntos → Agente Geral

3. **Execução do Roteamento**
   - Chamada do agente apropriado
   - Transferência de contexto
   - Monitoramento de resposta

### 👋 Agente Geral - Triagem e Direcionamento

**Fluxo Típico:**

1. **Saudação Inicial**
   ```
   "Oi! Tudo bem? 😊
   Meu nome é Sara, sou da Le Mans.
   Qual é o seu nome?"
   ```

2. **Coleta de Nome**
   - Ativa tool `cadastro_lead`
   - Registra na base de dados
   - Confirma recebimento

3. **Identificação de Necessidade**
   ```
   "Prazer, [Nome]!
   Como posso te ajudar hoje?"
   ```

4. **Análise de Resposta**
   - **Loteamentos/Construção**: Transição suave para especialista
   - **Outros assuntos**: Script de direcionamento para (19) 2533-0370
   - **Dúvida**: Perguntas de qualificação

5. **Finalização**
   - Tool `anotacao_lead` com resumo
   - Transição ou encerramento educado

### 🏞️ Agente Loteamentos - Especialista em Terrenos

**Fluxo Consultivo:**

1. **Recepção Calorosa**
   ```
   "[Nome], que bom que você tem interesse em loteamentos!
   Nossa especialista vai adorar te ajudar com isso."
   ```

2. **Qualificação Gradual** (1 pergunta por vez)
   - Região de preferência
   - Tamanho desejado
   - Finalidade (morar/investir)
   - Prazo para decisão

3. **Apresentação de Opções**
   - Consulta `rag_loteamentos`
   - Informações relevantes
   - Material visual via `envio_midia_loteamentos`

4. **Monitoramento de Sinais**
   - 🟢 **Interesse ativo**: Continue qualificando
   - 🟡 **Satisfação aparente**: "Tem mais alguma dúvida?"
   - 🔴 **Desinteresse**: Pause e aguarde

5. **Transição para Especialista**
   ```
   "[Nome], vi que você tem bastante interesse!
   Se quiser conversar sobre valores específicos e condições de pagamento,
   posso te conectar com nosso especialista. Quer que eu faça essa conexão?"
   ```

6. **Qualificação Final**
   - Tool `interesse_lead` (Loteamentos)
   - Tool `lead_qualificado` (se aceitar especialista)
   - Tool `anotacao_lead` com insights

### 🏗️ Agente Construtora - Especialista em Projetos

**Fluxo Similar ao Loteamentos:**

1. **Recepção Especializada**
   ```
   "[Nome], legal que você quer construir!
   Vou te conectar com nossa especialista."
   ```

2. **Qualificação Técnica**
   - Tipo de projeto desejado
   - Tamanho da casa
   - Situação do terreno
   - Estilo preferido

3. **Apresentação de Portfolio**
   - Consulta `rag_construtora`
   - Projetos similares
   - Material visual via `envio_midia_construtora`

4. **Conexão com Especialista**
   - Mesmo padrão do Agente Loteamentos
   - `interesse_lead` (Construtora)
   - Qualificação e anotações

## 🎥 Sub-fluxos de Mídia

### Envio de Mídia Loteamentos
```
Cliente solicita: "Quero ver fotos do Terra Nova"
↓
Tool: envio_midia_loteamentos
↓
Parâmetros: query="fotos", loteamento="Terra Nova"
↓
Sub-workflow busca e filtra mídias específicas
↓
Retorna até 5 links relevantes
↓
Cliente recebe materiais visuais
```

### Envio de Mídia Construtora
```
Cliente solicita: "Tem fotos de casas que vocês construíram?"
↓
Tool: envio_midia_construtora
↓
Parâmetro: query="fotos de casas"
↓
Sub-workflow busca no portfólio geral
↓
Retorna até 5 links de projetos
↓
Cliente recebe exemplos de trabalhos
```

## 🚨 Cenários de Exceção

### 1. Assuntos Fora do Escopo
```
Cliente: "Vocês têm casa para alugar?"
↓
Agente Geral detecta
↓
Script de direcionamento:
"Para aluguel de imóveis, a equipe da Le Mans Imóveis
tem várias opções disponíveis.
O WhatsApp deles é (19) 2533-0370"
```

### 2. Cliente Não Responde
- Após 2-3 mensagens sem resposta
- Sistema para de enviar mensagens
- Aguarda reativação pelo cliente

### 3. Mudança de Assunto
```
Cliente estava falando de loteamentos
→ Muda para construção
→ Agente Supervisor detecta
→ Redireciona para Agente Construtora
```

### 4. Informação Não Encontrada
```
RAG não retorna resultados relevantes
↓
"Não tenho essa informação específica.
Quer que eu conecte você com nosso especialista
para esclarecer isso?"
```

## 📊 Indicadores de Qualidade

### Métricas de Fluxo
- **Tempo até primeira resposta**: < 3 segundos
- **Taxa de roteamento correto**: > 95%
- **Conversão para especialista**: Meta definida por agente
- **Satisfação subjetiva**: Monitoramento de feedback

### Pontos de Controle
- Resposta inicial do Supervisor
- Primeira interação do agente especializado
- Momento de sugestão de especialista
- Finalização com anotações

## 🔄 Melhorias Contínuas

### Otimizações Implementadas
- Buffer de mensagens para evitar fragmentação
- Think Tool obrigatório para decisões críticas
- Sinais de interesse para timing adequado
- Fallback robusto para cenários não previstos

### Evolução do Sistema
- Análise de logs para padrões
- Ajuste de prompts baseado em performance
- Adição de novos cenários conforme necessário
- Refinamento de critérios de roteamento

---

Este fluxo garante uma experiência natural e eficiente, maximizando a conversão de leads enquanto mantém a qualidade do atendimento humano.
# Tools - Ferramentas de Pensamento

## 1. Think_tool

**Descrição**: Pausa obrigatória para planejamento interno. Reflita passo a passo sobre a última mensagem, o histórico, a etapa atual do atendimento atual e a próxima ação ideal. Não produz saída para o usuário.

**Uso**: Ferramenta de reflexão e planejamento interno
**Visibilidade**: Não produz saída visível para o usuário
**Obrigatório**: Deve ser usado em situações específicas

---

## Quando usar Think_tool por Agente:

### Agente Supervisor
- **SEMPRE** antes de cada decisão de roteamento
- Para analisar contexto completo (mensagem + histórico)
- Para decidir qual agente acionar
- Obrigatório para todo processo de decisão

### Agente Geral
- Quando precisar analisar se deve direcionar ou continuar atendendo
- Quando não tiver certeza sobre qual agente acionar
- Para decidir se o assunto é adequado para este canal
- Antes de fazer transições para outros agentes

### Agente Loteamentos
- Antes de cada resposta para planejar
- Para avaliar sinais do usuário (interesse, desinteresse, satisfação)
- Antes de sugerir especialista
- Para decidir próximos passos baseado no comportamento do usuário

### Agente Construtora
- Antes de cada resposta para planejar
- Para avaliar sinais do usuário (interesse, desinteresse, satisfação)
- Antes de sugerir especialista
- Para decidir próximos passos baseado no comportamento do usuário

---

## Processo de Reflexão

O Think_tool deve seguir este processo estruturado:

1. **Análise da Mensagem Atual**
   - O que o usuário disse?
   - Qual é a intenção por trás da mensagem?

2. **Revisão do Histórico**
   - Qual é o contexto da conversa?
   - Que informações já foram coletadas?
   - Qual foi o tom/interesse demonstrado anteriormente?

3. **Avaliação da Etapa Atual**
   - Em que ponto do atendimento estamos?
   - O usuário está engajado ou demonstrando desinteresse?
   - Já foi fornecida informação suficiente?

4. **Decisão da Próxima Ação**
   - Qual é a melhor resposta?
   - Devo fazer uma pergunta ou finalizar?
   - É momento de sugerir especialista?
   - Preciso direcionar para outro agente/canal?

---

## Importância Estratégica

O Think_tool é fundamental para:
- **Qualidade do Atendimento**: Evita respostas automáticas ou inadequadas
- **Continuidade**: Mantém coerência na conversa
- **Eficiência**: Evita loops desnecessários ou perguntas repetitivas
- **Conversão**: Identifica o momento certo para ações importantes
- **Experiência do Usuário**: Proporciona atendimento mais natural e humano

---

## Nota Importante

Esta ferramenta é **invisível** ao usuário final, servindo apenas como uma pausa reflexiva interna do sistema para garantir respostas mais assertivas e contextualmente apropriadas.
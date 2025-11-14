# Tools - Operações de Banco de Dados

## 1. cadastro_lead

**Descrição**: Chame essa tool assim que o usuário informar o seu nome, para que você salve o nome dele na tabela `leads` na coluna `nome`.

**Uso**: Primeira coleta de dados do lead
**Quando usar**: Apenas na primeira coleta, evite duplicações
**Operação**: UPDATE na tabela `leads`

---

## 2. anotacao_lead

**Descrição**: Chame essa tool ao final do atendimento com o usuário para adicionar anotações sobre a conversa na tabela `leads`, coluna `notas`. Você deve criar uma anotação curta e direta, de no máximo 250 caracteres. Escreva em bullets-points. Escreva a anotação direcionada para o vendedor que irá assumir a conversa posteriormente com o usuário, para que ele tenha insights sobre os interesses do usuário, para que possa ter uma conversa e negociação mais direcionada.

**Uso**: Registro de informações importantes da conversa
**Quando usar**: 
- Finalizar atendimento geral
- Direcionar para outro canal (Le Mans Imóveis)
- Usuário decidir não prosseguir
**Operação**: UPDATE na tabela `leads`, coluna `notas`
**Limite**: Máximo 250 caracteres

---

## 3. lead_qualificado (Agente Loteamentos)

**Descrição**: Chame essa tool quando o usuário desejar falar com um especialista. Na tabela `leads`, coluna `qualificado`, adicione o valor `TRUE`.

**Uso**: Marcar lead como qualificado para especialista
**Quando usar**: APENAS quando usuário aceitar falar com especialista
**Operação**: UPDATE na tabela `leads`, coluna `qualificado` = TRUE

---

## 4. lead_qualificado (Agente Construtora)

**Descrição**: Chame essa tool quando o usuário desejar falar com um especialista. Na tabela `leads`, coluna `qualificado`, adicione o valor `TRUE`.

**Uso**: Marcar lead como qualificado para especialista
**Quando usar**: APENAS quando usuário aceitar falar com especialista
**Operação**: UPDATE na tabela `leads`, coluna `qualificado` = TRUE

---

## 5. interesse_lead (Agente Loteamentos)

**Descrição**: Chame essa tool assim que o lead demonstrar interesse em Loteamentos. Ou seja, após o "Agente de Triagem" perguntar para qual tipo ele deseja atendimento, se o usuário disser que é para "Loteamentos", você deve acionar essa tool e na tabela `leads`, coluna `interesse` adicionar o valor `Loteamentos`.

**Uso**: Registrar interesse específico em loteamentos
**Quando usar**: Quando identificar interesse claro em loteamentos
**Operação**: UPDATE na tabela `leads`, coluna `interesse` = "Loteamentos"

---

## 6. interesse_lead (Agente Construtora)

**Descrição**: Chame essa tool assim que o lead demonstrar interesse em Construções. Ou seja, após o "Agente de Triagem" perguntar para qual tipo ele deseja atendimento, se o usuário disser que é para "Construções", você deve acionar essa tool e na tabela `leads`, coluna `interesse` adicionar o valor `Construtora`.

**Uso**: Registrar interesse específico em construção
**Quando usar**: Quando identificar interesse claro em construção
**Operação**: UPDATE na tabela `leads`, coluna `interesse` = "Construtora"
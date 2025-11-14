# Sub-workflow - Envio de Mídia Loteamentos

## System Message do Agente Buscador de Mídia

Sua missão é identificar e extrair links de mídias relevantes (imagens, vídeos do YouTube, etc.) para um loteamento específico, baseado na solicitação do usuário. Você receberá como entrada uma 'query' (a solicitação original do usuário, ex: "fotos da piscina do Terra Nova") e o nome do 'loteamento' (ex: "Terra Nova").

## Processo de Execução

Siga estes passos rigorosamente:

### 1. Busca Específica no Vector Store
**Utilize a ferramenta `Answer questions with a vector store`** para localizar o ÚNICO documento na base `rag_loteamentos` que contém o compilado de mídias para o `loteamento` fornecido.

#### Configuração da Busca:
- **Query de busca**: Pode ser a `query` original do usuário
- **CRUCIAL**: Aplicar os seguintes filtros de metadados combinados (AND):
  - `content` IGUAL A `'MÍDIAS'`
  - `metadata.loteamento` IGUAL A `{{$json.loteamento}}`

### 2. Processamento do Resultado
A ferramenta retornará um documento. Dentro dele, acesse `metadata.links`. Este é um array de strings, onde cada string é um link, podendo conter um prefixo "- " e um comentário descritivo após "#".

### 3. Limpeza dos Links
Para cada string no array `metadata.links`:
- Remova o prefixo "- " se presente
- Extraia a URL principal, descartando qualquer comentário após o caractere "#"

### 4. Filtragem Inteligente por Loteamento
Com base na `query` original do usuário, selecione APENAS os links que são diretamente relevantes para essa solicitação:

#### Exemplos de Filtragem:
- **Query "vídeo"**: Retorne apenas links de vídeo
- **Query "fotos da piscina"**: Procure por links cujos comentários originais (a parte após '#') ou nomes de arquivo sugiram que são da piscina
- **Query "fotos" ou "imagens"**: Selecione uma variedade de até 5 links de imagem
- **Query "todas as mídias"**: Selecione uma variedade de até 5 links mistos (imagens e vídeos)

### 5. Limitação de Resultados
Você deve retornar no **máximo 5 links de mídia**, entre fotos e vídeos.

## Funcionalidade do Workflow

### Entradas
- `query`: Solicitação específica do usuário sobre que tipo de mídia deseja ver
- `loteamento`: Nome específico do loteamento para busca direcionada

### Processamento
1. Busca direcionada no banco de dados por loteamento específico
2. Aplicação de filtros de metadados para precisão
3. Filtragem baseada na intenção do usuário
4. Limpeza e formatação dos links
5. Seleção dos mais relevantes

### Saída
- Lista de até 5 links de mídia filtrados e relevantes para o loteamento específico
- Links limpos (sem prefixos ou comentários)
- Adequados à solicitação específica do usuário

## Casos de Uso

### Típicas Solicitações:
- "Quero ver fotos do Terra Nova"
- "Tem vídeo da área de lazer do Residencial Santos?"
- "Mostra imagens da infraestrutura do loteamento"
- "Fotos da piscina do [Nome do Loteamento]"
- "Vídeo de drone do [Nome do Loteamento]"

### Tratamento Específico por Loteamento:
- **Busca direcionada**: Cada loteamento tem seu próprio conjunto de mídias
- **Filtros rigorosos**: Garante que apenas mídias do loteamento específico sejam retornadas
- **Contexto preservado**: Mantém a relação entre query e loteamento solicitado

## Diferencial em Relação ao Workflow da Construtora

### Especificidade:
- Requer identificação do loteamento específico
- Aplica filtros de metadados mais rigorosos
- Trabalha com estrutura de dados segmentada por loteamento

### Precisão:
- Evita mistura de mídias entre diferentes loteamentos
- Garante relevância específica ao projeto solicitado
- Mantém organização por empreendimento

## Integração com Sistema Principal

Este sub-workflow é chamado pelo **Agente Loteamentos** através da tool `envio_midia_loteamentos` quando o usuário solicita materiais visuais relacionados a loteamentos específicos.
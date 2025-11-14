# Tools - Workflows de Mídia

## 1. envio_midia_construtora

**Descrição**: Chame essa tool sempre que o usuário pedir alguma imagem ou vídeo de alguma construção que já foi feita. Essa tool será responsável por buscar a mídia e enviar para o usuário.

**Parâmetros necessários**:
- `query`: O que o usuário deseja ver

**Uso**: Envio de materiais visuais de projetos da construtora
**Quando usar**: Quando usuário solicitar imagens, vídeos ou exemplos de construções
**Sub-workflow**: Conecta ao workflow de envio de mídia da construtora
**Workflow ID**: iOrWflyc6Dd8r7YU

---

## 2. envio_midia_loteamentos

**Descrição**: Chame essa tool sempre que o usuário pedir alguma imagem ou vídeo de algum loteamento. Essa tool será responsável por buscar a mídia e enviar para o usuário.

**Parâmetros necessários**:
- `query`: O que o usuário deseja ver
- `loteamento`: Qual loteamento o usuário deseja ver as imagens ou vídeos

**Uso**: Envio de materiais visuais de loteamentos específicos
**Quando usar**: Quando usuário solicitar imagens, vídeos ou materiais de loteamentos
**Sub-workflow**: Conecta ao workflow de envio de mídia de loteamentos
**Workflow ID**: iOrWflyc6Dd8r7YU

---

## Diretrizes de Uso

### Para envio_midia_construtora:
- Use quando o usuário quiser ver exemplos do trabalho da construtora
- Exemplos de queries: "fotos de casas prontas", "vídeos de obras", "exemplos de projetos"
- A tool automaticamente busca e filtra as mídias relevantes

### Para envio_midia_loteamentos:
- Use quando o usuário quiser ver materiais específicos de um loteamento
- Sempre informe o nome específico do loteamento
- Exemplos de queries: "fotos da área de lazer", "vídeo do Terra Nova", "imagens da infraestrutura"

### Limitações:
- Máximo 5 links de mídia retornados por consulta
- Mistura entre fotos e vídeos conforme disponibilidade
- Filtragem automática baseada na query do usuário

### Integração com Sistema:
- Ambas as tools são sub-workflows que executam de forma assíncrona
- Retornam links diretos para as mídias solicitadas
- Integradas com o sistema de RAG para localização precisa dos materiais
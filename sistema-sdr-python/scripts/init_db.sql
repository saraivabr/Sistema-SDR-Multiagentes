-- Script de inicialização do banco de dados PostgreSQL
-- Sistema SDR Multi-Agentes - Le Mans

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de leads
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    telefone VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(100),
    interesse VARCHAR(50),
    qualificado BOOLEAN DEFAULT FALSE NOT NULL,
    notas VARCHAR(250),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_leads_telefone ON leads(telefone);
CREATE INDEX IF NOT EXISTS idx_leads_qualificado ON leads(qualificado);
CREATE INDEX IF NOT EXISTS idx_leads_interesse ON leads(interesse);

-- Comentários nas colunas
COMMENT ON TABLE leads IS 'Tabela de leads capturados pelo sistema';
COMMENT ON COLUMN leads.telefone IS 'Telefone do lead (sessionId) - formato: 5519999999999';
COMMENT ON COLUMN leads.nome IS 'Nome do lead coletado pelo agente';
COMMENT ON COLUMN leads.interesse IS 'Área de interesse: Loteamentos, Construtora, etc.';
COMMENT ON COLUMN leads.qualificado IS 'Lead qualificado para contato com especialista';
COMMENT ON COLUMN leads.notas IS 'Anotações sobre a conversa (máx 250 chars)';

-- Tabela de histórico de mensagens (chat memory)
CREATE TABLE IF NOT EXISTS chat_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    agent_name VARCHAR(50),
    metadata TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índices para chat memory
CREATE INDEX IF NOT EXISTS idx_chat_memory_session ON chat_memory(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_memory_timestamp ON chat_memory(timestamp);
CREATE INDEX IF NOT EXISTS idx_chat_memory_agent ON chat_memory(agent_name);

-- Comentários
COMMENT ON TABLE chat_memory IS 'Histórico de mensagens do chat';
COMMENT ON COLUMN chat_memory.session_id IS 'ID da sessão (telefone do usuário)';
COMMENT ON COLUMN chat_memory.role IS 'Role: user, assistant, system, function';
COMMENT ON COLUMN chat_memory.content IS 'Conteúdo da mensagem';
COMMENT ON COLUMN chat_memory.agent_name IS 'Nome do agente que gerou a mensagem';
COMMENT ON COLUMN chat_memory.metadata IS 'Metadata adicional em JSON';

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Dados de exemplo (opcional - comentar em produção)
-- INSERT INTO leads (telefone, nome, interesse, qualificado, notas)
-- VALUES
--     ('5519999999999', 'João Silva', 'Loteamentos', FALSE, 'Interessado em terreno na região Norte'),
--     ('5519888888888', 'Maria Santos', 'Construtora', TRUE, 'Quer orçamento para casa 150m²')
-- ON CONFLICT (telefone) DO NOTHING;

-- Fim do script

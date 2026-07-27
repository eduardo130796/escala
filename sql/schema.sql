-- ==========================================
-- SISTEMA DE ESCALAS
-- Versão 1.1
-- ==========================================

DROP TABLE IF EXISTS escalas CASCADE;
DROP TABLE IF EXISTS servidores CASCADE;
DROP TABLE IF EXISTS configuracoes CASCADE;

------------------------------------------------
-- CONFIGURAÇÕES
------------------------------------------------

CREATE TABLE configuracoes (

    id INTEGER PRIMARY KEY,

    mes SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),

    ano SMALLINT NOT NULL,

    max_dias_por_servidor SMALLINT NOT NULL DEFAULT 2,

    bloqueado BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()

);

INSERT INTO configuracoes
(id, mes, ano, max_dias_por_servidor, bloqueado)
VALUES
(1, 8, 2026, 2, FALSE);

------------------------------------------------
-- SERVIDORES
------------------------------------------------

CREATE TABLE servidores (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    nome TEXT NOT NULL,

    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    ordem INTEGER NOT NULL DEFAULT 0,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()

);

------------------------------------------------
-- ESCALAS
------------------------------------------------

CREATE TABLE escalas (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    servidor_id BIGINT NOT NULL
        REFERENCES servidores(id)
        ON DELETE CASCADE,

    data DATE NOT NULL,

    confirmado BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_servidor_data
        UNIQUE (servidor_id, data)

);

------------------------------------------------
-- ÍNDICES
------------------------------------------------

CREATE INDEX idx_escalas_data
ON escalas(data);

CREATE INDEX idx_escalas_servidor
ON escalas(servidor_id);
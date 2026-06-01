-- Schema principal do sistema de produção Moura

CREATE SCHEMA IF NOT EXISTS producao;
CREATE SCHEMA IF NOT EXISTS vendas;
CREATE SCHEMA IF NOT EXISTS manutencao;

-- Tabela de produtos
CREATE TABLE producao.produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    descricao TEXT,
    peso_kg DECIMAL(10,2),
    preco_custo DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de ordens de produção
CREATE TABLE producao.ordens_producao (
    id_ordem SERIAL PRIMARY KEY,
    id_produto INT REFERENCES producao.produtos(id_produto),
    quantidade_planejada INT NOT NULL,
    quantidade_produzida INT DEFAULT 0,
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente','em_andamento','concluida','cancelada')),
    prioridade INT DEFAULT 0,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de vendas
CREATE TABLE vendas.vendas (
    id_venda SERIAL PRIMARY KEY,
    id_produto INT REFERENCES producao.produtos(id_produto),
    quantidade INT NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total DECIMAL(10,2) GENERATED ALWAYS AS (quantidade * valor_unitario) STORED,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    regiao VARCHAR(50),
    canal_venda VARCHAR(30),
    vendedor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de manutenção
CREATE TABLE manutencao.manutencoes (
    id_manutencao SERIAL PRIMARY KEY,
    maquina VARCHAR(20) NOT NULL,
    tipo VARCHAR(20) CHECK (tipo IN ('preventiva','corretiva','preditiva')),
    data_agendada DATE,
    data_realizada DATE,
    tecnico_responsavel VARCHAR(100),
    duracao_horas DECIMAL(5,2),
    custo DECIMAL(10,2),
    descricao TEXT,
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente','em_andamento','concluido','cancelado')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_ordens_status ON producao.ordens_producao(status);
CREATE INDEX idx_vendas_data ON vendas.vendas(data_venda);
CREATE INDEX idx_vendas_regiao ON vendas.vendas(regiao);
CREATE INDEX idx_manutencao_maquina ON manutencao.manutencoes(maquina);
CREATE INDEX idx_manutencao_status ON manutencao.manutencoes(status);

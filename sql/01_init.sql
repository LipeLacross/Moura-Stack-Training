-- Tabela base
CREATE TABLE IF NOT EXISTS sales (
  order_id    SERIAL PRIMARY KEY,
  region      TEXT NOT NULL,
  product     TEXT NOT NULL,
  quantity    INT  NOT NULL,
  unit_price  NUMERIC(12,2) NOT NULL,
  total       NUMERIC(14,2)  -- será preenchido por trigger
);

-- Função/Trigger para manter total = quantity * unit_price
CREATE OR REPLACE FUNCTION set_total() RETURNS trigger AS $$
BEGIN
  NEW.total := NEW.quantity * NEW.unit_price;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_set_total ON sales;
CREATE TRIGGER trg_set_total
BEFORE INSERT OR UPDATE ON sales
FOR EACH ROW EXECUTE PROCEDURE set_total();

-- Tabela agregada (exemplo)
CREATE TABLE IF NOT EXISTS product_revenue (
  product TEXT PRIMARY KEY,
  revenue NUMERIC(18,2) NOT NULL DEFAULT 0
);

-- Procedure para consolidar receita por produto
CREATE OR REPLACE PROCEDURE upsert_product_revenue()
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO product_revenue(product, revenue)
  SELECT product, SUM(total) FROM sales GROUP BY product
  ON CONFLICT (product) DO UPDATE SET revenue = EXCLUDED.revenue;
END;
$$;

-- Dados de exemplo (amostra expandida)
INSERT INTO sales (region, product, quantity, unit_price) VALUES
('Norte','Bateria A',10,200),
('Sul','Bateria B',5,350),
('Nordeste','Bateria C',8,180),
('Sudeste','Bateria D',12,220),
('Centro-Oeste','Bateria E',7,210),
('Norte','Bateria F',15,195),
('Sul','Bateria G',9,340),
('Nordeste','Bateria H',6,175),
('Sudeste','Bateria I',11,230),
('Centro-Oeste','Bateria J',13,205),
('Norte','Bateria K',14,215),
('Sul','Bateria L',8,360),
('Nordeste','Bateria M',10,185),
('Sudeste','Bateria N',7,225),
('Centro-Oeste','Bateria O',9,200),
('Norte','Bateria P',16,210),
('Sul','Bateria Q',12,355),
('Nordeste','Bateria R',5,170),
('Norte','Bateria A',7,200),
('Sul','Bateria A',5,200),
('Sudeste','Bateria B',10,350),
('Centro-Oeste','Bateria B',6,350),
('Nordeste','Bateria C',9,180),
('Sul','Bateria C',4,180),
('Norte','Bateria D',8,220),
('Sul','Bateria E',6,210),
('Nordeste','Bateria F',12,195),
('Sudeste','Bateria G',7,340),
('Centro-Oeste','Bateria H',10,175),
('Norte','Bateria I',9,230),
('Sul','Bateria J',11,205),
('Nordeste','Bateria K',13,215),
('Sudeste','Bateria L',14,360),
('Centro-Oeste','Bateria M',8,185),
('Norte','Bateria N',10,225),
('Sul','Bateria O',7,200),
('Nordeste','Bateria P',9,210),
('Sudeste','Bateria Q',15,355),
('Centro-Oeste','Bateria R',5,170),
('Norte','Bateria A',12,200),
('Sul','Bateria B',8,350),
('Nordeste','Bateria C',6,180),
('Sudeste','Bateria D',13,220),
('Centro-Oeste','Bateria E',9,210),
('Norte','Bateria F',11,195),
('Sul','Bateria G',10,340),
('Nordeste','Bateria H',7,175),
('Sudeste','Bateria I',12,230),
('Centro-Oeste','Bateria J',14,205)
ON CONFLICT DO NOTHING;

-- Chamar a procedure (opcional)
-- CALL upsert_product_revenue();

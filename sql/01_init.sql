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
('Sudeste','Bateria S',14,240),
('Centro-Oeste','Bateria T',10,215),
('Norte','Bateria U',13,205),
('Sul','Bateria V',11,345),
('Nordeste','Bateria W',8,180),
('Sudeste','Bateria X',9,225),
('Centro-Oeste','Bateria Y',15,210),
('Norte','Bateria Z',7,220),
('Sul','Bateria AA',10,330),
('Nordeste','Bateria AB',12,190),
('Sudeste','Bateria AC',8,235),
('Centro-Oeste','Bateria AD',14,200),
('Norte','Bateria AE',9,215),
('Sul','Bateria AF',13,370),
('Nordeste','Bateria AG',11,185),
('Sudeste','Bateria AH',15,250),
('Centro-Oeste','Bateria AI',12,220),
('Norte','Bateria AJ',10,210),
('Sul','Bateria AK',14,355),
('Nordeste','Bateria AL',9,175),
('Sudeste','Bateria AM',13,245),
('Centro-Oeste','Bateria AN',11,215),
('Norte','Bateria AO',8,205),
('Sul','Bateria AP',15,340),
('Nordeste','Bateria AQ',7,180),
('Sudeste','Bateria AR',12,230),
('Centro-Oeste','Bateria AS',10,200),
('Norte','Bateria AT',11,215),
('Sul','Bateria AU',9,360),
('Nordeste','Bateria AV',14,185),
('Sudeste','Bateria AW',8,255),
('Centro-Oeste','Bateria AX',13,210)
ON CONFLICT DO NOTHING;

-- Chamar a procedure (opcional)
-- CALL upsert_product_revenue();

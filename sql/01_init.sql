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

-- Dados de exemplo
INSERT INTO sales (region, product, quantity, unit_price) VALUES
('Norte','Bateria A',10,200),
('Sul','Bateria B',5,350),
('Nordeste','Bateria C',8,180)
ON CONFLICT DO NOTHING;

-- Chamar a procedure (opcional)
-- CALL upsert_product_revenue();

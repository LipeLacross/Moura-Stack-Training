-- Tabela base
CREATE TABLE IF NOT EXISTS sales (
  order_id    SERIAL PRIMARY KEY,
  region      TEXT NOT NULL,
  product     TEXT NOT NULL,
  quantity    INT  NOT NULL,
  unit_price  NUMERIC(12,2) NOT NULL,
  total       NUMERIC(14,2),
  date        DATE NOT NULL DEFAULT CURRENT_DATE
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
INSERT INTO sales (region, product, quantity, unit_price, date) VALUES
('Norte','Bateria A',10,200,'2025-08-01'),
('Sul','Bateria B',5,350,'2025-08-02'),
('Nordeste','Bateria C',8,180,'2025-08-03'),
('Sudeste','Bateria D',12,220,'2025-08-04'),
('Centro-Oeste','Bateria E',7,210,'2025-08-05'),
('Norte','Bateria F',15,195,'2025-08-06'),
('Sul','Bateria G',9,340,'2025-08-07'),
('Nordeste','Bateria H',6,175,'2025-08-08'),
('Sudeste','Bateria I',11,230,'2025-08-09'),
('Centro-Oeste','Bateria J',13,205,'2025-08-10'),
('Norte','Bateria K',14,215,'2025-08-11'),
('Sul','Bateria L',8,360,'2025-08-12'),
('Nordeste','Bateria M',10,185,'2025-08-13'),
('Sudeste','Bateria N',7,225,'2025-08-14'),
('Centro-Oeste','Bateria O',9,200,'2025-08-15'),
('Norte','Bateria P',16,210,'2025-08-16'),
('Sul','Bateria Q',12,355,'2025-08-17'),
('Nordeste','Bateria R',5,170,'2025-08-18'),
('Norte','Bateria A',7,200,'2025-08-19'),
('Sul','Bateria A',5,200,'2025-08-20'),
('Sudeste','Bateria B',10,350,'2025-08-21'),
('Centro-Oeste','Bateria B',6,350,'2025-08-22'),
('Nordeste','Bateria C',9,180,'2025-08-23'),
('Sul','Bateria C',4,180,'2025-08-24'),
('Norte','Bateria D',8,220,'2025-08-25'),
('Sul','Bateria E',6,210,'2025-08-26'),
('Nordeste','Bateria F',12,195,'2025-08-27'),
('Sudeste','Bateria G',7,340,'2025-08-28'),
('Centro-Oeste','Bateria H',10,175,'2025-08-29'),
('Norte','Bateria I',9,230,'2025-08-30'),
('Sul','Bateria J',11,205,'2025-08-31'),
('Nordeste','Bateria K',13,215,'2025-09-01'),
('Sudeste','Bateria L',14,360,'2025-09-02'),
('Centro-Oeste','Bateria M',8,185,'2025-09-03'),
('Norte','Bateria N',10,225,'2025-09-04'),
('Sul','Bateria O',7,200,'2025-09-05'),
('Nordeste','Bateria P',9,210,'2025-09-06'),
('Sudeste','Bateria Q',15,355,'2025-09-07'),
('Centro-Oeste','Bateria R',5,170,'2025-09-08'),
('Norte','Bateria A',12,200,'2025-09-09'),
('Sul','Bateria B',8,350,'2025-09-10'),
('Nordeste','Bateria C',6,180,'2025-09-11'),
('Sudeste','Bateria D',13,220,'2025-09-12'),
('Centro-Oeste','Bateria E',9,210,'2025-09-13'),
('Norte','Bateria F',11,195,'2025-09-14'),
('Sul','Bateria G',10,340,'2025-09-15'),
('Nordeste','Bateria H',7,175,'2025-09-16'),
('Sudeste','Bateria I',12,230,'2025-09-17'),
('Centro-Oeste','Bateria J',14,205,'2025-09-18')
ON CONFLICT DO NOTHING;

-- Chamar a procedure (opcional)
-- CALL upsert_product_revenue();

-- Tabela base
CREATE TABLE IF NOT EXISTS sales (
  order_id    SERIAL PRIMARY KEY,
  region      TEXT NOT NULL,
  product     TEXT NOT NULL,
  quantity    INT  NOT NULL,
  unit_price  NUMERIC(12,2) NOT NULL,
  total       NUMERIC(14,2),
  date        DATE NOT NULL DEFAULT CURRENT_DATE,
  customer_id INT,
  status      TEXT DEFAULT 'paid',
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes       TEXT,
  user_id     INT,
  category    TEXT,
  payment_method TEXT
);

-- Função/Trigger para manter total = quantity * unit_price
CREATE OR REPLACE FUNCTION set_total() RETURNS trigger AS $$
BEGIN
  NEW.total := NEW.quantity * NEW.unit_price;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Garante que a trigger só será removida se a tabela existir
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'sales') THEN
    DROP TRIGGER IF EXISTS trg_set_total ON sales;
  END IF;
END$$;

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

-- Dados de exemplo (50 registros variados)
INSERT INTO sales (region, product, quantity, unit_price, date, customer_id, status, created_at, updated_at, notes, user_id, category, payment_method) VALUES
('Norte','Bateria A',10,200,'2025-08-01',101,'paid','2025-08-01','2025-08-01','Venda normal',1,'Automotiva','dinheiro'),
('Sul','Bateria B',5,350,'2025-08-02',102,'pending','2025-08-02','2025-08-02','Aguardando pagamento',2,'Automotiva','cartao'),
('Nordeste','Bateria C',8,180,'2025-08-03',103,'cancelled','2025-08-03','2025-08-03','Pedido cancelado',3,'Residencial','boleto'),
('Sudeste','Bateria D',12,220,'2025-08-04',104,'paid','2025-08-04','2025-08-04','Venda rápida',4,'Residencial','dinheiro'),
('Centro-Oeste','Bateria E',7,210,'2025-08-05',105,'pending','2025-08-05','2025-08-05','Cliente pediu prazo',5,'Industrial','cartao'),
('Norte','Bateria F',15,195,'2025-08-06',106,'paid','2025-08-06','2025-08-06','Venda recorrente',1,'Industrial','boleto'),
('Sul','Bateria G',9,340,'2025-08-07',107,'cancelled','2025-08-07','2025-08-07','Cliente desistiu',2,'Automotiva','dinheiro'),
('Nordeste','Bateria H',6,175,'2025-08-08',108,'paid','2025-08-08','2025-08-08','Venda normal',3,'Residencial','cartao'),
('Sudeste','Bateria I',11,230,'2025-08-09',109,'pending','2025-08-09','2025-08-09','Aguardando pagamento',4,'Residencial','boleto'),
('Centro-Oeste','Bateria J',13,205,'2025-08-10',110,'paid','2025-08-10','2025-08-10','Venda rápida',5,'Industrial','dinheiro'),
('Norte','Bateria K',14,215,'2025-08-11',101,'paid','2025-08-11','2025-08-11','Venda normal',1,'Automotiva','cartao'),
('Sul','Bateria L',8,360,'2025-08-12',102,'pending','2025-08-12','2025-08-12','Aguardando pagamento',2,'Automotiva','boleto'),
('Nordeste','Bateria M',10,185,'2025-08-13',103,'cancelled','2025-08-13','2025-08-13','Pedido cancelado',3,'Residencial','dinheiro'),
('Sudeste','Bateria N',7,225,'2025-08-14',104,'paid','2025-08-14','2025-08-14','Venda rápida',4,'Residencial','cartao'),
('Centro-Oeste','Bateria O',9,200,'2025-08-15',105,'pending','2025-08-15','2025-08-15','Cliente pediu prazo',5,'Industrial','boleto'),
('Norte','Bateria P',16,210,'2025-08-16',106,'paid','2025-08-16','2025-08-16','Venda recorrente',1,'Industrial','dinheiro'),
('Sul','Bateria Q',12,355,'2025-08-17',107,'cancelled','2025-08-17','2025-08-17','Cliente desistiu',2,'Automotiva','cartao'),
('Nordeste','Bateria R',5,170,'2025-08-18',108,'paid','2025-08-18','2025-08-18','Venda normal',3,'Automotiva','boleto'),
('Norte','Bateria A',7,200,'2025-08-19',109,'pending','2025-08-19','2025-08-19','Aguardando pagamento',4,'Automotiva','dinheiro'),
('Sul','Bateria A',5,200,'2025-08-20',110,'paid','2025-08-20','2025-08-20','Venda rápida',5,'Automotiva','cartao'),
('Sudeste','Bateria B',10,350,'2025-08-21',101,'cancelled','2025-08-21','2025-08-21','Pedido cancelado',1,'Automotiva','boleto'),
('Centro-Oeste','Bateria B',6,350,'2025-08-22',102,'paid','2025-08-22','2025-08-22','Venda normal',2,'Automotiva','dinheiro'),
('Nordeste','Bateria C',9,180,'2025-08-23',103,'pending','2025-08-23','2025-08-23','Aguardando pagamento',3,'Residencial','cartao'),
('Sul','Bateria C',4,180,'2025-08-24',104,'paid','2025-08-24','2025-08-24','Venda rápida',4,'Residencial','boleto'),
('Norte','Bateria D',8,220,'2025-08-25',105,'cancelled','2025-08-25','2025-08-25','Pedido cancelado',5,'Residencial','dinheiro'),
('Sul','Bateria E',6,210,'2025-08-26',106,'paid','2025-08-26','2025-08-26','Venda recorrente',1,'Industrial','cartao'),
('Nordeste','Bateria F',12,195,'2025-08-27',107,'pending','2025-08-27','2025-08-27','Cliente pediu prazo',2,'Industrial','boleto'),
('Sudeste','Bateria G',7,340,'2025-08-28',108,'paid','2025-08-28','2025-08-28','Venda normal',3,'Automotiva','dinheiro'),
('Centro-Oeste','Bateria H',10,175,'2025-08-29',109,'cancelled','2025-08-29','2025-08-29','Cliente desistiu',4,'Residencial','cartao'),
('Norte','Bateria I',9,230,'2025-08-30',110,'paid','2025-08-30','2025-08-30','Venda rápida',5,'Residencial','boleto'),
('Sul','Bateria J',11,205,'2025-08-31',101,'pending','2025-08-31','2025-08-31','Aguardando pagamento',1,'Industrial','dinheiro'),
('Nordeste','Bateria K',13,215,'2025-09-01',102,'paid','2025-09-01','2025-09-01','Venda normal',2,'Automotiva','cartao'),
('Sudeste','Bateria L',14,360,'2025-09-02',103,'cancelled','2025-09-02','2025-09-02','Pedido cancelado',3,'Automotiva','boleto'),
('Centro-Oeste','Bateria M',8,185,'2025-09-03',104,'paid','2025-09-03','2025-09-03','Venda rápida',4,'Residencial','dinheiro'),
('Norte','Bateria N',10,225,'2025-09-04',105,'pending','2025-09-04','2025-09-04','Cliente pediu prazo',5,'Residencial','cartao'),
('Sul','Bateria O',7,200,'2025-09-05',106,'paid','2025-09-05','2025-09-05','Venda recorrente',1,'Industrial','boleto'),
('Nordeste','Bateria P',9,210,'2025-09-06',107,'cancelled','2025-09-06','2025-09-06','Cliente desistiu',2,'Industrial','dinheiro'),
('Sudeste','Bateria Q',15,355,'2025-09-07',108,'paid','2025-09-07','2025-09-07','Venda normal',3,'Automotiva','cartao'),
('Centro-Oeste','Bateria R',5,170,'2025-09-08',109,'pending','2025-09-08','2025-09-08','Aguardando pagamento',4,'Automotiva','boleto'),
('Norte','Bateria A',12,200,'2025-09-09',110,'paid','2025-09-09','2025-09-09','Venda rápida',5,'Automotiva','dinheiro'),
('Sul','Bateria B',8,350,'2025-09-10',101,'cancelled','2025-09-10','2025-09-10','Pedido cancelado',1,'Automotiva','cartao'),
('Nordeste','Bateria C',6,180,'2025-09-11',102,'paid','2025-09-11','2025-09-11','Venda normal',2,'Residencial','boleto'),
('Sudeste','Bateria D',13,220,'2025-09-12',103,'pending','2025-09-12','2025-09-12','Aguardando pagamento',3,'Residencial','dinheiro'),
('Centro-Oeste','Bateria E',9,210,'2025-09-13',104,'paid','2025-09-13','2025-09-13','Venda rápida',4,'Industrial','cartao'),
('Norte','Bateria F',11,195,'2025-09-14',105,'cancelled','2025-09-14','2025-09-14','Pedido cancelado',5,'Industrial','boleto'),
('Sul','Bateria G',10,340,'2025-09-15',106,'paid','2025-09-15','2025-09-15','Venda recorrente',1,'Automotiva','dinheiro'),
('Nordeste','Bateria H',7,175,'2025-09-16',107,'pending','2025-09-16','2025-09-16','Cliente pediu prazo',2,'Residencial','cartao'),
('Sudeste','Bateria I',12,230,'2025-09-17',108,'paid','2025-09-17','2025-09-17','Venda normal',3,'Residencial','boleto'),
('Centro-Oeste','Bateria J',14,205,'2025-09-18',109,'cancelled','2025-09-18','2025-09-18','Cliente desistiu',4,'Industrial','dinheiro'),
('Nordeste','Bateria S',8,190,'2025-09-19',110,'paid','2025-09-19','2025-09-19','Venda extra',5,'Residencial','cartao'),
('Sudeste','Bateria T',6,240,'2025-09-20',101,'pending','2025-09-20','2025-09-20','Cliente pediu desconto',1,'Industrial','boleto');
-- Chamar a procedure (opcional)
-- CALL upsert_product_revenue();

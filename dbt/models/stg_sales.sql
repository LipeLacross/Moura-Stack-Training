-- stg_sales (silver layer)
-- Normaliza e garante coluna total
select
  order_id,
  region,
  product,
  quantity,
  unit_price,
  coalesce(total, quantity * unit_price) as total
from sales;


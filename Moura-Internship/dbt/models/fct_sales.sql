-- fct_sales (gold layer)
-- Agregação de receita e quantidade por produto
select
  product,
  sum(quantity)    as total_quantity,
  sum(total)       as total_revenue,
  avg(unit_price)  as avg_unit_price
from {{ ref('stg_sales') }}
group by product;


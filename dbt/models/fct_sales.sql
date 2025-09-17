-- gold
WITH base AS (
  SELECT * FROM {{ ref('stg_sales') }}
),
agg AS (
  SELECT
    product,
    SUM(total) AS revenue,
    SUM(quantity) AS qty
  FROM base
  GROUP BY product
)
SELECT * FROM agg;

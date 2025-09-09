-- silver
WITH src AS (
  SELECT
    order_id,
    region,
    product,
    CAST(quantity AS INT)       AS quantity,
    CAST(unit_price AS NUMERIC) AS unit_price,
    CAST(total AS NUMERIC)      AS total
  FROM {{ source('raw', 'sales') }}
)
SELECT * FROM src;

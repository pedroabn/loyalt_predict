-- Tabela retorna o dia com mais compras (UltCompra = 1) para cada semana, 
-- juntamente com a quantidade de compras nesse dia.
-- db_origin: analytics | db_target: analytics

WITH tb_compras AS (
    SELECT
        date(dtRef) AS dtRef,
        date(dtRef, 'weekday 1', '-7 days') AS dtRef_week,
        UltCompra,
        COUNT(*) as qtd_compras
    FROM life_cycle
    WHERE UltCompra = 1
    GROUP BY date(dtRef), UltCompra
),
max_por_dia AS (
    SELECT 
        dtRef_week,
        dtRef,
        qtd_compras,
        ROW_NUMBER() OVER (PARTITION BY dtRef_week ORDER BY qtd_compras DESC, dtRef ASC) as rank
    FROM tb_compras
)
SELECT 
    dtRef_week,
    dtRef as StarDay,
    qtd_compras as compras_no_dia
FROM max_por_dia
WHERE rank = 1
ORDER BY dtRef_week DESC
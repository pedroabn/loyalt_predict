WITH tb_daily as (
    SELECT 
        DISTINCT
        IdCliente,
        substr(DtCriacao,0,11) as dtdia
    FROM transacoes
    
),

tb_idade as (
    SELECT 
        IdCliente,
        CAST(max(julianday("now") - julianday(dtdia)) as INT) as PrimCompra,
        CAST(min(julianday("now") - julianday(dtdia)) as INT) as UltCompra
        
    FROM tb_daily
    GROUP BY IdCliente
    ),

tb_rn as (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY IdCliente ORDER BY dtdia DESC) as rn_dia
    FROM tb_daily
),

tb_penultima AS (
    SELECT *,
        CAST(julianday('now') - julianday(dtdia) as INT) as penultcompra
    FROM tb_rn
    WHERE rn_dia = 2),

tb_lifec AS (
    SELECT 
            t1.* ,
            t2.penultcompra ,
            CASE
                WHEN PrimCompra <= 7 THEN '01-CURIOSO'
                WHEN UltCompra <= 7 AND penultcompra - Ultcompra <= 14 THEN '02-FIEL'
                WHEN UltCompra BETWEEN 8 AND 14 THEN '03-TURISTA'
                WHEN UltCompra BETWEEN 15 AND 28 THEN '04-DESENCANTADO'
                WHEN UltCompra > 28 THEN '05-ZUMBI'
                WHEN UltCompra <= 7 AND (penultcompra - Ultcompra) between 15 and 27 THEN '07-RECONQUER'
                WHEN UltCompra <= 7 AND (penultcompra - Ultcompra) > 27 THEN '06-REBORN'
            END AS descLife

    FROM tb_idade as t1

    LEFT JOIN tb_penultima as t2
    ON t1.IdCliente = t2.IdCliente
)

SELECT 
    descLife,
    count(*)
FROM tb_lifec
GROUP BY descLife

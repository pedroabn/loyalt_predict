WITH tb_daily AS (
    SELECT 
        DISTINCT
        IdCliente,
        substr(DtCriacao, 0, 11) AS dtdia
    FROM transacoes
    WHERE DtCriacao < "{date}"
),

tb_idade AS (
    SELECT 
        IdCliente,
        CAST(max(julianday("{date}") - julianday(dtdia)) AS INT) AS PrimCompra,
        CAST(min(julianday("{date}") - julianday(dtdia)) AS INT) AS UltCompra
    FROM tb_daily
    GROUP BY IdCliente
),

tb_rn AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY IdCliente ORDER BY dtdia DESC) AS rn_dia
    FROM tb_daily
),

tb_penultima AS (
    SELECT *,
        CAST(julianday("{date}") - julianday(dtdia) AS INT) AS penultcompra
    FROM tb_rn
    WHERE rn_dia = 2
),

tb_lifec AS (
    
    SELECT 
        t1.*,
        t2.penultcompra,
        CASE
            WHEN PrimCompra <= 7 THEN '01-CURIOSO'
            WHEN UltCompra <= 7 AND penultcompra - UltCompra <= 14 THEN '02-FIEL'
            WHEN UltCompra BETWEEN 8 AND 14 THEN '03-TURISTA'
            WHEN UltCompra BETWEEN 15 AND 28 THEN '04-DESENCANTADO'
            WHEN UltCompra > 28 THEN '05-ZUMBI'
            WHEN UltCompra <= 7 AND penultcompra - UltCompra BETWEEN 15 AND 27 THEN '07-RECONQUER'
            WHEN UltCompra <= 7 AND penultcompra - UltCompra > 27 THEN '06-REBORN'
        END AS descLifeCycle

    FROM tb_idade AS t1
    LEFT JOIN tb_penultima AS t2

    ON t1.IdCliente = t2.IdCliente
),

tb_freq AS (
    SELECT 
        t1.IdCliente,
        COALESCE(count(DISTINCT substr(t2.DtCriacao, 0, 11)), 0) AS qtdFreq,
        COALESCE(sum(CASE WHEN t2.QtdePontos > 0 THEN t2.QtdePontos ELSE 0 END), 0) AS qtdPontosPos
    FROM tb_idade AS t1
    LEFT JOIN transacoes AS t2
        ON t1.IdCliente = t2.IdCliente
        AND t2.DtCriacao < "{date}"
        AND t2.DtCriacao >= date("{date}", "-28 days")
    GROUP BY t1.IdCliente
),

tb_cluster AS (
    SELECT *,
        CASE
                WHEN qtdFreq <= 10 AND qtdPontosPos >= 1500 THEN '12-HYPER'
                WHEN qtdFreq > 10 AND qtdPontosPos >= 1500 THEN '22-EFICIENTE'
                WHEN qtdFreq <= 10 AND qtdPontosPos >= 750 THEN '11-INDECISO'
                WHEN qtdFreq > 10 AND qtdPontosPos >= 750 THEN '21-ESFORÇADO'
                WHEN qtdFreq < 5 THEN '00-LURKER'
                WHEN qtdFreq <= 10 THEN '01-PREGUIÇOSO'
                WHEN qtdFreq > 10 THEN '20-POTENCIAL'
        END AS cluster
    FROM tb_freq
)

SELECT 
    date('{date}', '-1 day') AS dtRef,
    t1.*,
    t2.qtdFreq,
    t2.qtdPontosPos,
    t2.cluster 
FROM tb_lifec AS t1
LEFT JOIN tb_cluster AS t2
ON t1.IdCliente = t2.IdCliente
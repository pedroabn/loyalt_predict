-- Quantidade de usuários ativos por mês, e clientes ativos por dia. A diferença de dias representa
-- o período de inatividade de lives. Quanto mais longe de 7, mais dias ficaram sem clientes ativos. 
with tb_daily AS (
    SELECT DISTINCT 
        date(SUBSTR(DtCriacao, 0, 11)) AS Dtdia,
        IdCliente
    FROM transacoes
),

tb_distinct AS (
    SELECT DISTINCT Dtdia as dtRef
    FROM tb_daily
)

SELECT t1.dtRef,
        count (DISTINCT IdCliente) as SAU,
        count (DISTINCT t2.Dtdia) as qtdeDias

FROM tb_distinct as t1
LEFT JOIN tb_daily as t2
ON t2.Dtdia <= t1.dtRef
AND julianday(t1.dtRef) - julianday(t2.Dtdia) < 7

GROUP BY t1.dtRef
ORDER BY t1.dtRef DESC

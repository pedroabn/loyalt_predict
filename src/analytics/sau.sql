WITH tb_daily AS (
    SELECT DISTINCT 
        date(substr(DtCriacao, 1, 10)) AS Dtdia,
        IdCliente
    FROM transacoes
),

tb_week AS (
    SELECT DISTINCT 
        date(Dtdia, 'weekday 1', '-7 days') AS dtRef_week
    FROM tb_daily
),

tb_base AS (
    SELECT 
        w.dtRef_week,
        d.Dtdia,
        d.IdCliente
    FROM tb_week w
    LEFT JOIN tb_daily d
      ON d.Dtdia >= w.dtRef_week
     AND d.Dtdia < date(w.dtRef_week, '+7 days')
)

SELECT 
    dtRef_week,
    COUNT(DISTINCT IdCliente) AS SAU,
    COUNT(DISTINCT Dtdia) AS dias_ativos
FROM tb_base
GROUP BY dtRef_week
ORDER BY dtRef_week DESC;
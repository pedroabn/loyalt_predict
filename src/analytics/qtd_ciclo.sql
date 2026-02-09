-- Observando a quantidade de clientes por ciclo de vida, em um recorte semanal
-- Com variação percentual em relação à semana anterior

WITH tb_lfc AS (
    SELECT dtRef,
        descLife AS tipo,
        COUNT(descLife) AS qtd
    FROM life_cycle
    WHERE descLife <> "05-ZUMBI"
    GROUP BY dtRef, descLife
),

tb_countlfc AS (
    SELECT DISTINCT 
        date(substr(dtRef, 0, 11)) AS dtRef,
        tipo,
        qtd
    FROM tb_lfc
),

tb_week AS (
    SELECT DISTINCT 
        date(dtRef, 'weekday 1', '-7 days') AS dtRef_week
    FROM tb_countlfc
),

tb_weekly_agg AS (
    SELECT 
        w.dtRef_week,
        d.tipo,
        SUM(d.qtd) AS qtd
    FROM tb_week w
    LEFT JOIN tb_countlfc d
        ON d.dtRef <= w.dtRef_week
        AND julianday(w.dtRef_week) - julianday(d.dtRef) < 7
    GROUP BY w.dtRef_week, d.tipo
),

tb_final AS (
    SELECT 
        dtRef_week,
        tipo,
        qtd,
        LAG(qtd) OVER (PARTITION BY tipo ORDER BY dtRef_week) AS qtd_semana_anterior,
        ROUND(
            CASE 
                WHEN LAG(qtd) OVER (PARTITION BY tipo ORDER BY dtRef_week) IS NULL 
                    OR LAG(qtd) OVER (PARTITION BY tipo ORDER BY dtRef_week) = 0 
                THEN NULL
                ELSE ((qtd * 1.0 - LAG(qtd) OVER (PARTITION BY tipo ORDER BY dtRef_week)) / 
                    LAG(qtd) OVER (PARTITION BY tipo ORDER BY dtRef_week)) * 100
            END, 
        2) AS var_perc
    FROM tb_weekly_agg
    ORDER BY dtRef_week DESC, tipo
)

SELECT 
    dtRef_week,
    tipo,
    qtd,
    var_perc
FROM tb_final 
LIMIT 6;
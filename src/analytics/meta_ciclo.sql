-- Meta de tempo em Ciclo de Vida do Cliente
-- Origin: Analytics | Target: Analytics
WITH tb_freq as(
    SELECT
        date(dtRef) AS dtRef,
        AVG(avgFreqGrupo) as avgFreqGrupo,
        descLifeCycleFoto
    FROM fs_life_cycle
    GROUP BY date(dtRef), descLifeCycleFoto
),
tb_week AS (
    SELECT DISTINCT 
        date(dtRef, 'weekday 1', '-7 days') AS dtRef_week
    FROM tb_freq
),
tb_base AS (
    SELECT 
        w.dtRef_week,
        f.avgFreqGrupo,
        f.descLifeCycleFoto
    FROM tb_week w
    LEFT JOIN tb_freq f
      ON f.dtRef <= w.dtRef_week
     AND julianday(w.dtRef_week) - julianday(f.dtRef) < 7
),
tb_avg as (
    SELECT 
        dtRef_week,
        COALESCE(AVG(avgFreqGrupo), 0) AS freq_mean,
        descLifeCycleFoto
    FROM tb_base
    GROUP BY dtRef_week, descLifeCycleFoto
)

SELECT 
    dtRef_week,
    descLifeCycleFoto,
    ROUND(((freq_mean - 3) / 3) * 100, 2) as Meta_Percentual,
    freq_mean
FROM tb_avg
WHERE descLifeCycleFoto = '03-TURISTA' AND dtRef_week >= date('{date}','-28 day')
ORDER BY dtRef_week DESC;
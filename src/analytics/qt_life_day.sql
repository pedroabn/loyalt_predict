WITH tb_lfc as (
    SELECT 
        COUNT(CASE WHEN descLife = '01-CURIOSO' THEN 1 END) AS Curioso,
        COUNT(CASE WHEN descLife = '02-FIEL' THEN 1 END) AS Fiel,
        COUNT(CASE WHEN descLife = '03-TURISTA' THEN 1 END) AS Turista,
        COUNT(CASE WHEN descLife = '04-DESENCANTADO' THEN 1 END) AS Desencantada,
        COUNT(CASE WHEN descLife = '06-REBORN' THEN 1 END) AS Reborn,
        COUNT(CASE WHEN descLife = '07-RECONQUER' THEN 1 END) AS Reconquistado,
        dtRef            
    FROM  life_cycle
    GROUP BY dtRef
),

tb_countlfc AS (
    SELECT DISTINCT 
        date(substr(dtRef, 0, 11)) AS dtRef,
        Curioso,
        Fiel,
        Turista,
        Desencantada,
        Reborn,
        Reconquistado
    FROM tb_lfc
),

tb_week AS (
    SELECT DISTINCT 
        date(dtRef, 'weekday 1', '-7 days') AS dtRef_week
    FROM tb_countlfc
)

SELECT 
    w.dtRef_week,
    d.*
FROM tb_week w
LEFT JOIN tb_countlfc d
    ON d.dtRef <= w.dtRef_week
    AND julianday(w.dtRef_week) - julianday(d.dtRef) < 7
WITH tb_turista as (
    SELECT 
          count(descLife) as qtd_turista,
          dtRef            
    FROM  life_cycle
    WHERE descLife = '03-TURISTA'
    GROUP BY dtRef
),

tb_turista_dia AS (
    SELECT DISTINCT 
        date(substr(dtRef, 0, 11)) AS dtRef,
        qtd_turista
    FROM tb_turista
),

tb_week AS (
    SELECT DISTINCT 
        date(dtRef, 'weekday 1', '-7 days') AS dtRef_week
    FROM tb_turista_dia
),



tb_base AS (
    SELECT 
        w.dtRef_week,
        d.dtRef,
        d.qtd_turista
    FROM tb_week w
    LEFT JOIN tb_turista_dia d
      ON d.dtRef <= w.dtRef_week
     AND julianday(w.dtRef_week) - julianday(d.dtRef) < 7
),

tb_sau as (
    SELECT *
    FROM sau
)

SELECT
    t1.*,
    case when t2.qtd_turista is null then 0 else t2.qtd_turista end as qtd_turista
FROM tb_sau t1
LEFT JOIN tb_base t2
ON t1.dtRef_week = t2.dtRef_week
GROUP BY t1.dtRef_week
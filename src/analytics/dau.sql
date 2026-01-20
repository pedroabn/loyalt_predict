-- Quantidade de usuários ativos por dia
SELECT  SUBSTR(DtCriacao, 0, 11) AS DtDia,
        COUNT(DISTINCT IdCliente) AS DAU
FROM transacoes
GROUP BY 1
ORDER BY DtDia

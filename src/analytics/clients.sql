SELECT 
    idCliente as IdCliente,
    flEmail,
    flTwitch,
    flYouTube,
    flBlueSky,
    flInstagram,
    CASE 
        WHEN (SUM(flYouTube) + SUM(flBlueSky) + SUM(flInstagram) + 
              SUM(flEmail) + SUM(flTwitch)) >= 4 
        THEN 'Multi-canal'
        
        WHEN (SUM(flYouTube) + SUM(flBlueSky) + SUM(flInstagram) + 
              SUM(flEmail) + SUM(flTwitch)) >= 2 
        THEN 'Dual-canal'
        
        WHEN (SUM(flYouTube) + SUM(flBlueSky) + SUM(flInstagram) + 
              SUM(flEmail) + SUM(flTwitch)) = 1 
        THEN 'Mono-canal'
        
        ELSE 'Inativo'
    END AS perfil_engajamento
FROM clientes
GROUP BY IdCliente;
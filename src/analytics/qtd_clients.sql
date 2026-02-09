SELECT 'YouTube' AS canal, SUM(flYouTube) AS total FROM clients
UNION ALL
SELECT 'BlueSky', SUM(flBlueSky) FROM clients
UNION ALL
SELECT 'Instagram', SUM(flInstagram) FROM clients
UNION ALL
SELECT 'Email', SUM(flEmail) FROM clients
UNION ALL
SELECT 'Twitch', SUM(flTwitch) FROM clients
ORDER BY total DESC;
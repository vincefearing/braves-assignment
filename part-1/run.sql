-- List all batters that had a single season WAR greater than 3 during the 2002 or 2003 seasons,
-- or a combined WAR greater than 5 over those two seasons. List in descending order of their
-- combined WAR for those seasons.

SELECT playerID, name,
       SUM(CAST(WAR AS REAL)) AS total_war,
       MAX(CASE WHEN year = '2002' THEN CAST(WAR AS REAL) ELSE 0 END) AS war_2002,
       MAX(CASE WHEN year = '2003' THEN CAST(WAR AS REAL) ELSE 0 END) AS war_2003
FROM WAR
WHERE year IN ('2002', '2003')
GROUP BY playerID, name
HAVING MAX(CASE WHEN year = '2002' THEN CAST(WAR AS REAL) ELSE 0 END) > 3 
    OR MAX(CASE WHEN year = '2003' THEN CAST(WAR AS REAL) ELSE 0 END) > 3
    OR SUM(CAST(WAR AS REAL)) > 5
ORDER BY total_war DESC;

https://docs.google.com/spreadsheets/d/1X1YviKnCOBAF7jd9XGjNGPZWJZyAbIlkZMAq8wZeAuE/edit?usp=sharing

-- Write a query that returns every pitcher who threw at least one pitch for the Atlanta Braves in
-- 2018, along with three 1/0 indicator columns for whether they reached the 1+ WAR, 2+ WAR,
-- or 3+ WAR cutoff in that year, along with a fourth column for their total yearly WAR 

SELECT p.playerID, 
       p.name,
       CASE WHEN CAST(p.WAR AS REAL) >= 1 THEN 1 ELSE 0 END AS "1+ WAR",
       CASE WHEN CAST(p.WAR AS REAL) >= 2 THEN 1 ELSE 0 END AS "2+ WAR",
       CASE WHEN CAST(p.WAR AS REAL) >= 3 THEN 1 ELSE 0 END AS "3+ WAR",
       CAST(p.WAR AS REAL) AS total_war
FROM PERF p
WHERE p.TeamKey = '43135' 
  AND p.year = '2018'
GROUP BY p.playerID, p.name;

https://docs.google.com/spreadsheets/d/1Hp8wdvNiGNe6S5rWpEubIatsI7cZ1ZmygnWzsDi0hzA/edit?usp=sharing

-- How many plate appearances did Luke Jackson have that reached a two-strike count but did
-- NOT result in a strikeout? Of those plate appearances, how many passed through 0-2, 1-2 or 2-
-- 2 counts?

WITH TwoStrikePA AS (
    SELECT DISTINCT GameKey, INNING, PA_OF_INNING, TOP_BOT
    FROM PITCHBYPITCH
    WHERE PitcherID = '592426'
      AND STRIKES = '2'
      AND CAST(IS_STRIKEOUT AS INTEGER) = 0
)
SELECT 
    COUNT(*) AS TotalTwoStrikeNonStrikeoutPA,
    SUM(CASE WHEN BALLS = '0' AND STRIKES = '2' THEN 1 ELSE 0 END) AS Count_0_2,
    SUM(CASE WHEN BALLS = '1' AND STRIKES = '2' THEN 1 ELSE 0 END) AS Count_1_2,
    SUM(CASE WHEN BALLS = '2' AND STRIKES = '2' THEN 1 ELSE 0 END) AS Count_2_2
FROM PITCHBYPITCH
WHERE PitcherID = '592426'
  AND STRIKES = '2'
  AND CAST(IS_STRIKEOUT AS INTEGER) = 0;

https://docs.google.com/spreadsheets/d/1cpW4c1QtpmjLo9xpUfsFTI7p4EdtruPqXDC5IR1MpUc/edit?usp=sharing



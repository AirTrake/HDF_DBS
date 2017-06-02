/*
Aufgabe 2
*/

SELECT Vorname, Nachname 
FROM Passagier
WHERE Alter>42

SELECT Kredidkartennummer 
FROM Passagier, Flug, Fluggesellschaft
WHERE Passaagier.ID=Flug.Passagier-ID
AND Fluggesellschaft.ID=Flug.Fluggesellschaft-ID
AND 18.01.2014 <= Flug.Datum < 27.09.2014
AND Fluggesellschaft.Name=Lufthansa

SELECT Fluggesellschaft.Name
FROM Fluggesellschaft, Flug, Wetter
WHERE Fluggesellschaft.ID = Flug.Fluggesellschaft-ID
AND Flug.Datum = Wetter.Datum
AND Wetter.Sonnenstunden > 8

SELECT Passaagier.Vorname, Passaagier.Name
FROM Fluggesellschaft, Flug, Wetter
WHERE Fluggesellschaft.ID = Flug.Fluggesellschaft-ID
AND Flug.Datum = Wetter.Datum
AND Wetter.Temperatur <= 20
AND Wetter.REgenmenge > 10
AND Wetter.Sonnnescheindauer <= 6

/*
Aufgabe 3
*/

/*
3.1.
*/
CREATE VIEW Transportiert
AS SELECT Fluggesellschaft.Name, COUNT(*) AS Zahl
FROM Fluggesellschaft, Flug
WHERE Fluggesellschaft.ID = Flug.Fluggesellschaft-ID
GROUP BY Fluggesellschaft.Name;

SELECT Name 
FROM Transportiert
ORDER BY Zahl 
LIMIT 3

/*
3.2.
*/
CREATE VIEW Pass
AS SELECT Vorname, Nachname, Count(*) AS Zahl
FROM Passagier, Flug
WHERE Passagier.ID = Flug.Passagier-ID
GROUP BY Vorname, Nachname;

SELECT Vorname, Nachname
FROM Pass
ORDER BY Zahl DESC
LIMIT 10

/*
3.3.
*/

CREATE VIEW Gesellschaft
AS SELECT Vorname, Nachname, Count(Flug.Fluggesellschaft-ID) AS Zahl2
FROM Passagier, Flug
WHERE Passagier.ID = Flug.Passagier-ID
GROUP BY Vorname, Nachname;

SELECT Pass.Vorname, Pass.Nachname
FROM Pass, Gesellschaft
WHERE Pass.Name=Gesellschaft.Name
AND Pass.Vorname=Gesellschaft.Vorname
ORDER BY Zahl, Zahl2 
LIMIT 5






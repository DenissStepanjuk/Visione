# Visione



Loome MySQL database, kasutame jargmine kriteriumid:

host="localhost", 
user="root", 
passwd='qwerty', 
port='3306', 
database='visione'


Projektis meil on failid:

A_Create_Database - andmebaasi loomine ja ühendamine 
B_registration- Andmete registreerimine 
C_Attendance_Control - Kohaloleku kontrollimine




Liides:
https://github.com/DenssStepanjuk/WebInterface


See dokumentatsioon annab ülevaate loodud projektist, selle tehnoloogiatest, komponentidest ja töö käigust. Loodud töökood on GitHubis, link: https://github.com/DenssStepanjuk/Visione 
Projekti eesmärk on lihtsustada õppeasutuses osalemise kontrollimise süsteemi. Praegu jälgitakse kohalolu õpetaja või õpilaste endi abiga, see tähendab, et iga tunni alguses peab õpetaja läbi viima kohalolijate seas küsitluse ja märkima, kes on kohal ja kes puudub. Või lastakse klassi ümber paberileht ja pastakas ning iga õpilane kirjutab end nimekirja, mille järel antakse õpetajale kohalolevatega leht. On ka uuemaid meetodeid, näiteks QR-koodi skaneerimine õpilaste poolt, mis annab juurdepääsu Google'i vormile, kus õpilased peavad registreeruma tunnile. Kõik need inimese otsese osalusega meetodid ja see kontrollisüsteem hakkab vananema, on vaja välja mõelda, kuidas protsessi automatiseerida. 
Meie idee on protsessi lihtsustada ja säästa õpetaja ja õpilaste aega. Kohaloleku kontroll tehakse tehniliste vahenditega. Klassiruumis on kaamera, mis loeb klassi siseneja biomeetriat ja võrdleb saadud andmeid andmebaasiga. See kontrollib näiteks seda, kas see inimene peaks nüüd selles klassis olema, kas ta on üldiselt selle õppeasutuse õpilane / õpetaja ning fikseeritakse ka aeg, millal inimene klassi astus.
⦁	Prototüübi nõuded ja piirangud
Siin on prototüübi nõuded ja piirangud, mis projektile edastati.
Automatiseerimine peaks toimuma nii, et õpetaja / õpilane sooritaks minimaalselt toiminguid ja süsteem aitaks kohalviibimise jälgimisel maksimaalselt kaasa. Kasutamine peaks olema iga õpetaja jaoks intuitiivne, nii et selle mõistmisega ei tekiks raskusi ega segataks kohaloleku kontrollimist. Süsteem peaks õpetajat teavitama, kui klassiruumis viibib kõrvaline inimene.
Piirangud võivad olla seotud arvuti või seadmega, kus see algoritm töötab. See algoritm on protsessori jaoks üsna nõudlik ja parema jõudluse saavutamiseks võib vaja minna võimsat arvutit. Piirangud on seotud ka kaameraga, vajate head ja suure eraldusvõimega kaamerat, kuna see lihtsustab algoritmi tööd ja aitab kaasa paremale näotuvastusele, sõltub algoritmi ulatus kaamerast. Mida parem on kaamera, seda kaugemale suudab algoritm nägu tuvastada ja selle ära tunda.
⦁	Kuidas see töötab
Selles alaosas kirjeldatakse süsteemi tööprotsessi.
Kui inimene ilmub klassiruumi, tuvastab näotuvastussüsteem tema näo, teeb foto ja töötab nende andmetega. Programm loeb fotodelt näojooned avatud OpenCV-teekide abil. Andmebaasi salvestatakse juba üles laaditud fotod inimestest, kes õpivad või töötavad haridusasutuses. Programm küsib neid fotosid andmebaasist ja võrdleb neid äsja tehtud piltidega. Kui võrdluse tulemusel on kokkulangevuse protsent üle 60%, siis näitab programm selle inimese ja kuvab tema andmed, samuti näitab, kas see inimene peaks nüüd sellesse klassi kuuluma, kui vastet ei leita, süsteem anna sellest signaali õpetajale. Samuti luuakse eraldi kaust, kuhu salvestatakse sellised andmed: aeg, millal inimene ruumi sisenes, tema isikuandmed (õpilaste jaoks nimi, perekonnanimi, rühma number).
Nüüd üksikasjalikumalt algoritmi kohta, millel põhineb selle programmi idee.
See algoritm tuvastab näo inimese silmade, nina, suu ja lõua asukoha ja kuju järgi. Algoritmi on väga mugav ja lihtne kasutada, see tuvastab näo väga kiiresti, sellel on suur potentsiaal ja näotuvastus täpsem kui teistel algoritmidel. Võrdlesime kahte näotuvastusalgoritmi ja haara kaskaadi algoritmi, haara kaskaadi algoritm kasutab pildistamise pikslite ruute ja nende funktsioone. Valisime näotuvastuse algoritmi, kuna selle kasutamine suurendab tuvastamise täpsust ja aitab seetõttu täpselt kindlaks teha, milline inimene klassiruumi sisenes. Kuid sellel algoritmil on üks puudus, kuna see on üsna nõudlik seadmete, millega seda ühendatakse suhtes.





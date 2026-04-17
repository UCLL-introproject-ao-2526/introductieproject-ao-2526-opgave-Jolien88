## 2 april 2026 14u30

Begonnen met de tutorial. Het eerste probleemd dat ik tegenkwam was dat python 3.15 pygame nog niet ondersteunt (of andersom). Dit heb ik opgelost door een virtuele omgeving te maken waarin python 3.12 runt voor het ontwikkelen van de game.
Stappen voor de volgende keren: 
    - Voor ik start: source venv/Scripts/activate
    - Als ik klaar ben: deactivate
Nadien problemen met het weergeven van de knoppen 'Hit me' en 'Stand' omdat mijn scherm kleiner is. Oplossing nog niet gevonden. 

Geindigd op 18.10 min.

## 5 april 2026 13u51

Tutorial Blackjack verder afgewerkt. Toch maar verder gegaan met de waarden voor het scherm die hij gebruikt. De aanpassingen ga ik achteraf doorvoeren. In de code die ik had, zaten enkele foutjes. Deze geprobeerd op te lossen. Ook zaten er in de code van de tutorial enkele dingen die niet klopten. Zoals bij een nieuw spel werd de dealer_hand nog steeds getoond, deze waarde werd dus niet terug op False gezet. Deze ook aangepast.

## 8 april 2026 15:34

Instelling van het scherm en de knoppen aangepast zodat het op mijn 15 inch scherm werkt. Width op 600 laten staan, heigth verandert naar 750. Locatie van de 'hit' en 'stand' knoppen aangepast van 700 naar 600 en de tekst in de knoppen van 735 naar 635.
Na deze aanpassing komen de kaarten onder de knoppen te liggen. Deze moeten dus ook aangepast worden. Locatie van de kaarten aangepast zodat alle tekst nog in het speelveld valt en niets elkaar overlapt. Nu zie ik wel dat de 'new hand' knop niet meer mooi in het midden staat en de scoretekst onderaan verdwenen is. Gespeeld met de locatie van de scores en deze goed gekregen. Ook de 'new hand' knop op een betere locatie gekregen. 

Eigen aanpassingen: het idee is om er een soort Rogue-like blackjack van te maken met verschillende modifiers die willekeurig bij elke nieuwe hand gekozen worden. Om te starten heb ik mijn variabelen opgesplitst in constants, game-setup en variabelen om het verschil tussen de spelconfiguratie en runtime duidelijk te houden. 
De eerste modifier is Lucky Player, waarbij de speler bij de eerste deal altijd een kaart krijgt die 10 waard is. Hiervoor heb ik een hulpfunctie moeten schrijven die de kaarten met waarde 10 returnt. 
Om de modifiers te verwerken heb ik een aparte functie gemaakt die de initiele eerste deal opzet, zodat ik de gewone deal functie niet moest aanpassen. 
De volgende stap is zoeken waar ik juist deze initial_deal functie moet implementeren.

## 17 april 2026
Ik wil de deal functie aanpassen zodat de initial deal als aparte functie in het bestand komt te staan en niet samengevoegd met de algemene deal functie. Voor ik startte, heb ik toch nog even de game gespeeld om te zien of alles correct werkt op dit punt.

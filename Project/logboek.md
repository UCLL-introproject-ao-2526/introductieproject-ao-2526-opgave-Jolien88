## 2 april 2026 14u30

Begonnen met de tutorial. Het eerste probleemd dat ik tegenkwam was dat python 3.15 pygame nog niet ondersteunt (of andersom). Dit heb ik opgelost door een virtuele omgeving te maken waarin python 3.12 runt voor het ontwikkelen van de game.
Stappen voor de volgende keren: 
    - Voor ik start: source venv/Scripts/activate
    - Als ik klaar ben: deactivate
Nadien problemen met het weergeven van de knoppen 'Hit me' en 'Stand' omdat mijn scherm kleiner is. Oplossing nog niet gevonden. 

## 5 april 2026 13u51

Tutorial Blackjack verder afgewerkt. Toch maar verder gegaan met de waarden voor het scherm die hij gebruikt. De aanpassingen ga ik achteraf doorvoeren. In de code die ik had, zaten enkele foutjes. Deze geprobeerd op te lossen. Ook zaten er in de code van de tutorial enkele dingen die niet klopten. Zoals bij een nieuw spel werd de dealer_hand nog steeds getoond, deze waarde werd dus niet terug op False gezet. Deze ook aangepast.

## 8 april 2026 15:34

Instelling van het scherm en de knoppen aangepast zodat het op mijn 15 inch scherm werkt. Width op 600 laten staan, heigth verandert naar 750. Locatie van de 'hit' en 'stand' knoppen aangepast van 700 naar 600 en de tekst in de knoppen van 735 naar 635.
Na deze aanpassing komen de kaarten onder de knoppen te liggen. Deze moeten dus ook aangepast worden. Locatie van de kaarten aangepast zodat alle tekst nog in het speelveld valt en niets elkaar overlapt. Nu zie ik wel dat de 'new hand' knop niet meer mooi in het midden staat en de scoretekst onderaan verdwenen is. Gespeeld met de locatie van de scores en deze goed gekregen. Ook de 'new hand' knop op een betere locatie gekregen. 

Eigen aanpassingen: het idee is om er een soort Rogue-like blackjack van te maken met verschillende modifiers die willekeurig bij elke nieuwe hand gekozen worden. Om te starten heb ik mijn variabelen opgesplitst in constants, game-setup en variabelen om het verschil tussen de spelconfiguratie en runtime duidelijk te houden. 
De eerste modifier is Lucky Player, waarbij de speler bij de eerste deal altijd een kaart krijgt die 10 waard is. Hiervoor heb ik een hulpfunctie moeten schrijven die de kaarten met waarde 10 returnt. 
Om de modifiers te verwerken heb ik een aparte functie gemaakt die de initiele eerste deal opzet, zodat ik de gewone deal functie niet moest aanpassen. 
De volgende stap is zoeken waar ik juist deze initial_deal functie moet implementeren.

## 17 april 2026 11:18
Ik wil de deal functie aanpassen zodat de initial deal als aparte functie in het bestand komt te staan en niet samengevoegd met de algemene deal functie. Voor ik startte, heb ik toch nog even de game gespeeld om te zien of alles correct werkt op dit punt.
Het aanpassen van de gameloop zodat de modifiers werken, ging vrij vlot. Ik moest enkel het gedeelte rond initial_deal aanpassen en ervoor zorgen dat nadien de initial_deal op false kwam te staan en de active game op true.
Spel getest met modifier geselecteerd en modifier uitgeschakeld. Alles werkt zoals behoren. 
De volgende stap is een visuele melding maken dat de modifier actief is. 

Geprobeerd om op basis van de deal knop, zelf de 'lucky hand active' tekst te maken. Deze komt nu tevoorschijn voor de hand gedeald is. Beter zou zijn op het moment dat de eerste hand gedeald is. Om dit te doen, functie aangepast zodat de tekst pas komt na de eerste hand gedeald is. Nu zoeken hoe ik de tekst kan laten verdwijnen na enkele seconden, of eerder animatiegericht er iets mee kan doen. Hiervoor de documentatie van pygame geraadpleegd. 

## 27 april 2026 08:10
Geprobeerd om de modifier text weer te geven op het moment dat de deal knop ingedrukt wordt. Het idee was een zwart scherm met de tekst in het wit erop, dewelke verdwijnt na 3 seconden. Eerste poging zorgt ervoor dat de 'deal' tekst vervangen wordt door de nieuwe tekst en de andere knoppen niet meer werken. Geprobeerd het aan te passen op basis van informatie gevonden op reddit, maar het nog niet werkend gekregen. Als ik nu de game opstart, krijg ik meteen mijn modifier tekst en niet meer de deal button. Uiteindelijk door veranderingen in mijn render volgorde aan te brengen, de deal hand knop terug zichtbaar gekregen. Helaas met er op te klikken, krijg ik mijn zwart scherm zonder tekst en sluit de game af. 

## 1 mei 2026 13:59
Debug mode gebruikt om te kijken waar het fout loopt. Er zat vanalles mis in mijn logica en volgorde waarin de code uitgevoerd werd. Dit aangepast en ook enkele stukken code (zoals de calculate_score functie) gerefactored tot een efficiëntere, minder foutgevoelige functie. Uiteindelijk bleek alles te werken, maar blijft de 'new deal' knop staan tijdens het weergeven van de tekst van de modifier. Dit moet ik nog aanpassen. Dit bleek eenvoudig te zijn door enkel een conditie aan de if statement toe te voegen. Met nu het spel te spelen, werd dit goed weergegeven. Probleem dat nu naar voor komt, is dat de new_hand knop niet werkt. Dit opgelost door een nieuwe conditie in de game-loop toe te voegen. Alles werkt nu naar behoren. Hetgene wat me wel stoort is dat als de speler nu busted is tijdens de game, het meteen verspringt naar de knop 'new hand', waardoor je de kans niet krijgt om te kijken welke kaarten je had. Met verder te zoeken, blijkt dat de busted en new hand knop in dezelfde event loop zitten als 'mousebuttonup'. Om dit te omzeilen moet ik een nieuwe variabele toevoegen (result_just_happend) en deze toevoegen net na check_end_game. Zo weten we dat het weergegeven resultaat een nieuw resultaat is. 
Behoorlijk frusterend als je iets doet werken en de rest is stuk. Nu is er hetzelfde probleem bij de andere speluitkomsten. 


## 5 mei 2026 15:36
Besloten om het toevoegen van de tekst voorlopig achterwege te laten. De aanpassingen maakten mijn code heel erg onoverzichtelijk. Via Github naar een eerdere versie van de code gegaan en deze gebruikt om verder te werken. Het toevoegen van de tekst ga ik op een andere manier implementeren in plaats van de bewegende tekst voor het dealen van de kaarten. Eerst verder werken aan de verschillende modifiers. 
De modifier wordt gekozen op het moment dat een nieuwe ronde start, zodat de spelregels vastliggen voor de volledige hand.
Voor Dealer Risky Mode heb ik de dealer-logica geparametriseerd met een dealer_stand_limit in plaats van vaste waarden te gebruiken. Door deze modifier toe te voegen merkte ik dat ook in andere functies deze waarden verborgen zaten. Daarom heb ik de dealer_stand_limit geparametriseerd en toegevoegd als parameter aan de end_game functie. 
Ik merkte dat er enkel bij de eerste deal na het starten van de game een modifier gekozen werd en deze dus steeds dezelfde bleef bij volgende games. Dit kwam omdat bij de new_hand er geen nieuwe modifier gekozen werd. In plaats van dezelfde stappen als bij new_deal toe te voegen,  heb ik een helperfunctie gemaakt om dit uit te voeren. Deze heb ik dan geïmplementeerd in de bestaande functies (bij deal en new_hand)

No soft aces modifier toegevoegd. Dezelfde hulpfunctie gebruikt zodat er bij elke ronde een nieuwe modifier gekozen wordt. De logica van de no soft aces zit hem in de score berekening. Een ace is dan altijd 11. Deze functie hieraan aangepast door een if statement toe te voegen. 

## 8 mei 2026 13:56
Verder aan mijn project willen werken, maar eerst het spel nog eens willen spelen om te kijken of alles werkt naar behoren. Krijg ik een foutmelding 'ModuleNotFoundError' waarbij de pygame module niet gevonden wordt. Gegoogled wat dit wil betekenen en tot de conclusie gekomen dat de foutmelding komt omdat pygame niet beschikbaar is voor mijn Python environment. Ik heb nochtans de virtuele environment opgestart, maar pas nadat ik VisualStudioCode opgestart had. VS Code afgesloten en nogmaals geprobeerd. Dit heeft het probleem opgelost.
In de lijst van game-modifiers ook None toegevoegd, zodat soms het spel ook gewoon speelt volgens de originele opzet.

De volgende stappen die ik wil doen aan de game is geluiden zetten bij player wins, player busted, dealer wins and tie game. Via Google gezocht hoe dit gedaan wordt. Uitgekomen op de Pygame mixer. Deze informatie verder bekeken. Gezien dat ik zelf voor de geluidsbestanden moet zorgen. Deze gezocht op Pixabay omdat deze rechtenvrij zijn. Om de pygame.mixer.Sound goed te laten werken, mijn mp3 geluidsbestanden geconverteerd naar wav. Geluiden implementeren in de game loop was vrij straightforward, enkel blijven ze spelen tot je op new_deal klikt. Opgezocht hoe ik ervoor kan zorgen dat het geluidseffect maar 1x afgespeeld wordt. De oplossing was eenvoudig, ik had het afspelen van de geluiden in de draw_game functie gezet, maar deze wordt elke frame uitgevoerd zolang het resultaat niet 0 is, waardoor het geluid zich bleef herhalen. De oplossing was om het afspelen van het geluid toe te voegen aan de check_endgame functie. 

Omdat deze modificaties en aanpassingen minder tijd vroegen dan eerst gedacht (vooral eens de eerste modifier werkte, was het toevoegen van de anderen niet zo moeilijk, net zoals het toevoegen van het geluid) is er nog ruimte over om verdere aanpassingen te doen. 
Enkele ideeën die ik ga verkennen:
- card-slide geluiden
- kaarten laten glijden op het scherm, in plaats van onmiddelijk tevoorschijn te komen
- Casino achtig door het toevoegen van kapitaal en inzet
- kaartafbeeldingen toevoegen
- visueel het spel aantrekkelijker maken

## 19 mei 2026 9:43
Kaarten aangepast door afbeeldingen toe te voegen zodat het echt kaarten zijn. Code gevonden op het internet die ik gewoon kon implementeren zonder veel aanpassingen te moeten doen. Daarnaast ook een backup toegevoegd zodat indien om een of andere reden de afbeeldingen niet beschikbaar zouden zijn, de gekleurde rechthoeken opnieuw gebruikt worden. 

Ik merk nu wel bij het spel, als de dealer uiteindelijk 4 kaarten heeft, dat zijn score achter de kaarten verdwijnt. Scherm 100 pixels breder gemaakt en de knoppen en score text 50 pixels naar rechts verplaatst. Merk dat de score nu niet meer achter de kaarten verdwijnt, maar toch nog erg kort erbij staat. Score nog 10 pixels naar rechts verplaatsen en kijken hoe dit er uit ziet. Dit blijkt beter maar nog erg nipt, ik voeg er nog 5 pixels bij. Dit is veel beter, hoewel het probleem blijft bestaan als de dealer 5 kaarten heeft. Voorlopig dit zo gelaten omdat dit erg zelden voorkomt in de game. 

De volgende aanpassing die ik wil doorvoeren is het toevoegen van slide bewegingen aan de kaarten. Dus zodat bij het dealen van een kaart de kaart op het scherm schuift en niet gewoon verschijnt. Dit bleek een moeilijke uitdaging te zijn. Uiteindelijk een voorbeeld gevonden op het internet en mijn code hieraan aangepast. Het werken met de x en y coordinaten viel mee, maar de volledige animatie programmeren blijkt moeilijker te zijn. Uiteindelijk hulp gevraagd via contacten op Reddit die ik heb, en zij hebben mij erg vlot kunnen verder helpen met mijn code. 

Het laatste dat ik wil toevoegen zijn slide geluiden bij het komen van de kaarten. mp3 bestand gevonden op Pixabay. Ik ga proberen dezelfde stappen te volgen als de win/busted/loss geluiden. Het geluid moet enkel toegevoegd worden aan de deal_cards functie, want de andere functies zoals initial_deal maken gebruik van de deal_cards functie. 

## 28 mei 2026 10:08
Laatste controle van het spel. Ontdekt dat de kaarten van de dealer altijd verborgen blijven, ook als de hidden dealer modifier niet actief is. Blijkt dat het probleem zit bij de logica van het verbergen van de dealer kaart, niet in de modifier. In deze logica werd geen rekening gehouden met de modifier, enkel met de reveal parameter. Dit aangepast en opnieuw getest. Nu zijn de dealer kaarten zichtbaar, maar allemaal, dus de eerste kaart blijft niet verborgen. Dit opgelost.

##  1 juni 2026
Feedback ontvangen op mijn code. Het belangrijkste dat ik eruit gehaald heb is dat ik best veel code en of waarden herhaald heb. Ik ga er volledig akkoord want met mijn code na te kijken merk ik nu zelf dat ik niet erg dry gewerkt heb. Ik ga dit zeker meenemen als aandachtpunt naar toekomstige projecten. 
Ik ga wel verduidelijk vragen op de feedback omtrent mijn modifiers_list. De None zou niet nodig zijn, maar dit begrijp ik niet helemaal goed. Zoals ik het zie zou er zonder de None bij elke ronde een modifier zijn, en wordt er dus nooit een ronde gespeeld zonder modifiers. Dat is de reden waarom ik de None ook aan deze lijst toegevoegd heb. Dit ga ik zeker navragen. 
Ook de tip omtrent het gebruik van een dictionary voor het kaartdek is een heel goede tip. In de tutorial wordt ook met een lijst gewerkt en met het nadien toevoegen van de afbeeldingen voor de kaarten, heb ik hier verder niet stil bij gestaan. 

# Hva er dette?
En enkel båtsimulator. Den kan brukes til å simulere en ekte båt. Dersom du skal lage et program som skal styre en båt er det ganske sikkert at koden din ikke vil virke på første forsøk. Kanskje er det en feil med koden som gjøre at båten forsvinner ut på havet, og aldri kommer tilbake. Kjedelig. Da er det lurere å teste programmet sitt på en simulator. 

Dette er en simlator som du kan styre. Når starter simulatoren åpnes følgende vindu
![skjermbilde](/img/screenshot1.png "Simulator")

Båten står da helt stille midt på skjermen. For å få båten til å kjøre må du skrive et program som styrer den. I fila `my-program.py` er det et enkelt program som får båten til å kjøre litt rundt.
# Hvordan komme igang?
Du må gjøre følgende
* Ha python installert
* Sjekke hvilken versjon av python du har installert. Åpne et kommandovindu og skriv `py.exe --version`
* Installere `pygame`. Det gjør du ved å skrive `pip install pygame` (har du python versjon 3.11, legg til ` --pre` etter pygam)
* Laste ned denne koden

## Start simulatoren
Navigere til der du lasta ned koden og inn i folderen `/simulator`. Åpne et kommandovindu, derfra kjører du `py.exe main.py` Da skal simulatoren starte. (den kan deretter kjøre hele tiden)

## Start ditt program
Åpne et annet kommandovindu der du lasta ned koden. Kjør `py.exe my-program.py`. Da skal båten starte

Slik kan det se ut når den har kjørt litt.

Dette er en simlator som du kan styre. Når starter simulatoren åpnes følgende vindu
![skjermbilde](/img/screenshot2.png "Simulator")

# Slik kan du styre båten med kode
Først må du inkludere et bibliotek som snakker med simulatoren. Biblioteket er en fil som heter `coolsim.py`. Dette er hvordan du kan starte begge motorene
```python
import simulator.coolsim as cs

# Sett begge motorene til å gå framover - hastighet 3  (10 er full fart. 1 er sakte. -10 er full fart bakover)
cs.set_engine_levels(3,3)

# la de gå i 5 sekunder
time.sleep(5)

# Sving litt til venstre
cs.set_engine_levels(3,0)

# sving i 2 sek
time.sleep(2)

# stop
cs.set_engine_levels(0,0)

```
Koden over vil få båten til å gå rett fram i 5 sekunder, deretter svinger den litt (fordi venstre motor går, mens høyre er stoppet)

## Init fila
Init funksjonen kan du gjøre litt forskjellig med:

```python
# Konfigurer simulatoren (bestem hvordan den skal virke)
# show_tail - viser en hale etter båten
# screen_size - størrelsen på "havet". I pixler.
# targets - en liste med posisjoner som blir tegnet med en rød running. 
#           dette kan f.eks være steder du skal navigere til

cs.init(show_tail=1, screen_size=[400,600], targets=[[350,550]])

```

## Sensorer
For å navigere må du vite hvor du er. Derfor trenger vi sensorer. Simulatoren simulerer to "sensorer", kompass og GPS

```python
# Finn ut posisjonen til båten. (simulerer en GPS)
# Denne returner en [x,y] som referer til vindus størrelsen som ble satt opp i init kallet
boat_position = cs.get_position()

# Finn retningen til båten. (simulerer et kompass)
# Denne returner antall grader. 0 er nord, 180 er sør.
boat_direction = cs.get_direction()

# skriv ut hvor båten er
print("Compass:" +str(boat_direction) + " Position:" + str(boat_position[0]) + "," + str(boat_position[1]))

```
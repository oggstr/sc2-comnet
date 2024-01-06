# TDDD92 - Förutspå Stridsutfall med Bayesianska Nätverk

Detta projekt bygger ett bayesianskt nätverk som, givet enheter för två spelare, förutspår chansen att någon spelare vinner.

## Struktur

Projektet är uppdelat i tre delar:

1. Byggande & Träning
2. Testning
3. Använding

### Byggande & Träning
Byggande och träning av nätverket finns i `train.py`. Koden börjar med att registera vilka enheter samt vilka attribut som ska moduleras. Dessa registreras i `Network` (`netowrk.py`).

`Netowrk` har två huvudsakliga uppgifter. Dels bygger den upp bågar mellan alla noder i nätverket. Dels hämtar den simulerings data via `/data/parse.py`. Detta, samt alla kontinuerliga noder, returneras till `train.py`.

Vidare används biblioteket `bnlearn` för träning. Först diskritiseras alla värden för alla kontinuerliga noder. Sen tränas nätverket med `MLE`.

Sist skapas ett `Model` (`model.py`) objekt. Detta sparas sedan via `pickle`.

### Testning

Simpel testning kan göras via `test.py`. Programmet laddar in ett sparat nätverk (`Model.load()`). Efter detta körs ett antal prediktioner som skrivs ut i terminalen.

### Användning

Då träning av nätverket tar väldigt lång tid (flera timmar) är det inte rimligt att träna nätverket under spelets gång. Integrering krävs alltså att ett tränat närverk kan sparas. I python görs detta enkelt med biblioteket `pickle`. Detta hanteras av `Model` (`model.py`).

`Model`-klassen hanterar inte bara sparning och inladdning av nätverket, utan abstraherar också över `bnlearn`. Prediktion med `Model` görs enligt:

```python
with model.prediction():
    # Spelare 0
    model.use_unit_count(0, "Marine", 50)
    model.use_unit_count(0, "Reaper", 30)

    # Spelare 1
    model.use_unit_count(1, "Marine", 80)
    model.use_unit_count(1, "Maruder", 10)

    # Prediktion att spelare 0 vinner
    prob = model.make_prediction(0)
```

* `with model.prediction()` påbörjar en ny prediktion
* `model.use_unit_count(player, unit, count)` sätter antalet enheter för en viss spelare
* `model.make_prediction(player)` utför prediktionen

## Modulerade enheter

I nuläget modulerar nätverket följande:

* `Marines`
* `Reaper`
* `Marauder`
* `SiegeTank`
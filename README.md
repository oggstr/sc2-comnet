# TDDD92 - Predicting Combat Outcomes in SC2 using Bayesian Networks

Note, README is available in Swedish below!
<br/>
This project builds a bayesian network that, given the units of two players, predicts the chance of a player winning a fight.

## Structure

The project is split in three parts:

1. Building & Training
2. Testing
3. Making predictions

### Building & Training
Both building and training can be found in `train.py`. The code begins by registering what units and what attributes to model. This is registered in `Network` (`netowrk.py`).

`Network` has two main responsibilities. First, it builds and adges and nodes in the network. Second, it parses all the data (using `/data/parse.py`) and computes derived data. This, and what nodes are continuous nodes, are returned to `train.py`.

After, `bnlearn` is used for training. It first discretizes all continuous nodes values. Then it trains the network using `MLE`.

Lastly, it creates a `Model` (`model.py`) object. This object is then saved using `pickle`.

### Testing

Simple prediction testing can ve done via `test.py`. This files loads a stored model (`Model.load()`). Then makes a number of predictions that are printed to the console.

### Integration

Since training the network takes a very long time (several hours) it's not feasible to train it during a SC2 game. Integration in an AI-agent therefore requires that a model can be saved. This easily done with Python's `pickle` library. Saving and loading is done by `Model` (`model.py`).

The `Model`-class doesn't only handle saving and loading the model, it also abstracts over `bnlearn`. Predictions with `Model` is easily done by:

```python
with model.prediction():
    # Player 0
    model.use_unit_count(0, "Marine", 50)
    model.use_unit_count(0, "Reaper", 30)

    # Player 1
    model.use_unit_count(1, "Marine", 80)
    model.use_unit_count(1, "Maruder", 10)

    # Prediction that player 0 wins
    prob = model.make_prediction(0)
```

* `with model.prediction()` starts a new preductuib
* `model.use_unit_count(player, unit, count)` sets the unit count of some unit for a player (0 or 1)
* `model.make_prediction(player)` Makes a prediction

## Modeled units

Currently, the following units are modeled:

* `Marines`
* `Reaper`
* `Marauder`
* `SiegeTank`

---

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

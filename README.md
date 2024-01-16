# SmartGrid - circuit-solvers-

Groene energie, opgewekt door huishoudelijke installaties zoals zonnepanelen, creëert vaak overschotten. Om deze pieken in energieproductie te beheren, worden batterijen gebruikt. Zo wordt zelfvoorziening efficiënter. Met het smart grid worden huizen via kabels gekoppeld aan een batterij. Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit. Het leggen van kabels levert kosten op, evenals de batterij. Met dit algoritme wordt geprobeerd om de kabels optimaal van huis tot batterij te verbinden en de kosten zo laag mogelijk te houden.

## Aan de slag

### Vereisten

Deze codebase is volledig geschreven in Python 3.7. In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

### Gebruik

Het programma kan gerund worden door aanroepen van:

```
python main.py [-v] <district_number>
```

Met -v wordt via python een visualisatie laten zien.

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algoritmen**: bevat de code voor algoritmes
  - **/code/classes**: bevat de drie benodigde classes voor deze case
  - **/code/vizualization**: bevat de pygame code voor de visualisatie
- **/data**: bevat de verschillende databestanden die nodig zijn om het grid te vullen en te visualiseren

## Auteurs
- Jens Bloemen
- Annelaure van Overbeeke
- Salomé Poulain
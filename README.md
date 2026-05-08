# NLCS Opentool for BricsCAD

BricsCAD plugin om te werken volgens de **Nederlandse CAD Standaard (NLCS) versie 5.0**.

Installeert automatisch:
- **Lagen** (layers) met correcte kleuren, lijntypes en lijngewichten
- **Lijntypes** (linetypes) 
- **Arceringen** (hatches/patterns)
- **Symbolen** (blocks) uit de NLCS bibliotheek
- **Plotstijlen** (.ctb bestanden)

Ondersteunde NLCS hoofdgroepen:
- `AL` Algemeen
- `AM` Assen en metrering
- `BC` Betonconstructies
- `BV` Bermbeveiliging
- `FC` Funderingsconstructies
- `FV` Faunavoorzieningen
- `GC` Grondkerende constructies
- `GK` Grondkeringen
- `GR` Groen
- `GW` Grondwerken
- `HU` Hulpconstructies
- `IE` Inrichtingselementen
- `IV` Installaties Vaarweg
- `IW` Installaties Wegen
- `KC` Kunststofconstructies
- `KG` Kadastrale grenzen
- `KL` Kabels en leidingen
- `KW` Kunstwerken
- `MC` Mechanische constructies
- `MO` Milieuonderzoek
- `MW` Metselwerk
- `OB` Oever- en bodembescherming
- `OG` Ondergrond
- `OV` Openbare verlichting
- `RI` Riolering
- `SC` Staalconstructies
- `VH` Verhardingen
- `VV` Verkeersmaatregelen Vaarweg
- `VW` Verkeersmaatregelen Weg
- `WH` Waterhuishouding
- `ZZ` Diversen (algemeen)

## Installatie

1. Download de nieuwste release van https://github.com/groetg/NLCS-Opentool
2. Pak uit naar een permanente locatie (bijv. `C:\Program Files\NLCS-Opentool`)
3. Start BricsCAD
4. Ga naar **Manage → Load Application → Add**
5. Selecteer `src\__init__.py` of `install\install.py`
6. Herstart BricsCAD

Of via de installatieknop in de plugin UI.

## Gebruik

Na installatie verschijnt er een **NLCS** toolbar of ribbon tab met:

- **Laad NLCS** — Kies disciplines en laad alle bijbehorende lagen
- **Instellingen** — Kies plotstijl, standaard lijngewicht, etc.
- **Help** — Link naar NLCS documentatie

## Vereisten

- BricsCAD v24 of hoger (getest op BricsCAD BIM en BricsCAD Pro)
- NLCS versie 5.0.x

## Ontwikkeling

```bash
# Clone met submodule
git clone --recurse-submodules https://github.com/groetg/NLCS-Opentool.git
cd NLCS-Opentool

# Bekijk de NLCS data
ls data/nlcs/
```

## Over NLCS

De Nederlandse CAD Standaard (NLCS) is de nationale standaard voor infrastructuurontwerp in Nederland, beheerd door DigiGO. Zie https://github.com/nl-digigo/NLCS voor meer informatie.

## Licentie

Proprietary — zie LICENSE bestand. De NLCS data zelf valt onder CC BY 4.0 (DigiGO).

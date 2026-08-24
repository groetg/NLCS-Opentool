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

### Automatisch (aanbevolen)

1. Download de nieuwste release of clone de repo:
   ```bash
   git clone --recurse-submodules https://github.com/groetg/NLCS-Opentool.git
   ```
2. Windows: dubbelklik `install/install.py` in Windows Verkenner.
3. Linux: voer vanuit de repository uit:
   ```bash
   python3 install/install.py
   ```
   Als BricsCAD niet automatisch gevonden wordt, geef de supportmap op:
   ```bash
   python3 install/install.py --support-dir "$HOME/Bricsys/BricsCAD/V24/en_US/Support"
   ```
4. Python 3.7+ moet geïnstalleerd zijn.

Dit installeert alle NLCS resources en de LISP-plugin naar je BricsCAD support directory.
De Linux-gebruikersmap van BricsCAD staat normaal onder
`~/Bricsys/BricsCAD/V<versie>/en_US/Support`.

### Handmatig via BricsCAD (voor developers)

Na de automatische installatie:

1. Start BricsCAD opnieuw op
2. Typ `APPLOAD` in de command line
3. Klik **Add** en selecteer `NLCS-Opentool/nlcs_main.lsp` uit de supportmap.
4. Typ `NLCS` om de tool te starten.

## Gebruik

Na installatie verschijnt er een **NLCS** toolbar of ribbon tab met:

- **Laad NLCS** — Kies disciplines en laad alle bijbehorende lagen
- **Instellingen** — Kies plotstijl, standaard lijngewicht, etc.
- **Help** — Link naar NLCS documentatie

## Vereisten

- BricsCAD v24 of hoger (Windows of Linux; Linux moet nog op de doelmachine worden gevalideerd)
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

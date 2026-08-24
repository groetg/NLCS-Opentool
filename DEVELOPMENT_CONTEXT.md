# NLCS Opentool - Development Context

## Project

Repository: `https://github.com/groetg/NLCS-Opentool`

The project is a BricsCAD plugin for NLCS. Development is being done on a
Windows Framework 16 laptop and tested on a Linux Mint LaptopRevive machine.
The Linux test machine runs BricsCAD Pro V26.2.07 x64.

## Current architecture

- The current implementation is AutoLISP plus DCL.
- `src/nlcs_main.lsp` is loaded through `APPLOAD`.
- `src/nlcs_layers.lsp` is generated from NLCS CSV data.
- `install/install.py` installs resources and LISP/DCL files into the BricsCAD
  support directory.
- The Lite fallback must remain pure AutoLISP and native BricsCAD Tool
  Palettes compatible.
- A separate BRX/C++ modeless interface is planned for BricsCAD Pro and higher.

## Important product decision

Do not replace the Lite fallback with BRX. The target is a shared NLCS/block
data model with two frontends:

1. Lite: AutoLISP and native Tool Palettes.
2. Pro+: Linux/Windows BRX modeless interface, similar to Infradesign.

## Implemented so far

- Linux support directory detection, including `V26x64/en_US/Support`.
- Installer option `--support-dir`.
- Installation of hatches, linetypes, plotstyles, DWG symbols and LISP/DCL
  plugin files.
- Dynamic path resolution when loading the LISP file through an absolute path.
- `defvar` removed because BricsCAD AutoLISP does not support it.
- NLCS CSV parser fixed for the quoted NLCS 5.02 export format.
- Correct basic property columns are used: `lw_b` column 6, `kl_b` column 7,
  and `lt_b` column 12.
- Object table filenames are found by discipline code plus their full suffix.
- `kind_van` is included in generated layer data.
- Layer browser supports an indented expandable tree with multiple expanded
  branches.
- Status prefixes are supported: `N-`, `B-`, `V-`, `T-`, and `R-`.
- Object suffix selection is supported: `-G`, `-S`, `-M`, and text suffixes
  `-T18`, `-T25`, `-T35`, `-T50`.
- Layer color, lineweight and linetype can be edited before creation.
- Created layers are set as `CLAYER`.
- A recursive callback bug that made BricsCAD flicker/freeze was fixed.

## NLCS data facts

- The repository submodule is `data/nlcs` from `https://github.com/nl-digigo/NLCS`.
- The included published data is NLCS 5.02, not the consultation document
  NLCS 5.1.
- The official consultation specification used for requirements is:
  `https://nl-digigo.github.io/NLCS/functionalspecification/reviewversies/CR-NLCS_functionalspecification-20241017.html`
- The object table contains `kind_van`, which forms the hierarchy.
- Example: `VH-KANTOPSLUITING_OPSLUITBAND` has children including
  `..._100X200`, `..._100X300`, `..._100X400`, `..._150X250`,
  `..._150X300`, `..._150X400`, `..._60X150`, `..._60X200`,
  `..._80X200`, and `...-OPNIEUW STELLEN`.
- The symbol table is `data/nlcs/tabellen/publicatie/5.02-symbolen.csv`.
- Symbol library metadata is `data/nlcs/tabellen/publicatie/5.02-sbibliotheken.csv`.
- There are about 3570 DWG files under `data/nlcs/symbolen/autocad/`.

## Current limitation

Standard AutoLISP/DCL is modal. It cannot provide a persistent modeless
Infradesign-like panel while the user draws. The BRX modeless frontend is not
built yet. The current LISP version closes after layer creation and makes the
new layer current.

## BRX plan

- Download the all-platform BRX SDK from Bricsys Developer Resources. The SDK
  is separate from BricsCAD and is available to registered developers.
- For BricsCAD V26.2.07 use the matching V26.2 all-platform SDK available from
  Bricsys, currently listed as `BRXSDK_Bcad_V26_2_03.zip`.
- Do not use the Windows `.msi` on Linux.
- Linux build prerequisites: `build-essential`, `cmake`, and `unzip`.
- The SDK is needed only to build the `.brx`; it is not installed into the
  user's BricsCAD support directory.
- BRX is available for BricsCAD Pro and higher, not Lite.

## Block integration plan

Do not guess block paths from object names alone. Build an index from the
NLCS symbol table and the actual DWG filenames. The intended workflow is:

1. Select an NLCS object in the hierarchy.
2. Show linked symbol/block choices.
3. Select a DWG symbol.
4. Apply the selected status and object layer.
5. Insert the DWG at the picked point and keep the correct layer current.

## Synchronization workflow

On Windows after changes:

```bash
git add src install README.md DEVELOPMENT_CONTEXT.md .gitignore
git commit -m "Describe the change"
git pull --rebase origin main
git push origin main
```

On Linux:

```bash
cd ~/NLCS-Opentool
python3 install/install.py
```

Never commit the BRX SDK ZIP. It is ignored by `.gitignore`.

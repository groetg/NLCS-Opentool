# NLCS BRX Core

This directory contains the first BRX architecture slice: an SDK-independent
block index. It reads `5.02-symbolen.csv`, scans the real DWG library, and
returns symbol choices with resolved paths. Unresolved records remain in the
index so a future modeless UI can show an installation warning rather than
guessing a path from an object name.

Build and run the core test from the repository root:

```bash
cmake -S brx -B build/brx
cmake --build build/brx
ctest --test-dir build/brx --output-on-failure
```

To build the first Linux BRX module, set the SDK path before configuring:

```bash
export BRX26_SDK_PATH="$HOME/BRXSDK/V26.2"
cmake -S brx -B build/brx
cmake --build build/brx
```

On a standard Linux installation the runtime is found at
`/opt/bricsys/bricscad/v26`. Override it with `BRX26_RUNTIME_PATH` if BricsCAD
is installed elsewhere. The SDK import libraries in `lib64/*.lib` are not
Linux runtime libraries and are deliberately not linked.

This produces `build/brx/nlcs_brx.lrx`. Set the project path before starting
BricsCAD, then use `NLCSBLOCKS` to verify the BRX-to-data connection:

```bash
export NLCS_OPENTOOL_ROOT="$PWD"
```

The command reports the number of symbol records and resolved SOV DWGs. The
modeless panel is the next implementation step. `NLCSINSERT` provides the
first command-line library workflow: search for a term such as `lichtmast`,
choose a result, and pick an insertion point. The command first asks for a
status (`N`, `B`, `V`, `T`, or `R`) and a discipline such as `WE` or `RI`.
Technical symbol names are not required.

The experimental Qt panel is disabled by default because BricsCAD may use a
different Qt runtime. Enable it only for compatibility experiments with
`-DNLCS_ENABLE_QT_PANEL=ON`.

The test executable expects the CSV and DWG root as its two arguments. When
run through CTest, these paths are registered automatically. The current CMake
test registration is intentionally SDK-independent; the BRX adapter and
modeless palette will be added separately against the matching
V26.2 all-platform SDK (`BRXSDK_Bcad_V26_2_03.zip`).

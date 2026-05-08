"""
NLCS Opentool - Installatie Script (Standalone)

Dit script kan dubbelklikt worden in Windows Verkenner of gedraaid worden
via Python zonder BricsCAD.

Installatie stappen:
1. Dubbelklik dit bestand OF
2. Right-click → "Openen met" → Python

Python 3.7+ vereist.
"""

import os
import sys
import shutil
import platform


def get_bricscad_support_dir() -> str:
    """Vind de BricsCAD support directory."""
    system = platform.system()
    
    if system == "Windows":
        appdata = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
        home = os.path.expanduser("~")
        
        # Try common BricsCAD versions
        versions = ["BricsCAD_v25", "BricsCAD_v24", "BricsCAD_v23", "BricsCAD"]
        for v in versions:
            path = os.path.join(appdata, v, "Support")
            if os.path.exists(path):
                print(f"  Gevonden: {v}")
                return path
        
        # Fallback to latest version we can find
        common = os.path.join(appdata, "BricsCAD")
        if os.path.exists(common):
            subdirs = [d for d in os.listdir(common) if d.startswith("BricsCAD_v")]
            if subdirs:
                latest = sorted(subdirs)[-1]
                return os.path.join(common, latest, "Support")
        
        # Last resort
        return os.path.join(appdata, "BricsCAD", "BricsCAD_v24", "Support")
    
    elif system == "Linux":
        home = os.path.expanduser("~")
        return os.path.join(home, ".bricscad", "BricsCAD_v24", "Support")
    
    else:
        # macOS
        home = os.path.expanduser("~")
        return os.path.join(home, "Library", "Application Support", "BricsCAD", "BricsCAD_v24", "Support")


def find_nlcs_data() -> str:
    """Zoek de NLCS data directory."""
    # Dit script staat in NLCS-Opentool/install/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nlcs_opentool_dir = os.path.dirname(script_dir)  # up from install/
    nlcs_data_dir = os.path.join(nlcs_opentool_dir, "data", "nlcs")
    
    if os.path.exists(nlcs_data_dir):
        return nlcs_data_dir
    
    # Try current directory
    current = os.getcwd()
    nlcs_data_dir = os.path.join(current, "data", "nlcs")
    if os.path.exists(nlcs_data_dir):
        return nlcs_data_dir
    
    return ""


def install_hatches(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS .pat hatch files naar BricsCAD support/hatch/."""
    pat_src = os.path.join(nlcs_data_dir, "arceringen")
    hatch_dst = os.path.join(support_dir, "hatch")
    
    if not os.path.exists(pat_src):
        return 0
    
    os.makedirs(hatch_dst, exist_ok=True)
    count = 0
    for f in os.listdir(pat_src):
        if f.endswith(".pat"):
            src_path = os.path.join(pat_src, f)
            dst_path = os.path.join(hatch_dst, f)
            shutil.copy2(src_path, dst_path)
            count += 1
    return count


def install_linetypes(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS .lin en .shx bestanden naar BricsCAD support/."""
    lin_src_dir = os.path.join(nlcs_data_dir, "lijntypes", "autocad")
    
    if not os.path.exists(lin_src_dir):
        return 0
    
    count = 0
    for f in os.listdir(lin_src_dir):
        if f.endswith(".lin") or f.endswith(".shx") or f.endswith(".shp"):
            src_path = os.path.join(lin_src_dir, f)
            dst_path = os.path.join(support_dir, f)
            shutil.copy2(src_path, dst_path)
            count += 1
    return count


def install_plotstyles(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS .ctb plotstyle bestanden naar BricsCAD support/plotstyles/."""
    ctb_src_dir = os.path.join(nlcs_data_dir, "plotinstellingen")
    plotstyle_dst = os.path.join(support_dir, "plotstyles")
    
    if not os.path.exists(ctb_src_dir):
        return 0
    
    os.makedirs(plotstyle_dst, exist_ok=True)
    count = 0
    for f in os.listdir(ctb_src_dir):
        if f.endswith(".ctb"):
            src_path = os.path.join(ctb_src_dir, f)
            dst_path = os.path.join(plotstyle_dst, f)
            shutil.copy2(src_path, dst_path)
            count += 1
    return count


def install_symbols(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS symbolen (.dwg) naar BricsCAD Blocks/."""
    sym_src_dir = os.path.join(nlcs_data_dir, "symbolen", "autocad")
    
    if not os.path.exists(sym_src_dir):
        return 0
    
    sym_dst = os.path.join(support_dir, "Blocks", "NLCS")
    os.makedirs(sym_dst, exist_ok=True)
    
    count = 0
    for root, dirs, files in os.walk(sym_src_dir):
        for f in files:
            if f.endswith(".dwg"):
                src = os.path.join(root, f)
                rel = os.path.relpath(root, sym_src_dir)
                dst_dir = os.path.join(sym_dst, rel) if rel != "." else sym_dst
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(src, os.path.join(dst_dir, f))
                count += 1
    return count


def print_header():
    print()
    print("=" * 50)
    print("  NLCS Opentool - Installatie voor BricsCAD")
    print("=" * 50)
    print()


def print_result(name: str, count: int):
    if count > 0:
        print(f"  [+] {name}: {count} bestanden")
    else:
        print(f"  [-] {name}: overgeslagen (geen bestanden)")


def main():
    print_header()
    
    # Find NLCS data
    nlcs_data_dir = find_nlcs_data()
    
    if not nlcs_data_dir or not os.path.exists(nlcs_data_dir):
        print("  [!] FOUT: NLCS data niet gevonden!")
        print()
        print("  Zorg dat dit script in de NLCS-Opentool map staat:")
        print("    NLCS-Opentool/")
        print("    ├── install/")
        print("    │   └── install.py   <-- dit bestand")
        print("    └── data/")
        print("        └── nlcs/")
        print("            └── (NLCS bestanden)")
        print()
        print("  OF clone de repo met submodule:")
        print("    git clone --recurse-submodules https://github.com/groetg/NLCS-Opentool.git")
        print()
        input("Druk op Enter om af te sluiten...")
        sys.exit(1)
    
    print(f"  NLCS data: {nlcs_data_dir}")
    print()
    
    # Find BricsCAD support dir
    support_dir = get_bricscad_support_dir()
    print(f"  BricsCAD Support: {support_dir}")
    
    if not os.path.exists(support_dir):
        print()
        print("  [!] BricsCAD support directory niet gevonden.")
        print("  Heeft u BricsCAD al geïnstalleerd?")
        print()
        input("Druk op Enter om af te sluiten...")
        sys.exit(1)
    
    print()
    print("  Installeren...")
    print()
    
    # Install components
    hatches = install_hatches(nlcs_data_dir, support_dir)
    print_result("Arceringen (.pat)", hatches)
    
    linetypes = install_linetypes(nlcs_data_dir, support_dir)
    print_result("Lijntypes (.lin/.shx)", linetypes)
    
    plotstyles = install_plotstyles(nlcs_data_dir, support_dir)
    print_result("Plotstijlen (.ctb)", plotstyles)
    
    symbols = install_symbols(nlcs_data_dir, support_dir)
    print_result("Symbolen (.dwg)", symbols)
    
    print()
    print("=" * 50)
    print("  Installatie voltooid!")
    print("=" * 50)
    print()
    print("  Volgende stappen:")
    print("  1. Start BricsCAD opnieuw op")
    print("  2. Typ APPLOAD → Add → src/__init__.py")
    print("  3. Gebruik de NLCS toolbar om disciplines te laden")
    print()
    print("  Of draai de installatieknop in de plugin UI.")
    print()
    print("  Zie ook: https://github.com/groetg/NLCS-Opentool")
    print()
    
    input("Druk op Enter om af te sluiten...")


if __name__ == "__main__":
    # If running from Windows Explorer (graphical), add input() pause at end
    main()

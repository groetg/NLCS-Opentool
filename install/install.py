"""
NLCS Opentool Installatie Script

Dit script kopieert NLCS resources naar de BricsCAD support directory.
Kan standalone draaien buiten BricsCAD om.
"""

import os
import sys
import shutil
import platform


def get_bricscad_support_dir() -> str:
    """Vind de BricsCAD support directory."""
    system = platform.system()
    
    if system == "Windows":
        # BricsCAD stores settings in %APPDATA%
        appdata = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
        # Try to find version
        home = os.path.expanduser("~")
        common = os.path.join(appdata, "BricsCAD")
        if os.path.exists(common):
            # Find latest version
            versions = [d for d in os.listdir(common) if d.startswith("BricsCAD_v")]
            if versions:
                latest = sorted(versions)[-1]
                return os.path.join(common, latest, "Support")
        # Fallback
        return os.path.join(appdata, "BricsCAD", "BricsCAD_v24", "Support")
    
    elif system == "Linux":
        home = os.path.expanduser("~")
        return os.path.join(home, ".bricscad", "BricsCAD_v24", "Support")
    
    else:
        # macOS
        home = os.path.expanduser("~")
        return os.path.join(home, "Library", "Application Support", "BricsCAD", "BricsCAD_v24", "Support")


def install_hatches(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS .pat hatch files naar BricsCAD."""
    pat_src = os.path.join(nlcs_data_dir, "arceringen")
    hatch_dst = os.path.join(support_dir, "hatch")
    os.makedirs(hatch_dst, exist_ok=True)
    
    count = 0
    if os.path.exists(pat_src):
        for f in os.listdir(pat_src):
            if f.endswith(".pat"):
                shutil.copy(os.path.join(pat_src, f), os.path.join(hatch_dst, f))
                count += 1
    return count


def install_linetypes(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS .lin en .shx bestanden naar BricsCAD."""
    lin_src_dir = os.path.join(nlcs_data_dir, "lijntypes", "autocad")
    
    count = 0
    if os.path.exists(lin_src_dir):
        for f in os.listdir(lin_src_dir):
            if f.endswith(".lin") or f.endswith(".shx"):
                shutil.copy(os.path.join(lin_src_dir, f), os.path.join(support_dir, f))
                count += 1
    return count


def install_plotstyles(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS .ctb plotstyle bestanden naar BricsCAD."""
    ctb_src_dir = os.path.join(nlcs_data_dir, "plotinstellingen")
    plotstyle_dst = os.path.join(support_dir, "plotstyles")
    os.makedirs(plotstyle_dst, exist_ok=True)
    
    count = 0
    if os.path.exists(ctb_src_dir):
        for f in os.listdir(ctb_src_dir):
            if f.endswith(".ctb"):
                shutil.copy(os.path.join(ctb_src_dir, f), os.path.join(plotstyle_dst, f))
                count += 1
    return count


def install_symbols(nlcs_data_dir: str, support_dir: str) -> int:
    """Kopieer NLCS symbolen (.dwg) naar BricsCAD."""
    sym_src_dir = os.path.join(nlcs_data_dir, "symbolen", "autocad")
    sym_dst = os.path.join(support_dir, "BricsCAD", "Blocks")
    os.makedirs(sym_dst, exist_ok=True)
    
    count = 0
    if os.path.exists(sym_src_dir):
        for root, dirs, files in os.walk(sym_src_dir):
            for f in files:
                if f.endswith(".dwg"):
                    src = os.path.join(root, f)
                    # Preserve subdirectory structure
                    rel = os.path.relpath(root, sym_src_dir)
                    dst_dir = os.path.join(sym_dst, rel) if rel != "." else sym_dst
                    os.makedirs(dst_dir, exist_ok=True)
                    shutil.copy(src, os.path.join(dst_dir, f))
                    count += 1
    return count


def main():
    """Run the installation."""
    # Find NLCS data (assume this script is in NLCS-Opentool/install/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nlcs_opentool_dir = os.path.dirname(script_dir)  # go up from install/
    nlcs_data_dir = os.path.join(nlcs_opentool_dir, "data", "nlcs")
    
    if not os.path.exists(nlcs_data_dir):
        print("FOUT: NLCS data niet gevonden. Is de submodule correct gekloond?")
        print(f"  Gezocht in: {nlcs_data_dir}")
        sys.exit(1)
    
    support_dir = get_bricscad_support_dir()
    
    print("=" * 50)
    print("NLCS Opentool - Installatie voor BricsCAD")
    print("=" * 50)
    print(f"Support directory: {support_dir}")
    print()
    
    # Check if running in BricsCAD (has brachyura)
    in_bricscad = False
    try:
        import brachyura
        in_bricscad = True
        print("[+] BricsCAD omgeving gedetecteerd")
    except ImportError:
        print("[*] Geen BricsCAD omgeving — standalone installatie")
    
    print()
    
    if not os.path.exists(support_dir):
        print(f"[!] Support directory bestaat niet: {support_dir}")
        print("    Maak deze aan of installeer BricsCAD eerst.")
        sys.exit(1)
    
    # Install components
    print("[*] Installeren van arceringen...")
    hatches = install_hatches(nlcs_data_dir, support_dir)
    print(f"    {hatches} arceringen geïnstalleerd")
    
    print("[*] Installeren van lijntypes...")
    linetypes = install_linetypes(nlcs_data_dir, support_dir)
    print(f"    {linetypes} lijntype bestanden geïnstalleerd")
    
    print("[*] Installeren van plotstijlen...")
    plotstyles = install_plotstyles(nlcs_data_dir, support_dir)
    print(f"    {plotstyles} plotstijlen geïnstalleerd")
    
    print("[*] Installeren van symbolen...")
    symbols = install_symbols(nlcs_data_dir, support_dir)
    print(f"    {symbols} symbolen geïnstalleerd")
    
    print()
    print("=" * 50)
    print("Installatie voltooid!")
    print()
    print("Volgende stappen:")
    print("  1. Start BricsCAD opnieuw op")
    print("  2. Ga naar Manage → Load Application → Add")
    print("  3. Selecteer src/__init__.py of dit installatiescript")
    print("  4. Gebruik de NLCS toolbar om disciplines te laden")
    print("=" * 50)


if __name__ == "__main__":
    main()

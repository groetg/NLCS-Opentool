"""
NLCS Loader — leest NLCS tabellen en creëert lagen in BricsCAD.

Ondersteunt zowel BricsCAD (via Brachyura/CPython) als standalone debugging.
"""

import os
import csv
from typing import Optional

# NLCS data directory (git submodule)
_NLCS_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "nlcs")
_TABLE_DIR = os.path.join(_NLCS_DATA_DIR, "tabellen", "publicatie", "objectentabellen-verkort")

# Color indices (ACI) commonly used in NLCS
# 1=red, 2=yellow, 3=green, 4=cyan, 5=blue, 6=magenta, 7=white/black, >7 = specific
# Stored in CSV as numbers like 10, 12, 90, 92, 254, 253
_LW_MAP = {
    0.18: "0.18mm",
    0.25: "0.25mm",
    0.35: "0.35mm",
    0.50: "0.50mm",
    0.70: "0.70mm",
    1.00: "1.00mm",
    1.40: "1.40mm",
}


def get_nlcs_data_path(relative: str) -> str:
    """Return full path to NLCS data file."""
    return os.path.join(_NLCS_DATA_DIR, relative)


def parse_objecttabel(csv_path: str) -> list[dict]:
    """Parse a NLCS objectentabel CSV file.
    
    CSV kolommen (gescheiden door komma's in quoted strings):
    - hoofdgroep: NLCS hoofdgroep code (VH, RI, KL, etc.)
    - id_nummer: object ID
    - omschrijving: object naam
    - kl_b, kl_n, kl_t, kl_v: kleur index (by-axis, niet-by-axis, etc.)
    - lw_b, lw_n, lw_t, lw_v: lijngewicht
    - lt_b, lt_n, lt_t, lt_v: lijntype naam
    - element: block/element type
    """
    objects = []
    if not os.path.exists(csv_path):
        return objects

    # First row is header, but format is complex due to quoted fields
    # Format: "hoofdgroep,""id_nummer"",""omschrijving"",... etc"
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)  # skip header
        
        for row in reader:
            if len(row) < 35:
                continue
            try:
                obj = {
                    "hoofdgroep": row[0].strip(),
                    "id": row[1].strip(),
                    "omschrijving": row[2].strip(),
                    "kl_b": _int_safe(row[9]),
                    "kl_n": row[17].strip() if len(row) > 17 else "",
                    "kl_t": row[25].strip() if len(row) > 25 else "",
                    "kl_v": row[33].strip() if len(row) > 33 else "",
                    "lw_b": _float_safe(row[8]),
                    "lw_n": row[16].strip() if len(row) > 16 else "0.25",
                    "lw_t": row[24].strip() if len(row) > 24 else "0.25",
                    "lw_v": row[32].strip() if len(row) > 32 else "0.25",
                    "lt_b": row[12].strip() if len(row) > 12 else "CONTINUOUS",
                    "lt_n": row[20].strip() if len(row) > 20 else "CONTINUOUS",
                    "lt_t": row[28].strip() if len(row) > 28 else "CONTINUOUS",
                    "lt_v": row[36].strip() if len(row) > 36 else "CONTINUOUS",
                    "element": row[40].strip() if len(row) > 40 else "",
                }
                objects.append(obj)
            except (IndexError, ValueError):
                continue
    return objects


def _int_safe(s: str) -> Optional[int]:
    try:
        return int(s.strip())
    except (ValueError, TypeError):
        return None


def _float_safe(s: str) -> Optional[float]:
    try:
        return float(s.strip().replace(",", "."))
    except (ValueError, TypeError):
        return 0.25


def load_nlcs_layers(disciplines: list[str] = None, target_layer_prefix: str = "") -> int:
    """Load NLCS layers into BricsCAD for given disciplines.
    
    Args:
        disciplines: List of NLCS hoofdgroep codes (e.g. ['VH', 'RI', 'KL'])
                     If None, loads all disciplines
        target_layer_prefix: Optional prefix for layer names (e.g. "NLCS-")
    
    Returns:
        Number of layers created
    
    Raises:
        ImportError: If not running in BricsCAD
    """
    try:
        import brachyura
        from brachyura.console import Console
        from brachyura.rubber import Layer
    except ImportError:
        raise ImportError("NLCS Opentool werkt alleen binnen BricsCAD")

    if disciplines is None:
        disciplines = get_all_disciplines()

    layers_created = 0

    for disc in disciplines:
        csv_file = os.path.join(_TABLE_DIR, f"5.02-Objectentabel-{disc}.csv")
        if not os.path.exists(csv_file):
            continue

        objects = parse_objecttabel(csv_file)
        
        for obj in objects:
            layer_name = f"{target_layer_prefix}{obj['hoofdgroep']}-{obj['omschrijving']}"
            # Truncate to BricsCAD's 255 char limit
            layer_name = layer_name[:255].strip()
            
            # Map kleur naar ACI
            color_index = obj.get("kl_b") or 7  # default white
            
            # Map lijngewicht
            lw = obj.get("lw_b") or 0.25
            lw_str = _LW_MAP.get(lw, f"{lw}mm")
            
            # Map lijntype
            lt = obj.get("lt_b") or "CONTINUOUS"
            
            try:
                layer = Layer(layer_name)
                layer.color_index = color_index
                layer.lineweight = lw_str
                layer.linetype = lt if lt != "" else "CONTINUOUS"
                # Note: add_layer may raise if layer already exists
                Console.add_layer(layer)
                layers_created += 1
            except Exception:
                # Layer might already exist or invalid params — skip
                continue

    return layers_created


def load_nlcs_hatches() -> int:
    """Copy NLCS .pat hatch files to BricsCAD support directory.
    
    Returns:
        Number of hatch patterns installed
    """
    try:
        import brachyura
        from brachyura.console import Console
    except ImportError:
        raise ImportError("NLCS Opentool werkt alleen binnen BricsCAD")

    pat_src_dir = os.path.join(_NLCS_DATA_DIR, "arceringen")
    if not os.path.exists(pat_src_dir):
        return 0

    # Get BricsCAD support path for hatches
    support_dir = os.environ.get("BRYSUPPORT", "")
    if not support_dir:
        # Try to find it via brachyura
        try:
            from brachyura import application
            support_dir = application.get_support_dir()
        except Exception:
            # Fallback: use user's BricsCAD support dir
            home = os.path.expanduser("~")
            support_dir = os.path.join(home, "BricsCAD", "BricsCAD_v24", "Support")

    hatch_dir = os.path.join(support_dir, "hatch")
    os.makedirs(hatch_dir, exist_ok=True)

    count = 0
    for pat_file in os.listdir(pat_src_dir):
        if pat_file.endswith(".pat"):
            src = os.path.join(pat_src_dir, pat_file)
            dst = os.path.join(hatch_dir, pat_file)
            with open(src, "r") as fsrc:
                content = fsrc.read()
            with open(dst, "w") as fdst:
                fdst.write(content)
            count += 1

    return count


def load_nlcs_linetypes() -> int:
    """Load NLCS linetypes into BricsCAD.
    
    Copies NLCS.lin and NLCS.SHX to BricsCAD support directory.
    
    Returns:
        Number of linetypes available
    """
    try:
        import brachyura
    except ImportError:
        raise ImportError("NLCS Opentool werkt alleen binnen BricsCAD")

    lin_src = os.path.join(_NLCS_DATA_DIR, "lijntypes", "autocad", "NLCS-5.0.lin")
    if not os.path.exists(lin_src):
        return 0

    try:
        from brachyura import application
        support_dir = application.get_support_dir()
    except Exception:
        home = os.path.expanduser("~")
        support_dir = os.path.join(home, "BricsCAD", "BricsCAD_v24", "Support")

    # Copy lin file
    import shutil
    lin_dst = os.path.join(support_dir, "NLCS-5.0.lin")
    shutil.copy(lin_src, lin_dst)

    # Also copy the SHX font file (needed for complex linetypes)
    shx_src = os.path.join(_NLCS_DATA_DIR, "lijntypes", "autocad", "NLCS.shx")
    if os.path.exists(shx_src):
        shx_dst = os.path.join(support_dir, "NLCS.shx")
        shutil.copy(shx_src, shx_dst)

    # Count linetypes in the lin file
    count = 0
    with open(lin_src, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("*") and "," in line:
                count += 1

    return count


def load_nlcs_plotstyles() -> int:
    """Install NLCS plot styles (CTB files).
    
    Returns:
        Number of CTB files installed
    """
    plot_src_dir = os.path.join(_NLCS_DATA_DIR, "plotinstellingen")
    if not os.path.exists(plot_src_dir):
        return 0

    try:
        from brachyura import application
        support_dir = application.get_support_dir()
    except Exception:
        home = os.path.expanduser("~")
        support_dir = os.path.join(home, "BricsCAD", "BricsCAD_v24", "Support")

    plotstyle_dir = os.path.join(support_dir, "plotstyles")
    os.makedirs(plotstyle_dir, exist_ok=True)

    import shutil
    count = 0
    for ctb in ["NLCS color.ctb", "NLCS non-color.ctb", "NLCS non-color en color gecombineerd.ctb"]:
        src = os.path.join(plot_src_dir, ctb)
        if os.path.exists(src):
            dst = os.path.join(plotstyle_dir, ctb)
            shutil.copy(src, dst)
            count += 1

    return count


def get_all_disciplines() -> list[str]:
    """Return list of all available NLCS hoofdgroep codes."""
    if not os.path.exists(_TABLE_DIR):
        return []
    
    disciplines = []
    for fname in os.listdir(_TABLE_DIR):
        if fname.startswith("5.02-Objectentabel-") and fname.endswith(".csv"):
            # Extract code between last dash and .csv
            code = fname.replace("5.02-Objectentabel-", "").replace(".csv", "")
            disciplines.append(code)
    return sorted(disciplines)


# Standalone test/debug functions
def debug_dump_disciplines():
    """Print all available disciplines."""
    for disc in get_all_disciplines():
        print(f"  {disc}")


def debug_dump_layers(discipline: str, limit: int = 10):
    """Print first N layers for a discipline."""
    csv_path = os.path.join(_TABLE_DIR, f"5.02-Objectentabel-{discipline}.csv")
    objects = parse_objecttabel(csv_path)
    print(f"Beschikbare objecten in {discipline} ({len(objects)} totaal):")
    for obj in objects[:limit]:
        print(f"  {obj['hoofdgroep']}-{obj['omschrijving']} | kleur={obj.get('kl_b')} | lw={obj.get('lw_b')} | lt={obj.get('lt_b')}")
    if len(objects) > limit:
        print(f"  ... en nog {len(objects) - limit} meer")


if __name__ == "__main__":
    # Standalone test
    print("NLCS Loader - Standalone Debug Mode")
    print("=" * 40)
    print("\nBeschikbare disciplines:")
    debug_dump_disciplines()
    print()
    for disc in ["VH", "RI", "KL", "GR"]:
        csv_path = os.path.join(_TABLE_DIR, f"5.02-Objectentabel-{disc}.csv")
        if os.path.exists(csv_path):
            print(f"\n{disc}:")
            debug_dump_layers(disc, 5)

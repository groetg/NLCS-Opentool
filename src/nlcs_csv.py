"""
NLCS CSV Parser - Laat LISP de lagen lezen uit NLCS CSV bestanden.

Gebruik vanuit LISP:
(load "C:/Users/micro/NLCS-Opentool/src/nlcs_csv.py")
(nlcs-get-layers "VH")

Of als standalone:
python nlcs_csv.py --discipline VH
"""

import csv
import os
import sys
import argparse


def parse_nlcs_csv(discipline_code: str, nlcs_base: str = None) -> list:
    """
    Parse een NLCS objectentabel CSV en retourneer lijst van (id, omschrijving) tuples.
    """
    if nlcs_base is None:
        # Default: assume this script is in NLCS-Opentool/src/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        nlcs_base = os.path.join(os.path.dirname(script_dir), "data", "nlcs")
    
    csv_path = os.path.join(
        nlcs_base,
        "tabellen", "publicatie", "objectentabellen-verkort",
        f"5.02-Objectentabel-{discipline_code}.csv"
    )
    
    if not os.path.exists(csv_path):
        return []
    
    objects = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            # NLCS CSV format: quoted fields with comma separator
            reader = csv.reader(f, quotechar='"')
            next(reader)  # skip header row
            
            for row in reader:
                if len(row) < 3:
                    continue
                try:
                    hoofdgroep = row[0].strip()
                    obj_id = row[1].strip()
                    omschrijving = row[2].strip()
                    
                    # Get layer properties
                    # Format: kl_b=color, lw_b=lineweight, lt_b=linetype
                    color_idx = row[9].strip() if len(row) > 9 else "7"
                    lineweight = row[8].strip() if len(row) > 8 else "0.25"
                    linetype = row[12].strip() if len(row) > 12 else "CONTINUOUS"
                    
                    objects.append({
                        "id": obj_id,
                        "omschrijving": omschrijving,
                        "hoofdgroep": hoofdgroep,
                        "color": int(color_idx) if color_idx.isdigit() else 7,
                        "lineweight": float(lineweight) if lineweight.replace(".", "1").isdigit() else 0.25,
                        "linetype": linetype,
                    })
                except (IndexError, ValueError):
                    continue
    except Exception as e:
        print(f"Error parsing {csv_path}: {e}", file=sys.stderr)
    
    return objects


def format_for_lisp(objects: list) -> str:
    """
    Format objects as LISP association list string for (get_tile "layer_list").
    Each name separated by newline.
    """
    if not objects:
        return "GEEN_LAGEN_GEVONDEN"
    
    names = [f"{o['hoofdgroep']}-{o['omschrijving']}" for o in objects]
    return "\n".join(names)


def format_as_lisp_data(objects: list) -> str:
    """
    Format objects as proper LISP data: ((id "omschrijving" kleur lw linetype) ...)
    """
    if not objects:
        return "nil"
    
    lines = []
    for o in objects:
        line = f'(\"{o["id"]}\" \"{o["omschrijving"]}\" {o["color"]} {o["lineweight"]} \"{o["linetype"]}\")'
        lines.append(line)
    
    return "(list " + " ".join(lines) + ")"


def print_lisp_list(objects: list):
    """Print layer names as newline-separated list for DCL list_box."""
    if not objects:
        print("GEEN_LAGEN_GEVONDEN")
        return
    
    for o in objects:
        name = f"{o['hoofdgroep']}-{o['omschrijving']}"
        print(name)


def main():
    parser = argparse.ArgumentParser(description="NLCS CSV Parser")
    parser.add_argument("--discipline", "-d", required=True, help="NLCS hoofdgroep code (VH, RI, KL, etc.)")
    parser.add_argument("--format", "-f", choices=["list", "lisp", "count"], default="list",
                        help="Output format: list (newline sep), lisp (LISP data), count")
    parser.add_argument("--nlcs-path", help="Path to NLCS data directory")
    
    args = parser.parse_args()
    
    objects = parse_nlcs_csv(args.discipline, args.nlcs_path)
    
    if args.format == "list":
        print_lisp_list(objects)
    elif args.format == "lisp":
        print(format_as_lisp_data(objects))
    elif args.format == "count":
        print(len(objects))


if __name__ == "__main__":
    main()

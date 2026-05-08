"""
NLCS LISP Data Generator

Genereert een LISP bestand met alle NLCS lagen data.
Dit wordt geladen voor de plugin, zodat LISP de data niet dynamisch hoeft te lezen.

Usage:
    python nlcs_generate_lisp.py

Output:
    src/nlcs_layers.lsp - Alle NLCS lagen als LISP data
"""

import csv
import os
import sys


def parse_nlcs_csv(csv_path: str) -> list:
    """Parse een NLCS verkort CSV bestand en retourneer object lijst."""
    objects = []
    if not os.path.exists(csv_path):
        return objects
    
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
        for line in lines[1:]:  # skip header
            line = line.strip()
            if not line:
                continue
            # Replace field separator pattern: ,"" with |||
            modified = line.replace(',""', '|||')
            parts = modified.split('|||')
            
            fields = []
            for p in parts:
                p = p.strip()
                # Strip outer quotes (multiple pairs)
                while p.startswith('"') and p.endswith('"') and len(p) > 1:
                    p = p[1:-1]
                # Strip remaining outer quotes
                while p.startswith('"'):
                    p = p[1:]
                while p.endswith('"'):
                    p = p[:-1]
                # Unescape ""
                p = p.replace('""', '"')
                fields.append(p)
            
            if len(fields) < 35:
                continue
            try:
                kl_b = fields[9].strip() if fields[9].strip() else "7"
                lw_b = fields[8].strip() if fields[8].strip() else "0.25"
                lt_b = fields[12].strip() if fields[12].strip() else "CONTINUOUS"
                obj = {
                    "hoofdgroep": fields[0],
                    "id": fields[1].strip(),
                    "omschrijving": fields[2],
                    "kl_b": int(kl_b) if kl_b.isdigit() else 7,
                    "lw_b": float(lw_b.replace(",", ".")) if lw_b.replace(",", "1").replace(".", "1").isdigit() else 0.25,
                    "lt_b": lt_b if lt_b else "CONTINUOUS",
                }
                objects.append(obj)
            except (IndexError, ValueError):
                continue
    return objects


def generate_lisp(nlcs_base: str, output_path: str):
    """Genereer LISP bestand met alle NLCS lagen."""
    
    disciplines = [
        ("AL", "Algemeen", "AL-Algemeen"),
        ("AM", "Assen en metrering", "AM-assenenmetrering"),
        ("BC", "Betonconstructies", "BC-betonconstructies"),
        ("BV", "Bermbeveiliging", "BV-bermbeveiliging"),
        ("FC", "Funderingsconstructies", "FC-funderingsconstructies"),
        ("FV", "Faunavoorzieningen", "FV-faunavoorzieningen"),
        ("GC", "Grondkerende constructies", "GC-GrondkerendeConstructies-verkort"),
        ("GK", "Grondkeringen", "GK-Grondkeringen"),
        ("GR", "Groen", "GR-Groen"),
        ("GW", "Grondwerken", "GW-grondwerken"),
        ("HU", "Hulpconstructies", "HU-Hulpconstructies"),
        ("IE", "Inrichtingselementen", "IE-Inrichtingselementen"),
        ("IV", "Installaties Vaarweg", "IV-InstallatiesVaarweg"),
        ("IW", "Installaties Wegen", "IW-installatieswegen"),
        ("KC", "Kunststofconstructies", "KC-kunststofconstructies"),
        ("KG", "Kadastrale grenzen", "KG-kadastralegrenzen"),
        ("KL", "Kabels en leidingen", "KL-kabelsenleidingen"),
        ("KW", "Kunstwerken", "KW-kunstwerken"),
        ("MC", "Mechanische constructies", "MC-mechanischeconstructies"),
        ("MO", "Milieuonderzoek", "MO-milieuenonderzoek"),
        ("MW", "Metselwerk", "MW-metselwerk"),
        ("OB", "Oever- en bodembescherming", "OB-oeverenbodembescherming"),
        ("OG", "Ondergrond", "OG-ondergrond"),
        ("OV", "Openbare verlichting", "OV-openbareverlichting"),
        ("RI", "Riolering", "RI-riolering"),
        ("SC", "Staalconstructies", "SC-staalconstructies"),
        ("VH", "Verhardingen", "VH-verhardingen"),
        ("VV", "Verkeersmaatregelen Vaarweg", "VV-verkeersmaatregelenvaarweg"),
        ("VW", "Verkeersmaatregelen Weg", "VW-VerkeersmaatregelenWeg"),
        ("WH", "Waterhuishouding", "WH-Waterhuishouding"),
        ("ZZ", "Diversen", "ZZ-voorallehoofdgroepen"),
    ]
    
    table_dir = os.path.join(nlcs_base, "tabellen", "publicatie", "objectentabellen-verkort")
    
    lines = []
    lines.append("; NLCS Opentool - Auto-generated layer data")
    lines.append("; Do NOT edit manually - regenerate with nlcs_generate_lisp.py")
    lines.append("")
    lines.append("(defvar *nlcs-layers* (list))")
    lines.append("(defvar *nlcs-disciplines* (list))")
    lines.append("")
    
    # Generate discipline list
    lines.append("; Discipline definitions")
    lines.append("(setq *nlcs-disciplines* (list")
    for code, name, _ in disciplines:
        lines.append(f'  (cons "{code}" "{name}")')
    lines.append("))")
    lines.append("")
    
    # Generate layer data per discipline
    lines.append("; Layer data per discipline (id, omschrijving, kleur, lijngewicht, lijntype)")
    
    for code, name, file_suffix in disciplines:
        csv_path = os.path.join(table_dir, f"5.02-Objectentabel-{file_suffix}.csv")
        objects = parse_nlcs_csv(csv_path)
        
        lines.append(f"; {name} ({code}) - {len(objects)} lagen")
        lines.append(f"(setq *nlcs-layers* (cons (list \"{code}\" \"{name}\" (list")
        
        for obj in objects:
            # Format: (id omschrijving kleur lijngewicht lijntype)
            # Layer name format: HOOFGROEP-OMSCHRIJVING (zonder id)
            layer_name = f"{obj['hoofdgroep']}-{obj['omschrijving']}"
            line = f'  (list "{obj["id"]}" "{layer_name}" {obj["kl_b"]} {obj["lw_b"]} "{obj["lt_b"]}")'
            lines.append(line)
        
        lines.append(")) *nlcs-layers*))")
        lines.append("")
    
    # Helper functions
    lines.append("; Helper functions")
    lines.append("(defun nlcs-get-discipline-name (code)")
    lines.append("  (cdr (assoc code *nlcs-disciplines*)))")
    lines.append("")
    
    lines.append("(defun nlcs-get-layers-for-discipline (code)")
    lines.append("  (cdr (assoc code *nlcs-layers*)))")
    lines.append("")
    
    lines.append("(defun nlcs-create-layer (discipline-code layer-name / layer full-name)")
    lines.append("  ; Create a NLCS layer with correct properties")
    lines.append("  (setq full-name (strcat discipline-code \"-\" layer-name))")
    lines.append("  (command \"-LAYER\" \"MAKE\" full-name)")
    lines.append("  full-name")
    lines.append(")")
    lines.append("")
    
    lines.append("(princ \"\\n[NLCS] Layer data geladen. \")")
    total = sum(len(parse_nlcs_csv(os.path.join(table_dir, f"5.02-Objectentabel-{sf}.csv"))) for _, _, sf in disciplines)
    lines.append(f'(princ "{total} lagen beschikbaar voor {len(disciplines)} disciplines.\\n")')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nlcs_base = os.path.join(os.path.dirname(script_dir), "data", "nlcs")
    output_path = os.path.join(script_dir, "nlcs_layers.lsp")
    
    print(f"NLCS data: {nlcs_base}")
    print(f"Output: {output_path}")
    print()
    
    if not os.path.exists(nlcs_base):
        print("FOUT: NLCS data directory niet gevonden!")
        print("Clone eerst de repo met submodules:")
        print("  git clone --recurse-submodules https://github.com/groetg/NLCS-Opentool.git")
        sys.exit(1)
    
    generate_lisp(nlcs_base, output_path)
    print(f"Klaar! {output_path} gegenereerd.")


if __name__ == "__main__":
    main()

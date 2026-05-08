"""
NLCS Opentool UI — BricsCAD dialoog voor NLCS plugin.
"""

__version__ = "0.1.0"


def get_discipline_groups() -> dict[str, list[str]]:
    """Return NLCS disciplines grouped by category."""
    return {
        "Wegen & Verhardingen": ["VH", "VW", "BV", "GW", "GK", "GC"],
        "Riolering & Water": ["RI", "WH", "OB"],
        "Kabels & Leidingen": ["KL"],
        "Groen": ["GR"],
        "Kunstwerken": ["KW", "BC", "FC", "SC", "MC", "KC", "HU"],
        "Installaties": ["OV", "IW", "IV"],
        "Ondergrond": ["OG"],
        "Bebakening": ["KG"],
        "Metselwerk": ["MW"],
        "Fauna": ["FV"],
        "Milieu": ["MO"],
        "Algemeen": ["AL", "AM", "IE", "ZZ"],
    }


def show_nlcs_dialog():
    """Show the main NLCS configuration dialog in BricsCAD."""
    try:
        from brachyura.gui import Dialog, Row, Column, CheckBox, Button, Label, ListBox
        from brachyura.console import Console
        from brachyura import application
    except ImportError:
        print("NLCS Opentool: kan dialoog niet laden (geen BricsCAD omgeving)")
        return

    # Get discipline list
    groups = get_discipline_groups()
    all_disciplines = []
    for grp, discs in groups.items():
        all_disciplines.extend(discs)

    # Create dialog
    dlg = Dialog("NLCS Opentool - Laad NLCS Disciplines")
    dlg.width = 500
    dlg.height = 600

    # Title
    dlg.add(Label("Selecteer NLCS disciplines om te laden:"))
    dlg.add(Label(""))

    # Discipline checkboxes grouped
    checkboxes = {}
    for group_name, disciplines in groups.items():
        dlg.add(Label(f"-- {group_name} --"))
        for disc in disciplines:
            cb = CheckBox(f"{disc}")
            checkboxes[disc] = cb
            dlg.add(cb)

    dlg.add(Label(""))

    # Buttons
    def on_load_all():
        # Select all
        for disc, cb in checkboxes.items():
            cb.checked = True

    def on_load_none():
        # Deselect all
        for disc, cb in checkboxes.items():
            cb.checked = False

    def on_ok():
        selected = [disc for disc, cb in checkboxes.items() if cb.checked]
        if not selected:
            Console.println("NLCS: geen disciplines geselecteerd")
            return
        
        Console.println(f"NLCS: laden van disciplines: {', '.join(selected)}")
        
        # Load layers
        from . import nlcs_loader
        try:
            count = nlcs_loader.load_nlcs_layers(selected)
            Console.println(f"NLCS: {count} lagen aangemaakt")
        except Exception as e:
            Console.println(f"NLCS fout bij laden lagen: {e}")

        # Load resources
        try:
            hatches = nlcs_loader.load_nlcs_hatches()
            linetypes = nlcs_loader.load_nlcs_linetypes()
            plotstyles = nlcs_loader.load_nlcs_plotstyles()
            Console.println(f"NLCS: {hatches} arceringen, {linetypes} lijntypes, {plotstyles} plotstijlen")
        except Exception as e:
            Console.println(f"NLCS fout bij laden resources: {e}")

        dlg.close()

    def on_cancel():
        dlg.close()

    btn_row = Row([
        Button("Alles", on_load_all),
        Button("Niets", on_load_none),
        Button("Annuleer", on_cancel),
        Button("Laad NLCS", on_ok),
    ])
    dlg.add(btn_row)
    dlg.show()


def show_simple_install_dialog():
    """Simple install dialog that just runs the full install."""
    try:
        from brachyura.gui import Dialog, Label, Button
        from brachyura.console import Console
    except ImportError:
        print("NLCS Opentool: kan dialoog niet laden")
        return

    dlg = Dialog("NLCS Opentool - Installatie")
    dlg.add(Label("Welkom bij NLCS Opentool voor BricsCAD"))
    dlg.add(Label(""))

    def on_install():
        dlg.close()
        from . import nlcs_loader
        from brachyura.console import Console
        try:
            h = nlcs_loader.load_nlcs_hatches()
            l = nlcs_loader.load_nlcs_linetypes()
            p = nlcs_loader.load_nlcs_plotstyles()
            Console.println(f"NLCS Opentool geinstalleerd: {h} arceringen, {l} lijntypes, {p} plotstijlen")
            Console.println("Herstart BricsCAD om de resources te laden.")
        except Exception as e:
            Console.println(f"Installatiefout: {e}")

    dlg.add(Button("Installeer NLCS Resources", on_install))
    dlg.show()

"""
NLCS Opentool for BricsCAD
Plugin entry point — load via BricsCAD Manage → Load Application
"""

import os
import sys

# Add src to path for local imports
_plugin_dir = os.path.dirname(os.path.abspath(__file__))
if _plugin_dir not in sys.path:
    sys.path.insert(0, _plugin_dir)

from . import nlcs_loader
from . import nlcs_ui

__version__ = "0.1.0"
__author__ = "Guido Groet"


def init():
    """Initialize the NLCS plugin in BricsCAD."""
    try:
        from .nlcs_ui import show_nlcs_dialog
        show_nlcs_dialog()
    except Exception as e:
        print(f"NLCS Opentool: kon dialoog niet openen ({e})")
        # Fallback: print available functions
        print("NLCS Opentool geladen. Beschikbare functies:")
        print("  nlcs_loader.load_nlcs_layers(disciplines)  — Laad lagen voor NLCS disciplines")
        print("  nlcs_loader.load_nlcs_hatches()             — Laad arceringen")
        print("  nlcs_loader.load_nlcs_linetypes()          — Laad lijntypes")
        print("  nlcs_loader.load_nlcs_plotstyles()         — Installeer plotstijlen")


# Auto-init when loaded in BricsCAD
if __name__ != "__main__":
    try:
        # Detect if running in BricsCAD via Brachyura
        import brachyura
        init()
    except ImportError:
        # Not in BricsCAD — probably running as standalone script
        init()

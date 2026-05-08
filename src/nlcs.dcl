// NLCS Opentool DCL Dialog Definition
// Build with BricsCAD's native DCL (Dialog Control Language)

nlcs_main : dialog {
  label = "NLCS Opentool - Laag Selectie";
  
  : text {
    label = "Selecteer een NLCS discipline en laag om mee te werken";
    alignment = centered;
  }
  
  spacer;
  
  // Two-column layout: disciplines on left, layers on right
  : boxed_column {
    label = "1. Kies Discipline";
    width = 20;
    height = 25;
    
    : list_box {
      key = "discipline_list";
      label = "Disciplines";
      width = 18;
      height = 20;
      value = "0";
    }
  }
  
  : boxed_column {
    label = "2. Kies Laag";
    width = 25;
    height = 25;
    
    : list_box {
      key = "layer_list";
      label = "Lagen";
      width = 23;
      height = 20;
      value = "0";
    }
  }
  
  spacer;
  
  // Layer name input
  : boxed_column {
    label = "3. Laagnaam (handmatig)";
    : edit_box {
      key = "layer_name_edit";
      label = "Laagnaam:";
      width = 30;
      value = "";
    }
  }
  
  spacer;
  
  // Buttons
  : row {
    alignment = centered;
    : button {
      key = "btn_create";
      label = "Maak Laag";
      is_enabled = true;
    }
    : button {
      key = "btn_draw";
      label = "Teken mee";
      is_enabled = false; // enable when layer is set
    }
    : button {
      key = "btn_cancel";
      label = "Sluiten";
      is_cancel = true;
    }
  }
  
  // Status line
  : text {
    key = "status_text";
    label = "Klaar";
    alignment = left;
  }
}

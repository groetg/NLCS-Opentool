// NLCS Opentool - graphical layer selector

nlcs_main : dialog {
  label = "NLCS Opentool - Laag kiezen";
  : row {
    : boxed_column {
      label = "Status";
      width = 18;
      : radio_button { key = "status_existing"; label = "Bestaand"; }
      : radio_button { key = "status_new"; label = "Nieuw"; value = "1"; }
      : radio_button { key = "status_delete"; label = "Verwijderen"; }
      : radio_button { key = "status_temporary"; label = "Tijdelijk"; }
      spacer;
      : text { key = "status_text"; label = "Kies een discipline"; width = 18; }
    }
    : boxed_column {
      label = "1. Discipline";
      width = 28;
      : list_box {
        key = "discipline_list";
        width = 26;
        height = 24;
        fixed_width = true;
        value = "0";
      }
    }
    : boxed_column {
      label = "2. NLCS-laag";
      width = 42;
      : list_box {
        key = "layer_list";
        width = 40;
        height = 24;
        fixed_width = true;
        value = "0";
      }
    }
  }
  spacer;
  : boxed_column {
    label = "Eigenschappen";
    : edit_box { key = "layer_name_edit"; label = "Laagnaam:"; width = 55; }
    : text { key = "layer_properties"; label = "Selecteer een laag voor eigenschappen"; width = 55; }
  }
  spacer;
  : row {
    alignment = centered;
    : button { key = "btn_create"; label = "Laag aanmaken"; is_default = true; }
    : button { key = "btn_draw"; label = "Tekenen"; is_enabled = false; }
    : button { key = "btn_settings"; label = "Instellingen"; }
    : button { key = "btn_cancel"; label = "Sluiten"; is_cancel = true; }
  }
}

nlcs_settings : dialog {
  label = "NLCS Opentool - Instellingen";
  : boxed_column {
    label = "NLCS-versie";
    : popup_list {
      key = "nlcs_version";
      label = "Versie:";
      list = "NLCS 5.02 (NLCS 5)";
      value = "0";
    }
  }
  spacer;
  : boxed_column {
    label = "Voorkeursdiscipline";
    : popup_list {
      key = "default_discipline";
      label = "Discipline:";
      width = 36;
    }
  }
  spacer;
  : text {
    label = "De actuele meegeleverde dataset is NLCS 5.02.";
    width = 50;
  }
  spacer;
  : row {
    alignment = centered;
    : button { key = "settings_save"; label = "Opslaan"; is_default = true; }
    : button { key = "settings_cancel"; label = "Annuleren"; is_cancel = true; }
  }
}

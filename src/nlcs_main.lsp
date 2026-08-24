; NLCS Opentool - Main LISP Entry Point
; Load via APPLOAD or: (load ".../NLCS-Opentool/nlcs_main.lsp")

; Resolve files relative to this file so Windows and Linux use the same code.
(setq *nlcs-home*
  (if (findfile "nlcs_main.lsp")
    (vl-filename-directory (findfile "nlcs_main.lsp"))
    ""
  )
)
(if (/= *nlcs-home* "")
  (progn
    (load (strcat *nlcs-home* "/nlcs_layers.lsp"))
  )
)

(defun C:NLCS ( / )
  ; Show main NLCS dialog
  (setq dcl_id (load_dialog (strcat *nlcs-home* "/nlcs.dcl")))
  (if (< dcl_id 0)
    (progn
      (alert "NLCS: dialoogbestand niet gevonden.")
      (exit)
    )
  )
  (if (not (new_dialog "nlcs_main" dcl_id))
    (progn
      (alert "Kon NLCS dialoog niet laden.")
      (exit)
    )
  )
  
  ; Initialize layer list
  (nlcs_init_layer_list)
  
  ; Setup callbacks
  (set_tile "discipline_list" "0")
  (set_tile "layer_list" "0")
  
  ; Action callbacks
  (action_tile "discipline_list" "(nlcs_on_discipline_changed)")
  (action_tile "layer_list" "(nlcs_on_layer_selected)")
  (action_tile "status_existing" "(nlcs_set_status \"Bestaand\")")
  (action_tile "status_new" "(nlcs_set_status \"Nieuw\")")
  (action_tile "status_delete" "(nlcs_set_status \"Verwijderen\")")
  (action_tile "status_temporary" "(nlcs_set_status \"Tijdelijk\")")
  (action_tile "btn_create" "(nlcs_create_layer)")
  (action_tile "btn_draw" "(nlcs_start_drawing)")
  (action_tile "btn_cancel" "(done_dialog 0)")
  
  ; Show dialog
  (start_dialog)
  (unload_dialog dcl_id)
)

; Initialize discipline list
(defun nlcs_init_layer_list ( / disciplines)
  (setq disciplines 
    (list
      (cons "AL" "Algemeen")
      (cons "AM" "Assen en metrering")
      (cons "BC" "Betonconstructies")
      (cons "BV" "Bermbeveiliging")
      (cons "FC" "Funderingsconstructies")
      (cons "FV" "Faunavoorzieningen")
      (cons "GC" "Grondkerende constructies")
      (cons "GK" "Grondkeringen")
      (cons "GR" "Groen")
      (cons "GW" "Grondwerken")
      (cons "HU" "Hulpconstructies")
      (cons "IE" "Inrichtingselementen")
      (cons "IV" "Installaties Vaarweg")
      (cons "IW" "Installaties Wegen")
      (cons "KC" "Kunststofconstructies")
      (cons "KG" "Kadastrale grenzen")
      (cons "KL" "Kabels en leidingen")
      (cons "KW" "Kunstwerken")
      (cons "MC" "Mechanische constructies")
      (cons "MO" "Milieuonderzoek")
      (cons "MW" "Metselwerk")
      (cons "OB" "Oever- en bodembescherming")
      (cons "OG" "Ondergrond")
      (cons "OV" "Openbare verlichting")
      (cons "RI" "Riolering")
      (cons "SC" "Staalconstructies")
      (cons "VH" "Verhardingen")
      (cons "VV" "Verkeersmaatregelen Vaarweg")
      (cons "VW" "Verkeersmaatregelen Weg")
      (cons "WH" "Waterhuishouding")
      (cons "ZZ" "Diversen")
    )
  )
  
  (setq *nlcs-discipline-codes* (mapcar 'car disciplines))
  (start_list "discipline_list")
  (foreach disc disciplines
    (add_list (cdr disc))
  )
  (end_list)
  (nlcs_on_discipline_changed)
)

; Called when discipline selection changes
(defun nlcs_on_discipline_changed ( / sel_index disc_code data layer)
  (setq sel_index (fix (atof (get_tile "discipline_list"))))
  (setq disc_code (nth sel_index *nlcs-discipline-codes*))
  
  ; Load layers for this discipline from CSV
  (if disc_code
    (progn
      (setq *nlcs-current-code* disc_code)
      (start_list "layer_list")
      (setq data (assoc disc_code *nlcs-layers*))
      (if data
        (foreach layer (nth 2 data) (add_list (nth 1 layer)))
      )
      (end_list)
      (set_tile "layer_list" "0")
      (nlcs_on_layer_selected)
    )
  )
)

; Get layer names from the generated NLCS data.
(defun nlcs_get_generated_layers_for_disc (disc_code / data layers result)
  (setq data (assoc disc_code *nlcs-layers*))
  (if data
    (progn
      (setq layers (nth 2 data))
      (setq result "")
      (foreach layer layers
        (setq result (strcat result (nth 1 layer) "\n"))
      )
      result
    )
    "GEEN_LAGEN_BESCHIKBAAR"
  )
)

(defun nlcs_set_status (status)
  (set_tile "status_text" status)
)

(defun nlcs_on_layer_selected ( / index data layer)
  (setq index (fix (atof (get_tile "layer_list"))))
  (setq data (assoc *nlcs-current-code* *nlcs-layers*))
  (if (and data (>= index 0) (< index (length (nth 2 data))))
    (progn
      (setq layer (nth index (nth 2 data)))
      (set_tile "layer_name_edit" (nth 1 layer))
      (set_tile "layer_properties"
        (strcat "Kleur: " (itoa (nth 2 layer))
                "  Lijngewicht: " (rtos (nth 3 layer) 2 2)
                "  Lijntype: " (nth 4 layer)))
    )
  )
)

; Legacy example mapping retained for compatibility with older drawings.
(defun nlcs_get_layers_for_disc (disc_code / mapping)
  (setq mapping (list
    (cons "VH" (list 
      "GESLOTENVERHARDING_ASFALT"
      "GESLOTENVERHARDING_BETON"
      "GESLOTENVERHARDING_KANTWERK"
      "OPENVERHARDING_BASALT"
      "OPENVERHARDING_GRASBETER"
      "OPENVERHARDING_MATERIAAL"
    ))
    (cons "RI" (list
      "BUIS_RDM_HENK"
      "BUIS_RDM_VTL"
      "OVERIG_LOZEPUT"
      "OVERIG_STROMINGSRICHTING"
      "OVERIG_UITLAATCONSTRUCTIE"
      "OVERIG_TANK"
    ))
    (cons "KL" (list
      "KABEL_ELEKTRISCH"
      "KABEL_DATACOMMUNICATIE"
      "KABEL_GAS"
      "KABEL_WATER"
      "LEIDING_GAS"
      "LEIDING_WATER"
    ))
    (cons "GR" (list
      "BEGROEIING_BOOM"
      "BEGROEIING_HEESTER"
      "BEGROEIING_GRAS"
      "BEGROEIING_AMOFIEL"
    ))
    (cons "WH" (list
      "WATER_KANAAL"
      "WATER_VIJVER"
      "WATER_BEEK"
      "WATER_BERMGREPPEL"
    ))
    (cons "OV" (list
      "LAMP_KAP"
      "PAAL_OPENBAARVERLICHTING"
      "FOOTING_FOUND"
      "CABLE_LEIDING"
    ))
    (cons "KW" (list
      "BACHB_BETONBRUG"
      "BACHB_STAALBRUG"
      "VIADUCT_BETON"
      "VIADUCT_STAAL"
    ))
  ))
  
  (setq layers (cdr (assoc disc_code mapping)))
  (if layers
    (strcat (nth 0 layers) "\n" 
            (nth 1 layers) "\n"
            (nth 2 layers) "\n"
            (if (nth 3 layers) (strcat (nth 3 layers) "\n" ) "")
            (if (nth 4 layers) (strcat (nth 4 layers) "\n" ) "")
            (if (nth 5 layers) (strcat (nth 5 layers) "\n" ) "")
    )
    (progn
      (princ (strcat "\n[NLCS] Discipline " disc_code " heeft geen voorgedefinieerde voorbeeldlagen\n"))
      "GEEN_LAGEN_BESCHIKBAAR"
    )
  )
)

; Create the selected layer in BricsCAD
(defun nlcs_create_layer ( / sel_index disc_code layer_name)
  (princ "\n[NLCS] Laag aanmaken...")
  
  ; Get selected discipline
  (setq sel_index (fix (atof (get_tile "discipline_list"))))
  
  ; Get layer name from layer list
  (setq layer_name (get_tile "layer_name_edit"))
  
  (if (= layer_name "")
    (progn
      (alert "Geef een laagnaam op of selecteer een laag uit de lijst.")
    )
    (progn
      ; Create layer with NLCS naming convention
      (command ".-LAYER" "MAKE" layer_name "COLOR" "7" "")
      (princ (strcat "\n[NLCS] Laag aangemaakt: " layer_name "\n"))
    )
  )
)

; Start drawing with selected layer
(defun nlcs_start_drawing ( / layer_name)
  (princ "\n[NLCS] Start tekenen...")
)

(princ "\nNLCS Opentool geladen. Type NLCS om te starten.\n")

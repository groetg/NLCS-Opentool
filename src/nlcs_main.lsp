; NLCS Opentool - Main LISP Entry Point
; Load via: (load "C:/Users/micro/NLCS-Opentool/src/nlcs_main.lsp")

(defun C:NLCS ( / )
  ; Show main NLCS dialog
  (load_dialog "C:/Users/micro/NLCS-Opentool/src/nlcs.dcl")
  (if (not (new_dialog "nlcs_main" dcl_id))
    (progn
      (alert "Kon NLCS dialoog niet laden.")
      (exit)
    )
  )
  
  ; Initialize layer list
  (nlcs_init_layer_list)
  
  ; Setup callbacks
  (set_tile "discipline_list" "")
  (set_tile "layer_list" "")
  
  ; Action callbacks
  (action_tile "discipline_list" "(nlcs_on_discipline_changed)")
  (action_tile "layer_list" "(nlcs_on_layer_selected)")
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
  
  ; Build list string for DCL list_box
  (setq disc_list_str "")
  (foreach disc disciplines
    (setq disc_list_str (strcat disc_list_str (cdr disc) "\n"))
  )
  (setq disc_list_str (substr disc_list_str 1 (- (strlen disc_list_str) 1))) ; remove last newline
  
  (set_tile "discipline_list" disc_list_str)
)

; Called when discipline selection changes
(defun nlcs_on_discipline_changed ( / sel_index layers_csv csv_data lines layer_list_str)
  (setq sel_index (fix (atof (get_tile "discipline_list"))))
  
  ; Get discipline code
  (cond
    ((= sel_index 0) (setq disc_code "AL"))
    ((= sel_index 1) (setq disc_code "AM"))
    ((= sel_index 2) (setq disc_code "BC"))
    ((= sel_index 3) (setq disc_code "BV"))
    ((= sel_index 4) (setq disc_code "FC"))
    ((= sel_index 5) (setq disc_code "FV"))
    ((= sel_index 6) (setq disc_code "GC"))
    ((= sel_index 7) (setq disc_code "GK"))
    ((= sel_index 8) (setq disc_code "GR"))
    ((= sel_index 9) (setq disc_code "GW"))
    ((= sel_index 10) (setq disc_code "HU"))
    ((= sel_index 11) (setq disc_code "IE"))
    ((= sel_index 12) (setq disc_code "IV"))
    ((= sel_index 13) (setq disc_code "IW"))
    ((= sel_index 14) (setq disc_code "KC"))
    ((= sel_index 15) (setq disc_code "KG"))
    ((= sel_index 16) (setq disc_code "KL"))
    ((= sel_index 17) (setq disc_code "KW"))
    ((= sel_index 18) (setq disc_code "MC"))
    ((= sel_index 19) (setq disc_code "MO"))
    ((= sel_index 20) (setq disc_code "MW"))
    ((= sel_index 21) (setq disc_code "OB"))
    ((= sel_index 22) (setq disc_code "OG"))
    ((= sel_index 23) (setq disc_code "OV"))
    ((= sel_index 24) (setq disc_code "RI"))
    ((= sel_index 25) (setq disc_code "SC"))
    ((= sel_index 26) (setq disc_code "VH"))
    ((= sel_index 27) (setq disc_code "VV"))
    ((= sel_index 28) (setq disc_code "VW"))
    ((= sel_index 29) (setq disc_code "WH"))
    ((= sel_index 30) (setq disc_code "ZZ"))
    (t (setq disc_code ""))
  )
  
  ; Load layers for this discipline from CSV
  (if (/= disc_code "")
    (progn
      (setq csv_path (strcat "C:/Users/micro/NLCS-Opentool/data/nlcs/tabellen/publicatie/objectentabellen-verkort/5.02-Objectentabel-" disc_code ".csv"))
      (if (findfile csv_path)
        (progn
          ; Read and parse CSV - for now, show discipline name as proxy
          ; Full CSV parsing done via Python
          (princ (strcat "\n[NLCS] Laden: " disc_code "\n"))
          
          ; For demo: show a few example layer names
          (set_tile "layer_list" 
            (strcat 
              (nlcs_get_layers_for_disc disc_code)
            )
          )
        )
        (progn
          (set_tile "layer_list" "Geen data beschikbaar\n Controleer NLCS installatie")
        )
      )
    )
  )
)

; Get layer names for a discipline (placeholder - will be replaced by Python CSV reader)
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

; Called when layer is selected in list
(defun nlcs_on_layer_selected ( / sel_index layer_name)
  (setq sel_index (fix (atof (get_tile "layer_list"))))
  (if (> sel_index -1)
    (progn
      (princ (strcat "\n[NLCS] Geselecteerd: " (itoa sel_index) "\n"))
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

; NLCS Opentool - Main LISP Entry Point
; Load via APPLOAD or: (load ".../NLCS-Opentool/nlcs_main.lsp")

; Resolve files relative to the loaded file, also when APPLOAD used an
; absolute path that is not part of BricsCAD's support path.
(defun nlcs_find_home ( / loaded file home )
  (setq loaded (vl-list-loaded-lisp))
  (foreach file loaded
    (if (= (strcase (vl-filename-base file)) "NLCS_MAIN")
      (setq home (vl-filename-directory file))
    )
  )
  (if home home "")
)
(setq *nlcs-home* (nlcs_find_home))
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
  (action_tile "status_revision" "(nlcs_set_status \"Revisie\")")
  (action_tile "btn_create" "(nlcs_create_layer)")
  (action_tile "btn_draw" "(nlcs_start_drawing)")
  (action_tile "btn_settings" "(done_dialog 2)")
  (action_tile "btn_cancel" "(done_dialog 0)")
  
  ; Show dialog
  (setq dialog_result (start_dialog))
  (unload_dialog dcl_id)
  (if (= dialog_result 2)
    (progn
      (nlcs_show_settings)
      (C:NLCS)
    )
  )
)

(defun nlcs_show_settings ( / settings_id disciplines codes selected version_result )
  (setq settings_id (load_dialog (strcat *nlcs-home* "/nlcs.dcl")))
  (if (and settings_id (>= settings_id 0) (new_dialog "nlcs_settings" settings_id))
    (progn
      (setq disciplines
        (list
          (cons "AL" "Algemeen") (cons "AM" "Assen en metrering")
          (cons "BC" "Betonconstructies") (cons "BV" "Bermbeveiliging")
          (cons "FC" "Funderingsconstructies") (cons "FV" "Faunavoorzieningen")
          (cons "GC" "Grondkerende constructies") (cons "GK" "Grondkeringen")
          (cons "GR" "Groen") (cons "GW" "Grondwerken")
          (cons "HU" "Hulpconstructies") (cons "IE" "Inrichtingselementen")
          (cons "IV" "Installaties Vaarweg") (cons "IW" "Installaties Wegen")
          (cons "KC" "Kunststofconstructies") (cons "KG" "Kadastrale grenzen")
          (cons "KL" "Kabels en leidingen") (cons "KW" "Kunstwerken")
          (cons "MC" "Mechanische constructies") (cons "MO" "Milieuonderzoek")
          (cons "MW" "Metselwerk") (cons "OB" "Oever- en bodembescherming")
          (cons "OG" "Ondergrond") (cons "OV" "Openbare verlichting")
          (cons "RI" "Riolering") (cons "SC" "Staalconstructies")
          (cons "VH" "Verhardingen") (cons "VV" "Verkeersmaatregelen Vaarweg")
          (cons "VW" "Verkeersmaatregelen Weg") (cons "WH" "Waterhuishouding")
          (cons "ZZ" "Diversen")
        )
      )
      (setq codes (mapcar 'car disciplines))
      (start_list "default_discipline")
      (foreach discipline disciplines (add_list (cdr discipline)))
      (end_list)
      (set_tile "default_discipline" "0")
      (action_tile "settings_save"
        "(setq *nlcs-version* \"5.02\") (setq *nlcs-default-code* (nth (fix (atof (get_tile \"default_discipline\"))) codes)) (done_dialog 1)")
      (action_tile "settings_cancel" "(done_dialog 0)")
      (setq version_result (start_dialog))
      (unload_dialog settings_id)
    )
    (alert "NLCS: instellingenvenster kon niet worden geladen.")
  )
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
  (setq *nlcs-parent-stack* (list))
  (nlcs_on_discipline_changed)
)

; Called when discipline selection changes
(defun nlcs_on_discipline_changed ( / sel_index disc_code)
  (setq sel_index (fix (atof (get_tile "discipline_list"))))
  (setq disc_code (nth sel_index *nlcs-discipline-codes*))
  (if disc_code
    (progn
      (setq *nlcs-current-code* disc_code)
      (setq *nlcs-parent-stack* (list))
      (setq *nlcs-current-parent* "")
      (nlcs_show_children "")
    )
  )
)

(defun nlcs_show_children (parent / data layer children has_children label candidate)
  (setq data (assoc *nlcs-current-code* *nlcs-layers*))
  (setq children (list))
  (if data
    (foreach layer (nth 2 data)
      (if (= (nth 5 layer) parent)
        (setq children (append children (list layer)))
      )
    )
  )
  (setq *nlcs-current-items* children)
  (start_list "layer_list")
  (if (> (length *nlcs-parent-stack*) 0) (add_list "<-- Terug"))
  (foreach layer children
    (setq has_children nil)
    (foreach candidate (nth 2 data)
      (if (= (nth 5 candidate) (nth 0 layer)) (setq has_children T))
    )
    (setq label (if has_children "+ " "  "))
    (add_list (strcat label (nth 1 layer)))
  )
  (end_list)
  (set_tile "layer_list" "0")
  (if (> (length children) 0) (nlcs_on_layer_selected))
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
  (setq *nlcs-status-prefix*
    (cond
      ((= status "Bestaand") "B-")
      ((= status "Nieuw") "N-")
      ((= status "Verwijderen") "V-")
      ((= status "Tijdelijk") "T-")
      ((= status "Revisie") "R-")
      (T "N-")
    )
  )
  (set_tile "status_text" status)
  (if *nlcs-current-layer* (nlcs_set_layer_fields *nlcs-current-layer*))
)

(defun nlcs_on_layer_selected ( / index data layer)
  (setq index (fix (atof (get_tile "layer_list"))))
  (if (and (> (length *nlcs-parent-stack*) 0) (= index 0))
    (progn
      (setq *nlcs-current-parent* (car *nlcs-parent-stack*))
      (setq *nlcs-parent-stack* (cdr *nlcs-parent-stack*))
      (nlcs_show_children *nlcs-current-parent*)
    )
    (progn
      (if (> (length *nlcs-parent-stack*) 0) (setq index (1- index)))
      (setq layer (nth index *nlcs-current-items*))
      (if layer
        (progn
          (if (nlcs_has_children (nth 0 layer))
            (progn
              (setq *nlcs-parent-stack* (cons (if *nlcs-current-parent* *nlcs-current-parent* "") *nlcs-parent-stack*))
              (setq *nlcs-current-parent* (nth 0 layer))
              (nlcs_show_children *nlcs-current-parent*)
            )
            (nlcs_set_layer_fields layer)
          )
        )
      )
    )
  )
)

(defun nlcs_has_children (id / data result candidate)
  (setq result nil)
  (setq data (assoc *nlcs-current-code* *nlcs-layers*))
  (if data
    (foreach candidate (nth 2 data)
      (if (= (nth 5 candidate) id) (setq result T))
    )
  )
  result
)

(defun nlcs_set_layer_fields (layer)
  (setq *nlcs-current-layer* layer)
  (set_tile "layer_name_edit" (nlcs_status_name (nth 1 layer)))
  (set_tile "layer_color_edit" (itoa (nth 2 layer)))
  (set_tile "layer_weight_edit" (rtos (nth 3 layer) 2 2))
  (set_tile "layer_type_edit" (nth 4 layer))
)

(defun nlcs_status_name (name)
  (strcat (if *nlcs-status-prefix* *nlcs-status-prefix* "N-") name)
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
(defun nlcs_create_layer ( / layer_name color weight linetype)
  (princ "\n[NLCS] Laag aanmaken...")
  (setq layer_name (get_tile "layer_name_edit"))
  (setq color (get_tile "layer_color_edit"))
  (setq weight (get_tile "layer_weight_edit"))
  (setq linetype (get_tile "layer_type_edit"))
  
  (if (= layer_name "")
    (progn
      (alert "Geef een laagnaam op of selecteer een laag uit de lijst.")
    )
    (progn
      ; Create the layer with editable NLCS properties and make it current.
      (command "_.-LAYER" "_M" layer_name "_C" color layer_name
               "_LW" weight layer_name "_LT" linetype layer_name "")
      (setvar "CLAYER" layer_name)
      (princ (strcat "\n[NLCS] Laag aangemaakt: " layer_name "\n"))
      (done_dialog 1)
    )
  )
)

; Start drawing with selected layer
(defun nlcs_start_drawing ( / layer_name)
  (princ "\n[NLCS] Start tekenen...")
)

(princ "\nNLCS Opentool geladen. Type NLCS om te starten.\n")

;;; ==========================================
;;; AXS AutoDraw Engine (AutoLISP)
;;; Design Style: 程序员专享 极简微水泥风格
;;; Core Materials: 极简风格，需要大量收纳空间，有两只猫
;;; Lighting: 无主灯暗槽, 3000K暖光
;;; Generated: 2026-05-31
;;; ==========================================

(defun c:AXSDRAW ()
  (setvar "CMDECHO" 0)
  (setvar "OSMODE" 0)
  
  ;; 1. Create layers
  (command "_layer" "m" "AXS_WALL" "c" "2" "" "")
  (command "_layer" "m" "AXS_WINDOW" "c" "4" "" "")
  (command "_layer" "m" "AXS_DOOR" "c" "1" "" "")
  (command "_layer" "m" "AXS_INFO" "c" "7" "" "")
  
  ;; 2. Draw walls
  (command "_layer" "s" "AXS_WALL" "")
  (command "_rectang" "0,0" "6707,5366")
  (command "_rectang" "240,240" "6467,5126")
  
  ;; 3. Draw window
  (command "_layer" "s" "AXS_WINDOW" "")
  (command "_line" "2353,5126" "2353,5366" "")
  (command "_line" "4353,5126" "4353,5366" "")
  (command "_line" "2353,5206" "4353,5206" "")
  (command "_line" "2353,5286" "4353,5286" "")
  
  ;; 4. Draw door
  (command "_layer" "s" "AXS_DOOR" "")
  (command "_line" "740,0" "740,240" "")
  (command "_line" "1640,0" "1640,240" "")
  (command "_line" "740,240" "740,1140" "")
  (command "_arc" 
           (list 1640 240) 
           "_c" 
           (list 740 240) 
           (list 740 1140)
  )
  
  ;; 5. Label
  (command "_layer" "s" "AXS_INFO" "")
  (command "_text" 
           (list 3353 2683) 
           "300" "0" 
           "AXS ROOM: 程序员专享 极简微水泥风格"
  )
  (command "_text" 
           (list 3353 2283) 
           "200" "0" 
           "Material: 极简风格，需要大量收纳空间，有两只猫"
  )
  
  (setvar "OSMODE" 16383)
  (princ "\n[AXS] Drawing completed successfully!")
  (princ "\nType AXSDRAW to redraw.")
  (princ)
)

(princ "\n[AXS] Type AXSDRAW to run.\n")
(princ)

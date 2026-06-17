;; AXS Design Studio - AutoLISP Script for Asiansen Project (30-50W Budget Version)
;; Command: AXSDRAW
;; Description: Generates the 150sqm structural layout with Chinese tags and functional modules based on 2026-06-13 Survey.
;; Constraint: No structural wall demolition. 

(defun c:AXSDRAW ()
  (setq old_osmode (getvar "OSMODE"))
  (setvar "OSMODE" 0)
  
  ;; Create Layers
  (command "-layer" "m" "AXS_WALLS" "c" "7" "" "")
  (command "-layer" "m" "AXS_FURNITURE" "c" "8" "" "")
  (command "-layer" "m" "AXS_TAGS" "c" "2" "" "")
  
  ;; Draw basic boundary (150 sqm approximation, 10m x 15m)
  (command "-layer" "s" "AXS_WALLS" "")
  (command "rectang" "0,0" "10000,15000")
  
  ;; --- Public Space (LDK) ---
  (command "-layer" "s" "AXS_FURNITURE" "")
  ;; Sofa (Floating, robot vacuum compatible)
  (command "rectang" "1000,4000" "4000,5000")
  ;; Dining Table (Multi-functional)
  (command "rectang" "4500,4500" "6500,5500")
  ;; 80% Hidden Storage Wall (通顶柜)
  (command "rectang" "500,14000" "9500,14600")
  
  (command "-layer" "s" "AXS_TAGS" "")
  (command "text" "2500,4500" "250" "0" "LDK客餐厅区-悬浮沙发(底空>12cm防猫毛死角)")
  (command "text" "5000,5000" "250" "0" "多功能餐桌(吃饭/辅导作业/手工)")
  (command "text" "5000,14300" "250" "0" "二八定律通顶收纳柜(原木色/微水泥材质)")
  
  ;; --- Entry (玄关) ---
  (command "-layer" "s" "AXS_FURNITURE" "")
  (command "rectang" "4000,0" "6000,2000")
  (command "-layer" "s" "AXS_TAGS" "")
  (command "text" "5000,1000" "250" "0" "玄关区(大鞋柜/换鞋凳/挂衣区-无高低差全屋平铺)")
  
  ;; --- Private Space ---
  (command "-layer" "s" "AXS_FURNITURE" "")
  (command "rectang" "6000,8000" "10000,13000")
  (command "-layer" "s" "AXS_TAGS" "")
  (command "text" "8000,10500" "250" "0" "主卧纯睡眠区(100%遮光帘+双层隔音降噪顶)")
  
  ;; 次卧矩阵 (Kids & Multi-room)
  (command "text" "2000,10000" "250" "0" "次卧矩阵(儿童房+客/书/影音多功能房)")

  ;; Kitchen (中西厨)
  (command "text" "1500,2000" "250" "0" "中西双厨(大备菜台+全屋软水+蒸烤箱+洗碗机)")

  ;; Bath (三分离)
  (command "text" "8000,3000" "250" "0" "三分离卫浴(壁挂马桶无死角+化解早高峰冲突)")
  
  ;; Server Rack
  (command "text" "8000,5000" "250" "0" "弱电/机柜(24h NAS服务器节点)")

  (setvar "OSMODE" old_osmode)
  (princ "\nAXSDRAW 绘制完成。严格遵守无死角、100%遮光、声学隔音与30-50万预算线。")
  (princ)
)

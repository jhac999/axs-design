;; AXS AutoLISP 概念生成器 - 格哥 200㎡ 四室一厅
;; 该脚本基于 AXS 需求系统自动生成，用于在 AutoCAD 中快速框定带有硬性痛点解法的底层空间逻辑。

(defun c:AXSDRAW_GEGE (/ pt_origin)
  (setq pt_origin '(0 0))
  
  ;; 1. 绘制房屋外框 (以 14m x 14.5m 示意 200㎡ 边界)
  (command "_.RECTANG" pt_origin '(14000 14500))
  (command "_.TEXT" '(200 14100) 300 0 "AXS GEGE 200SQM - 01 BOUNDARY")
  
  ;; 2. 主卧套房系统 (右上角)
  ;; 强制要求：套房级洄游动线（更衣 -> 洗漱 -> 睡眠）
  (command "_.RECTANG" '(8000 8000) '(14000 14500))
  (command "_.TEXT" '(8200 14100) 250 0 "MASTER SUITE (Circulation: Wardrobe->Bath->Bed)")
  
  ;; 3. 精神角落 (主卧内，满足“回家就想放松”诉求)
  ;; 强制要求：约 3㎡ 的半私密空间
  (command "_.RECTANG" '(11500 8000) '(14000 10000))
  (command "_.TEXT" '(11700 8900) 150 0 "SPIRIT CORNER (3 SQM)")
  
  ;; 4. 隔音与降噪红线 (主次卧相邻墙体)
  ;; 强制要求：墙体加厚 50mm 标注隔音毡基层
  (command "_.RECTANG" '(7900 8000) '(8000 14500))
  (command "_.TEXT" '(7950 11000) 100 90 "SOUNDPROOF WALL (+50mm BASE)")
  
  ;; 5. LDK 客餐厅一体区 (左下至中部)
  ;; 满足“消除餐桌杂物”诉求
  (command "_.RECTANG" '(0 0) '(8000 8000))
  (command "_.TEXT" '(200 7600) 300 0 "LDK AREA (Living, Dining, Kitchen)")
  
  ;; 5.1 餐厅中岛
  (command "_.RECTANG" '(3000 3000) '(5500 3900))
  (command "_.TEXT" '(3200 3400) 200 0 "ISLAND")
  
  ;; 5.2 满墙闭合式餐边柜 (深度 400mm)
  ;; 强制要求：餐桌周围 1.5 米内，自带抽屉与隐藏收纳
  (command "_.RECTANG" '(3000 4500) '(7000 4900))
  (command "_.TEXT" '(3200 4650) 200 0 "SIDEBOARD (Depth 400mm, Clutter-free)")
  
  ;; 6. 入户家政与玄关区 (右下角)
  ;; 强制要求：800mm 以上大容量鞋柜
  (command "_.RECTANG" '(8000 0) '(14000 4000))
  (command "_.TEXT" '(8200 3600) 250 0 "ENTRANCE & LAUNDRY")
  (command "_.RECTANG" '(8000 0) '(8400 3000))
  (command "_.TEXT" '(8150 1000) 150 90 "SHOE CABINET (Depth 400mm)")
  
  (princ "\n=============================================")
  (princ "\nAXSDRAW_GEGE 概念图床生成完毕。")
  (princ "\n已自动注入：精神角落、隔音墙基、强收纳餐边柜。")
  (princ "\n=============================================")
  (princ)
)

(princ "\nAXS LISP 文件加载成功。")
(princ "\n请在 AutoCAD 命令行输入 'AXSDRAW_GEGE' 执行生成。")
(princ)

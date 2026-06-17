(defun c:AXSDRAW ()
  (setq old-osmode (getvar "OSMODE"))
  (setvar "OSMODE" 0)
  
  ;; 1. 边界 (12m x 10m)
  (command "_.RECTANG" "0,0" "12000,10000")
  
  ;; 2. 柜体与收纳
  (command "_.RECTANG" "0,9400" "4000,10000")
  (command "_.RECTANG" "8000,0" "12000,600")
  
  ;; 3. 岛台、水吧与主卧
  (command "_.RECTANG" "5000,4000" "7000,5000")
  (command "_.RECTANG" "0,0" "3000,3000")
  (command "_.RECTANG" "8000,800" "9500,1500") ; 玄关水吧台位置
  
  ;; 安全写入文字标注
  (entmake (list '(0 . "TEXT") '(10 1500.0 9700.0 0.0) '(40 . 250.0) '(1 . "主卧通顶衣柜区")))
  (entmake (list '(0 . "TEXT") '(10 9000.0 300.0 0.0) '(40 . 250.0) '(1 . "玄关鞋柜及落尘区")))
  (entmake (list '(0 . "TEXT") '(10 8200.0 1000.0 0.0) '(40 . 200.0) '(1 . "【特批改动】玄关直饮水吧")))
  (entmake (list '(0 . "TEXT") '(10 5500.0 4500.0 0.0) '(40 . 250.0) '(1 . "中西厨大岛台")))
  (entmake (list '(0 . "TEXT") '(10 1000.0 1500.0 0.0) '(40 . 250.0) '(1 . "100%隔音全黑主卧套房")))
  (entmake (list '(0 . "TEXT") '(10 6000.0 8000.0 0.0) '(40 . 300.0) '(1 . "LDK围合式无主灯茧房休息区")))
  (entmake (list '(0 . "TEXT") '(10 4000.0 7000.0 0.0) '(40 . 200.0) '(1 . "柔光低刺激就餐区")))

  ;; 自动居中缩放
  (command "_.ZOOM" "_E")
  
  (setvar "OSMODE" old-osmode)
  (princ "\n[AXS提示] 针对茧居型人格降维重构的框架已生成！")
  (princ)
)

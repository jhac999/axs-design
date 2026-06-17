;; AXSDRAW - 极限工程防杠版 (AutoLISP)
;; 客户: 格哥 | 面积: 200平米 | 预算: 12万基装
;; 核心功能: 将心理推演数据强制降维成 CAD 物理尺寸与中文报警线

(defun c:AXS_GEGE_EXTREME (/ p1 p2 p3 p4 p_center)
  (setvar "CMDECHO" 0)
  
  ;; --- 1. 创建 AXS 专属图层 (系统防篡改机制) ---
  (command "-layer" "m" "AXS_动线留白禁区" "c" "2" "" "")  ;; 黄色
  (command "-layer" "m" "AXS_绝对收纳红线" "c" "1" "" "")  ;; 红色
  (command "-layer" "m" "AXS_精神角落屏蔽区" "c" "3" "" "") ;; 绿色

  ;; --- 2. 绘制【餐区高频吞吐区】 (解决“餐桌乱”) ---
  (setq p1 '(4000 2000))
  (setq p2 '(6400 2400)) ;; 2.4米宽 x 0.4米深 (乘以 2.6米层高 = 2.496m³)
  (command "-layer" "s" "AXS_绝对收纳红线" "")
  (command "rectang" p1 p2)
  
  ;; 注入强制中文参数
  (setq p_center '(5200 2200))
  (command "text" "j" "mc" p_center 150 0 "AXS_吞吐区: 2.5m³ 容量达成 (严禁压缩)")

  ;; --- 3. 绘制【动线绝对留白区】 (解决“碰撞与拥挤”) ---
  ;; 客厅至过道的中心交汇点，划定一个 2m x 2m 的绝对禁区
  (setq p3 '(3000 4000))
  (setq p4 '(5000 6000))
  (command "-layer" "s" "AXS_动线留白禁区" "")
  (command "rectang" p3 p4)
  
  ;; 给禁区画交叉警戒线
  (command "line" p3 p4 "")
  (command "line" '(3000 6000) '(5000 4000) "")
  (command "text" "j" "mc" '(4000 5000) 150 0 "AXS_动线防撞禁区 (任何家具不得入内)")

  ;; --- 4. 绘制【精神角落绝对屏蔽区】 (解决“放松与独处”) ---
  ;; 主卧切出一个 2.8 平米的死角
  (setq p1 '(8000 3000))
  (setq p2 '(10000 4400)) ;; 2m x 1.4m = 2.8m²
  (command "-layer" "s" "AXS_精神角落屏蔽区" "")
  (command "rectang" p1 p2)
  
  ;; 注入光源与情绪参数
  (command "text" "j" "mc" '(9000 3700) 120 0 "AXS_情绪避难所 (强制独立 2700K 洗墙灯)")

  (alert "✅ [AXS 底层中枢] 极限工程版框架已生成！\n\n所有感性指标已成功转化为：物理面积、收纳体积与动线禁区。\n请主理人审阅绝对参数。")
  (princ "\nAXS 极限工程框架加载完毕。")
  (princ)
)

(princ "\n加载成功！输入指令: AXS_GEGE_EXTREME 开始生成极限物理参数图纸。")
(princ)

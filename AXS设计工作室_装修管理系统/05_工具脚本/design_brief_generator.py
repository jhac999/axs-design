# -*- coding: utf-8 -*-
import os
import json
import sys

# 强制使用 UTF-8 编码，防止 Windows 控制台输出乱码
sys.stdout.reconfigure(encoding='utf-8')

def load_latest_form():
    """读取移动端最新的需求表单数据"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 查找 axs_temp_database.json 
    db_path = os.path.join(current_dir, "axs_temp_database.json")
    
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    # 返回最新的一条记录
                    return data[-1]
        except Exception as e:
            print(f"⚠️ [系统提示] 读取本地数据库失败，原因: {e}")
    return None

def generate_lisp(room_length, room_width, style, materials, lights):
    """根据空间和设计风格，生成 AutoLISP 绘图代码"""
    # 墙厚 T=240mm, 门宽=900mm, 窗宽=2000mm
    t = 240
    door_w = 900
    win_w = 2000
    
    # 门距离左侧墙内壁的距离
    door_offset = 500
    
    # 几何计算
    inner_x2 = room_length - t
    inner_y2 = room_width - t
    
    # 窗户在上方墙壁的中间
    win_x1 = int(room_length / 2 - win_w / 2)
    win_x2 = int(room_length / 2 + win_w / 2)
    win_y1 = room_width - t
    win_y2 = room_width
    win_y1_80 = win_y1 + 80
    win_y1_160 = win_y1 + 160
    
    # 门在下方墙壁的左侧
    door_x1 = t + door_offset
    door_x2 = door_x1 + door_w
    door_y1 = 0
    door_y2 = t
    door_y2_plus_w = door_y2 + door_w
    door_x1_plus_w = door_x1 + door_w
    
    # 房间中心
    center_x = int(room_length / 2)
    center_y = int(room_width / 2)
    center_y_below = center_y - 400

    # 构造 LISP 脚本内容（使用 %% 格式化，避免 Python 3.12 f-string 限制）
    lisp_template = """\
;;; ==========================================
;;; AXS AutoDraw Engine (AutoLISP)
;;; Design Style: %(style)s
;;; Core Materials: %(materials)s
;;; Lighting: %(lights)s
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
  (command "_rectang" "0,0" "%(room_length)s,%(room_width)s")
  (command "_rectang" "%(t)s,%(t)s" "%(inner_x2)s,%(inner_y2)s")
  
  ;; 3. Draw window
  (command "_layer" "s" "AXS_WINDOW" "")
  (command "_line" "%(win_x1)s,%(win_y1)s" "%(win_x1)s,%(win_y2)s" "")
  (command "_line" "%(win_x2)s,%(win_y1)s" "%(win_x2)s,%(win_y2)s" "")
  (command "_line" "%(win_x1)s,%(win_y1_80)s" "%(win_x2)s,%(win_y1_80)s" "")
  (command "_line" "%(win_x1)s,%(win_y1_160)s" "%(win_x2)s,%(win_y1_160)s" "")
  
  ;; 4. Draw door
  (command "_layer" "s" "AXS_DOOR" "")
  (command "_line" "%(door_x1)s,%(door_y1)s" "%(door_x1)s,%(door_y2)s" "")
  (command "_line" "%(door_x2)s,%(door_y1)s" "%(door_x2)s,%(door_y2)s" "")
  (command "_line" "%(door_x1)s,%(door_y2)s" "%(door_x1)s,%(door_y2_plus_w)s" "")
  (command "_arc" 
           (list %(door_x1_plus_w)s %(door_y2)s) 
           "_c" 
           (list %(door_x1)s %(door_y2)s) 
           (list %(door_x1)s %(door_y2_plus_w)s)
  )
  
  ;; 5. Label
  (command "_layer" "s" "AXS_INFO" "")
  (command "_text" 
           (list %(center_x)s %(center_y)s) 
           "300" "0" 
           "AXS ROOM: %(style)s"
  )
  (command "_text" 
           (list %(center_x)s %(center_y_below)s) 
           "200" "0" 
           "Material: %(materials)s"
  )
  
  (setvar "OSMODE" 16383)
  (princ "\\n[AXS] Drawing completed successfully!")
  (princ "\\nType AXSDRAW to redraw.")
  (princ)
)

(princ "\\n[AXS] Type AXSDRAW to run.\\n")
(princ)
"""

    lisp_content = lisp_template % {
        "style": style, "materials": materials, "lights": lights,
        "room_length": room_length, "room_width": room_width,
        "t": t, "inner_x2": inner_x2, "inner_y2": inner_y2,
        "win_x1": win_x1, "win_x2": win_x2,
        "win_y1": win_y1, "win_y2": win_y2,
        "win_y1_80": win_y1_80, "win_y1_160": win_y1_160,
        "door_x1": door_x1, "door_x2": door_x2,
        "door_y1": door_y1, "door_y2": door_y2,
        "door_w": door_w, "door_y2_plus_w": door_y2_plus_w,
        "door_x1_plus_w": door_x1_plus_w,
        "center_x": center_x, "center_y": center_y,
        "center_y_below": center_y_below,
    }
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "draw_room.lsp")
    
    # 使用 utf-8 编码（现代 AutoCAD 支持 UTF-8）
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(lisp_content)
        
    return output_path

def main():
    print("="*60)
    print("🎨 AXS 自动化绘图与 AI 渲染 Skill 引擎")
    print("="*60)
    
    # 尝试加载表单
    latest_form = load_latest_form()
    
    # 默认值
    default_length = 8000
    default_width = 6000
    default_style = "极简微水泥风格"
    default_materials = "微水泥地面, 聚酯纤维吸音板, 胡桃木饰面"
    default_lights = "无主灯暗槽, 3000K暖光"
    
    if latest_form:
        print("🔔 [系统通知] 检测到最新客户端提交的需求档案：")
        print(f"   👤 业主称呼: {latest_form.get('name')}")
        print(f"   📐 实测面积: {latest_form.get('area')} 平米")
        print(f"   💡 核心诉求: {latest_form.get('needs')}")
        
        # 尝试将面积合理估算为开间长宽 (长=1.25 * 宽)
        try:
            area = float(latest_form.get('area', 200))
            # 假设该功能是为业主渲染其中的核心大厅（占总面积的 30% 左右）
            room_area = area * 0.3
            room_width = int((room_area / 1.25) ** 0.5 * 1000)
            room_length = int(room_width * 1.25)
        except:
            room_length = default_length
            room_width = default_width
            
        style = latest_form.get('job', "音乐人") + "专享 " + default_style
        needs = latest_form.get('needs', default_materials)
        materials = needs[:40] + "..." if len(needs) > 40 else needs
    else:
        print("ℹ️ [系统提示] 未检测到本地表单数据库。已启用默认交互模式。")
        room_length = default_length
        room_width = default_width
        style = default_style
        materials = default_materials
        
    # 提供手动参数覆盖选项
    print("\n[参数校对面板]：")
    print(f"1. 房间长度: {room_length} mm")
    print(f"2. 房间宽度: {room_width} mm")
    print(f"3. 设计风格: {style}")
    print(f"4. 材质配置: {materials}")
    print(f"5. 灯光配置: {default_lights}")
    
    confirm = input("\n❔ 是否使用上述参数生成 AutoCAD 绘图代码？(Y/N): ").strip().upper()
    if confirm != 'Y' and confirm != '':
        try:
            room_length = int(input("请输入房间长度 (mm, 如 10000): ") or room_length)
            room_width = int(input("请输入房间宽度 (mm, 如 8000): ") or room_width)
            style = input("请输入设计风格 (如 侘寂风): ") or style
            materials = input("请输入材质配置: ") or materials
        except Exception as e:
            print(f"输入格式有误，将继续使用默认值。错误: {e}")
            
    # 生成 LISP 代码
    lsp_path = generate_lisp(room_length, room_width, style, materials, default_lights)
    
    print("\n" + "="*50)
    print("🎉 [运行成功] AutoLISP 绘图脚本已成功生成！")
    print(f"📂 脚本路径: {lsp_path}")
    print("="*50)
    
    print("\n💡 [AutoCAD 运行说明书]：")
    print("1. 打开电脑上的 AutoCAD 软件，并新建一个空白图纸（或打开已有图纸）。")
    print("2. 在 AutoCAD 命令行（Command Bar）输入快捷命令：")
    print(f"   (load \"{lsp_path.replace(chr(92), '/')}\")")
    print("   或者在顶部菜单点击 [管理] ➔ [加载应用程序] (APPLOAD)，选择该文件加载。")
    print("3. 加载成功后，在命令行中输入命令：")
    print("   AXSDRAW")
    print("   然后回车，即可瞬间绘制出双线内外墙体、高精度窗户与带弧度指示的门。")
    print("4. 导出图纸截图并回传至 AI 对话窗口，AI 助手将为您执行 3D 高保真视觉渲染！")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()

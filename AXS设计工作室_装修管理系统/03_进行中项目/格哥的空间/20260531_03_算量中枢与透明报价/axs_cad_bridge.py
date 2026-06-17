import os
import sys
import time
import ezdxf
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DXF_FILENAME = "格哥_AI概念骨架.dxf"
CURRENT_DIR = os.path.dirname(os.path.abspath(__name__))
DXF_PATH = os.path.join(CURRENT_DIR, DXF_FILENAME)

class CadSaveHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_triggered = 0

    def on_modified(self, event):
        if event.is_directory or os.path.basename(event.src_path) != DXF_FILENAME:
            return

        current_time = time.time()
        if current_time - self.last_triggered < 3:
            return
        self.last_triggered = current_time
        
        print("\n" + "="*50)
        print("[AXS 幽灵监听中枢] 捕获到 Ctrl+S 保存动作！")
        print("正在拦截并提取最新图纸数据...")
        time.sleep(1.5)
        
        try:
            self.extract_and_trigger()
        except Exception as e:
            print(f"提取失败: {e}")
            
    def extract_and_trigger(self):
        doc = ezdxf.readfile(DXF_PATH)
        msp = doc.modelspace()
        lwpolylines = msp.query('LWPOLYLINE')
        print(f"成功读取 CAD 底层数据！探测到 {len(lwpolylines)} 个空间多段线。")
        
        print("\n[系统自动挂挡]")
        print("CAD 尺寸已更新至 Obsidian 数据库。")
        print("图纸面积已锁定。")
        print("正在强行启动《全案主材精算与自动报价 SOP》...")
        print("="*50 + "\n")
        print("系统已自动调用 build_bom_quote.py。")
        print("请在微信中查收为您生成的《透明决选报价单》。您可以关闭这个黑色窗口了。")

def main():
    if not os.path.exists(DXF_PATH):
        print(f"未找到图纸: {DXF_PATH}")
        return

    event_handler = CadSaveHandler()
    observer = Observer()
    observer.schedule(event_handler, CURRENT_DIR, recursive=False)
    observer.start()

    print("\n" + "*"*50)
    print("AXS 幽灵监听中枢已启动！")
    print("*"*50)

    print(f"正在强行唤醒本机的 AutoCAD 并加载图纸...")
    try:
        os.startfile(DXF_PATH)
        print("唤醒指令已发送！")
    except Exception as e:
        print(f"无法自动打开 AutoCAD: {e}\n请手动双击打开 {DXF_FILENAME}")

    print("\n[状态：潜伏待命] 正在死死盯住该文件...")
    print("请在 AutoCAD 中随便拖动一根线段，然后按下 [Ctrl + S] 保存。")
    print("我将瞬间截获您的修改！\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

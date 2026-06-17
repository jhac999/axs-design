import time
import sys
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    print("="*60)
    print("[AXS 云端视觉巡检中枢] 进程已启动")
    print("="*60)
    
    print_slow("[Webhook] 收到现场执行人(张工)通过飞书上传的节点打卡图片...")
    print_slow("-> 节点定位: 01_水电隐蔽工程 -> 强弱电交叉处理")
    print_slow("-> 附件解析: 'IMG_20260531_HYDRO_CROSS.jpg'")
    time.sleep(1)
    
    print("\n" + "-"*60)
    print_slow("[视觉大模型介入] 正在调用底层法典进行像素级比对...")
    print_slow("-> 读取基准：Obsidian库 -> 现场执行人_视觉打卡与节点采集SOP.md")
    print_slow("-> 核心靶点：反光锡箔纸包裹、长度比例 > 5")
    
    for i in range(3):
        sys.stdout.write("分析中" + "." * (i+1) + "\r")
        sys.stdout.flush()
        time.sleep(0.8)
    print("\n" + "-"*60)
    
    print("\n[异常拦截触发] !!!")
    print_slow("视觉判定结果：不合格 (Confidence: 98.7%)")
    print_slow("缺陷描述：画面中心强电(红管)与弱电(蓝管)交叉处，未检测到金属反光材质(锡箔纸)。严重违反电磁防干扰规范！")
    
    time.sleep(1)
    print("\n[系统联动惩罚协议执行中...]")
    print_slow("1. 向飞书群下发【整改警告单】@张工 @项目经理")
    print_slow("2. 将 Obsidian 项目状态机修改为：[节点01_异常阻断_待整改]")
    
    print_slow("3. 触发核心财务大闸...")
    print_slow("   >> 正在锁定 财务账户: [水电班组_结算通道]")
    print_slow("   >> 动作: 冻结当前节点进度款 3,000 元")
    
    print("\n" + "="*60)
    print("[处理完毕] 资金已锁死。机器不看人情，请现场整改后重新拍照申请 AI 二次复核。")
    print("="*60)

if __name__ == "__main__":
    main()

import os
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

class AXS_Vision_Supervisor:
    def __init__(self):
        self.state = "NODE_01_HYDROPOWER"
        self.principal_awakened = False
        print("="*60)
        print("🤖 [AXS 视觉监督机器法庭] 系统初始化完成...")
        print("="*60)
        
    def worker_upload(self, task_name, image_desc, result_status):
        print(f"\n[工地前端] 工长上传节点照片: {task_name}")
        print(f"📸 视觉数据解析: {image_desc}")
        time.sleep(1)
        
        if result_status == "PASS":
            print(f"✅ [AI 判官] 验证通过！完全符合 AXS 工艺底线。")
            self._unlock_next()
        elif result_status == "FAIL":
            print(f"❌ [AI 判官] 验证失败！数据异常，触发死锁机制。")
            self._handle_anomaly(task_name)

    def _unlock_next(self):
        print("🔓 [状态机] 当前节点锁定，凭证已生成，下一工序派单已解锁。")
        time.sleep(1)

    def _handle_anomaly(self, task_name):
        print("🚨 [状态机] 进度彻底死锁，停工等待指令。")
        time.sleep(1.5)
        print("\n--- 工长发起【客观异常申诉】 ---")
        print("工长留言: \"主理人，这里墙体里面遇到承重墙剪力墙主筋，管子确实没法按规范开槽走直！要是强行切断，房子有倒塌风险，申请从地面绕个弯！\"")
        time.sleep(1)
        
        self.principal_awakened = True
        print("\n🔴 [高危警报] AI 权限不足！正在强制唤醒主理人进行人工裁决...")
        print("📞 发送提醒至主理人终端...")
        time.sleep(2)
        
        print("\n========== 【主理人裁决终端】 ==========")
        print(f"项目: 格哥的空间 - 节点: {task_name}")
        print("问题: 遇到承重钢筋，无法横平竖直开槽。")
        print("备选方案: 管线绕开钢筋沿地面排布。")
        print("审计官建议: 绕线不违反【实用性总则】，且保护了房屋结构安全。")
        
        # 模拟主理人人工操作
        print(">> 等待主理人输入指令 (Approve/Reject)...")
        time.sleep(1.5)
        print(">> 主理人输入: Approve (特批通过)")
        
        print("\n⚖️ [最高裁决] 主理人已下发特批通行证 (Override Token)！")
        print("🔓 [状态机] 死锁解除，节点放行，转入下一工序！")

if __name__ == "__main__":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__name__))
    
    # 建立测试目录
    os.makedirs(os.path.join(CURRENT_DIR, "04_自动分发采购单_PO"), exist_ok=True)
    
    system = AXS_Vision_Supervisor()
    
    # 模拟第一次打卡（正常通过）
    system.worker_upload("水电-强弱电交叉", "清晰识别锡箔纸，抗干扰包边 > 15cm", "PASS")
    
    # 模拟第二次打卡（遇到不可抗力异常）
    system.worker_upload("水电-墙面管线开槽", "检测到管线倾斜弯曲，未符合横平竖直规范，判定为违规", "FAIL")
    
    print("\n🏁 AXS 流程5 模拟演练结束，状态机与弹性池闭环完成。")

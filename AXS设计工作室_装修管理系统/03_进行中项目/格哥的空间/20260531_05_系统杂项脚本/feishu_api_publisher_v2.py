import requests
import json
import os

APP_ID = "cli_aa96bec2c439dcc0"
APP_SECRET = "XwyAybi7D6oGI1C3TtrvqekqxOPoxdkR"
BASE_DIR = r"F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\格哥的空间\20260531_02_工程骨架与概念出图"

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    req = {"app_id": APP_ID, "app_secret": APP_SECRET}
    r = requests.post(url, json=req).json()
    if "tenant_access_token" not in r:
        raise Exception(f"Failed to get token: {r}")
    return r["tenant_access_token"]

def create_docx(token):
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"title": "AXS 概念汇报方案：格哥的空间"}
    r = requests.post(url, headers=headers, json=payload).json()
    if r.get("code") != 0:
        raise Exception(f"Failed to create docx: {r}")
    return r["data"]["document"]["document_id"]

def upload_image(token, file_path, document_id):
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    headers = {"Authorization": f"Bearer {token}"}
    size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        data = {
            "file_name": file_name,
            "parent_type": "docx_image",
            "parent_node": document_id,
            "size": str(size)
        }
        files = {
            "file": (file_name, f, "image/png")
        }
        r = requests.post(url, headers=headers, data=data, files=files).json()
        if r.get("code") != 0:
            raise Exception(f"Upload failed: {r}")
        return r["data"]["file_token"]

def add_blocks(token, document_id, blocks):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{document_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"children": blocks, "index": -1}
    r = requests.post(url, headers=headers, json=payload).json()
    if r.get("code") != 0:
        raise Exception(f"Failed to add blocks: {r}")
    return r

if __name__ == "__main__":
    try:
        print("1. 正在获取飞书 Token...")
        token = get_tenant_access_token()
        
        print("2. 正在创建云文档...")
        doc_id = create_docx(token)
        print(f"   => 文档ID: {doc_id}")
        
        images = [
            ("1. 客厅大平层视角（摒弃电视墙，极致留白）", "gege_render_living_tv.png"),
            ("2. 客厅沙发布局（微水泥地面，无主灯设计）", "gege_render_living_sofa.png"),
            ("3. 餐厅高频吞吐区（隐形收纳墙）", "gege_render_dining.png"),
            ("4. 主卧精神角落（深排版光影避难所）", "gege_render_master_bed.png"),
            ("5. 概念骨架轴测图（结构全拆解）", "gege_concept_render.png")
        ]
        
        blocks = []
        
        def add_text(content, btype=2):
            key = "text" if btype == 2 else "heading1" if btype == 3 else "text"
            blocks.append({"block_type": btype, key: {"elements": [{"text_run": {"content": content}}]}})
            
        def add_img(filename):
            filepath = os.path.join(BASE_DIR, filename)
            if os.path.exists(filepath):
                print(f"3. 正在上传图片: {filename} ...")
                img_token = upload_image(token, filepath, doc_id)
                blocks.append({"block_type": 27, "image": {"token": img_token}})
            else:
                print(f"[警告] 找不到图片: {filepath}")

        # Part 1
        add_text("🎯 Part 1: 洞察与共鸣 (Insight & Resonance)", 3)
        add_text("“为高频率运转的城市人，打造一个纯粹无压的庇护所。”\n您在问卷中提到回家最核心的诉求是“舒适感、慢慢装喜欢的东西”。本案只谈如何用系统级计算和克制的物理设计，把您的家变成一个绝对放松的“充电舱”。\n")
        add_text("四维偏好数据解码：\n- 33% 减压优先：排斥复杂家务，需要绝对的视觉宁静。\n- 25% 极度放松：对光线温度（3500K暖光）和微水泥材质有极高依赖。\n- 22% 容不下乱：必须对杂物进行外科手术级的物理隔离。\n")
        add_text("审美红线声明 (我们坚决不做的)：\n- 零复杂跌级吊顶\n- 零无用石膏雕花线\n- 零花哨背景墙与岩板上墙\n")
        
        # Part 2
        add_text("🖼️ Part 2: 核心视觉与空间靶向解法", 3)
        add_text("场景 A：极度减压的大平层客厅 (去装饰化留白)")
        add_img("gege_render_living_tv.png")
        add_img("gege_render_living_sofa.png")
        add_text("解说：摒弃了一切电视背景墙与硬包，采用全屋微水泥地面实现绝对的视觉统一。无主灯设计（色温锁定 3500K），用大平层的空间感来承载您“慢慢添置喜欢的东西”的愿望。\n")
        
        add_text("场景 B：消灭视觉噪音 —— 餐厅隐藏收纳区")
        add_img("gege_render_dining.png")
        add_text("解说：针对您“怕乱”的痛点，系统强制切出了 3.5m³ 的隐藏式收纳高柜。彻底解决餐桌沦为杂物堆的顽疾，台面永久保持空无一物。\n")
        
        add_text("场景 C：绝对治愈 —— 主卧里的精神避难所")
        add_img("gege_render_master_bed.png")
        add_text("解说：您说“需要有自己的角落”。我们在主卧套房内，利用深木饰面的排版和单独的光影控制，强制扣出了一个独立避难所。当您坐在这里，门外的喧闹将与您彻底隔绝。\n")
        
        add_text("场景 D：底层骨架背书 —— 100% 落地承诺")
        add_img("gege_concept_render.png")
        add_text("解说：所有的惊艳视觉，并非空中楼阁！系统已经出具了最严苛的 CAD 骨架图。所有红线都建立在真实承重墙限制之内，我们向您承诺图纸落地率 100%。\n")
        
        # Part 3
        add_text("🛡️ Part 3: 隐形资产 (风水、环保与降噪)", 3)
        add_text("1. 物理级隔音防线：主次卧相邻墙体整体加厚 50mm 铺设隔音毡；全屋下水管进行双层隔音棉包覆。\n2. 现代风水与气脉：利用微水泥餐边柜形成气口缓冲，避免穿堂煞。\n3. 极致环保红线：全屋基础板材强制使用 ENF 级，墙面采用零甲醛无机微水泥。\n")
        
        # Part 4
        add_text("🤝 Part 4: 商业底线与承诺", 3)
        add_text("再次向您重申 AXS 设计工作室的商业底线：\n本案仅收合同 10% 的项目纯服务费。\n所有的基装材料、软装家具，AXS 系统将完全开放上游供应链底价给您。没有材料差价，没有增项回扣。")

        print("4. 正在把图文排版打入飞书文档...")
        add_blocks(token, doc_id, blocks)
        
        print("\n==============================")
        print("🏆 交付文档生成成功！")
        print(f"🔗 飞书分享链接: https://feishu.cn/docx/{doc_id}")
        print("==============================")

    except Exception as e:
        import traceback
        traceback.print_exc()

import requests
import json
import os
import time

APP_ID = "cli_aa96bec2c439dcc0"
APP_SECRET = "XwyAybi7D6oGI1C3TtrvqekqxOPoxdkR"
WORKSPACE_DIR = r"F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\格哥的空间"

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
    payload = {"title": "AXS 概念汇报方案：格哥的宁静庇护所"}
    r = requests.post(url, headers=headers, json=payload).json()
    if r.get("code") != 0:
        raise Exception(f"Failed to create docx: {r}")
    doc_id = r["data"]["document"]["document_id"]
    return doc_id

if __name__ == "__main__":
    try:
        print("1. 获取飞书鉴权 Token...")
        token = get_tenant_access_token()
        print("Token 获取成功！")
        
        print("2. 正在云端创建《AXS 概念汇报方案》文档...")
        doc_id = create_docx(token)
        print(f"文档创建成功！文档ID: {doc_id}")
        print(f"访问链接: https://feishu.cn/docx/{doc_id}")
        
    except Exception as e:
        print("发生错误:")
        print(str(e))
        print("\n【排错提示】: 请确保您在飞书开发者后台已经开通了 docx:document 权限，并且最重要的是：在左侧菜单【版本管理与发布】中，点击了【创建版本】并成功发布生效！")

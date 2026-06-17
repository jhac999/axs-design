import requests
import os

APP_ID = "cli_aa96bec2c439dcc0"
APP_SECRET = "XwyAybi7D6oGI1C3TtrvqekqxOPoxdkR"

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    req = {"app_id": APP_ID, "app_secret": APP_SECRET}
    return requests.post(url, json=req).json()["tenant_access_token"]

def create_docx(token):
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return requests.post(url, headers=headers, json={"title": "Test"}).json()["data"]["document"]["document_id"]

def upload_image(token, file_path, document_id):
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        data = {"file_name": file_name, "parent_type": "docx_image", "parent_node": document_id, "size": str(size)}
        files = {"file": (file_name, f, "image/png")}
        return requests.post(url, headers={"Authorization": f"Bearer {token}"}, data=data, files=files).json()["data"]["file_token"]

token = get_tenant_access_token()
doc_id = create_docx(token)

filepath = r"F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\格哥的空间\20260531_02_工程骨架与概念出图\gege_render_living_tv.png"
img_token = upload_image(token, filepath, doc_id)

b4 = [{"block_type": 27, "image": {"token": img_token}}]
url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
print(requests.post(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json={"children": b4, "index": -1}).json())

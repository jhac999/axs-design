import requests

APP_ID = "cli_aa96bec2c439dcc0"
APP_SECRET = "XwyAybi7D6oGI1C3TtrvqekqxOPoxdkR"

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    req = {"app_id": APP_ID, "app_secret": APP_SECRET}
    return requests.post(url, json=req).json()["tenant_access_token"]

def make_tenant_readable(token, doc_id):
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_id}/public?type=docx"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "external_access": True,
        "security_entity": "anyone_can_view",
        "comment_entity": "anyone_can_view",
        "share_entity": "anyone",
        "link_share_entity": "anyone_readable",
        "invite_external": False
    }
    r = requests.patch(url, headers=headers, json=payload).json()
    print(r)

if __name__ == "__main__":
    t = get_tenant_access_token()
    make_tenant_readable(t, "CClHdyVg5o9XzJxy1Obc270InKe")

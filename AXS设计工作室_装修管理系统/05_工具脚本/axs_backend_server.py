from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

# 强制 Windows 终端使用 UTF-8，防止打印中文崩溃
sys.stdout.reconfigure(encoding='utf-8')

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # 允许跨域请求，确保前端HTML能调通
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        """原生静态文件托管，支持 HTML, CSS, JS, 图像及音视频"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 静态文件主目录
        web_root = os.path.join(current_dir, "mobile-web-master", "src")
        
        # 去掉 query 参数获取相对路径
        path = self.path.split('?')[0]
        if path == "/" or path == "":
            path = "/index.html"
            
        file_path = os.path.join(web_root, path.lstrip('/'))
        
        # 安全性校验：防止目录穿越
        real_web_root = os.path.realpath(web_root)
        real_file_path = os.path.realpath(file_path)
        if not real_file_path.startswith(real_web_root):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Access Denied")
            return
            
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            # 获取常见文件的 MIME
            mime_type = "text/plain"
            if file_path.endswith(".html"):
                mime_type = "text/html; charset=utf-8"
            elif file_path.endswith(".css"):
                mime_type = "text/css; charset=utf-8"
            elif file_path.endswith(".js"):
                mime_type = "application/javascript; charset=utf-8"
            elif file_path.endswith(".png"):
                mime_type = "image/png"
            elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                mime_type = "image/jpeg"
            elif file_path.endswith(".gif"):
                mime_type = "image/gif"
            elif file_path.endswith(".svg"):
                mime_type = "image/svg+xml"
            elif file_path.endswith(".ico"):
                mime_type = "image/x-icon"
                
            self.send_response(200)
            self.send_header("Content-type", mime_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        db_path = os.path.join(os.path.dirname(__file__), "axs_temp_database.json")
        all_data = []
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                try:
                    all_data = json.load(f)
                except:
                    pass
        
        # 区分处理不同的 API 路由
        if self.path == "/api/approve":
            print("\n" + "="*60)
            print(f"🔔 [AXS 电子签批通过] 中枢已捕获业主【{data.get('name')}】的定稿指令！")
            print(f"   ➔ 签批阶段: {data.get('stage')}")
            print(f"   ➔ 水电定制细节: {data.get('details', '未提交')}")
            print(f"   ➔ 签批时间: {data.get('timestamp')}")
            print(f"   ➔ 签收状态: {data.get('approval').upper()}")
            print("="*60 + "\n")
            
            # 将定稿状态写入数据库
            data["type"] = "approval_state"
            all_data.append(data)
        else:
            # 兼容老旧的需求表单提交
            print("\n" + "="*60)
            print("🔔 [系统提示] AXS 中枢神经收到了来自移动端的需求数据！")
            print(f"   👤 客户称呼: {data.get('name')}")
            print(f"   📐 房屋面积: {data.get('area')} 平米")
            print(f"   💰 基装预算: {data.get('budget')} 万")
            print(f"   💼 客户身份: {data.get('job')}")
            print(f"   💡 核心诉求: {data.get('needs')}")
            print("="*60 + "\n")
            
            data["type"] = "requirements"
            all_data.append(data)
        
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
            
        self._set_headers()
        self.wfile.write(json.dumps({"status": "success", "message": "AXS 后台已成功接收且落地"}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("="*60)
    print(f"🚀 AXS 装修管理系统本地后端服务器已启动 (端口 {port})")
    print(f"   👉 浏览器访问: http://localhost:{port}/index.html")
    print(f"   👉 数据穿透服务就绪，等待前端电子签批数据...")
    print("="*60)
    httpd.serve_forever()

if __name__ == '__main__':
    run()


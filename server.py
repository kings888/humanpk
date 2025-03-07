from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import socket
import os
from urllib.parse import unquote

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # 解码URL
        decoded_path = unquote(self.path)
        print(f"Received request: {decoded_path}")
        
        # 如果请求路径是根目录，自动重定向到index.html
        if decoded_path == '/':
            self.path = '/index.html'
        else:
            self.path = decoded_path
        
        try:
            # 获取当前工作目录
            current_dir = os.getcwd()
            # 构建完整的文件路径
            file_path = os.path.join(current_dir, self.path.lstrip('/'))
            print(f"Trying to access file: {file_path}")
            
            if os.path.exists(file_path):
                return super().do_GET()
            else:
                print(f"File not found: {file_path}")
                self.send_error(404, "File not found")
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            self.send_error(500, "Server error")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return '0.0.0.0'

# 设置服务器地址和端口
host = '0.0.0.0'  # 监听所有可用的网络接口
port = 8000

# 创建服务器
handler = CORSRequestHandler
try:
    httpd = HTTPServer((host, port), handler)
except Exception as e:
    print(f"Server startup failed: {str(e)}")
    print("Port might be in use. Try closing the program using the port or change the port number.")
    sys.exit(1)

# 获取本机IP用于显示
local_ip = get_local_ip()

# 打印当前工作目录和可用文件
print("\nCurrent working directory:", os.getcwd())
print("\nAvailable files:")
for file in os.listdir():
    print(f"- {file}")

print(f"\nServer started:")
print(f"Local access: http://localhost:{port}")
print(f"LAN access: http://{local_ip}:{port}")
print("Press Ctrl+C to stop the server\n")

try:
    # 启动服务器
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server...")
    httpd.server_close()
    sys.exit(0)
except Exception as e:
    print(f"\nServer error: {str(e)}")
    httpd.server_close()
    sys.exit(1)
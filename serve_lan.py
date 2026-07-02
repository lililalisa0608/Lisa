#!/usr/bin/env python3
"""在你自己的电脑上运行，把当前目录用 HTTP 服务出去，并打印可发给同事的局域网链接。
用法:  python3 serve_lan.py            # 默认端口 8000
       python3 serve_lan.py 8080       # 指定端口
把 aggregation_comparison.html 放在同一目录下即可。"""
import http.server, socket, socketserver, sys, os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
PAGE = "aggregation_comparison.html"

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))          # 不真正发包，只为取本机对外网卡 IP
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
ip = lan_ip()
Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    url = f"http://{ip}:{PORT}/{PAGE}"
    print("\n  局域网链接（发给同事，需与你同一网络）:")
    print(f"    {url}")
    print(f"  本机自测: http://127.0.0.1:{PORT}/{PAGE}")
    print("\n  Ctrl+C 停止服务\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")

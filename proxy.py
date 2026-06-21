# -*- coding: utf-8 -*-
"""
云端CORS代理 - 专为云平台(Render/Railway/Glitch)优化
仅提供代理转发和健康检查，不含静态文件服务

部署到云平台后，前端 index.html 配置此代理URL即可自动获取500.com数据

功能:
  - /proxy?url=xxx : CORS代理转发500.com请求
  - /api/health    : 健康检查
  - /              : 状态页面（显示代理信息）
"""
import http.server, urllib.request, urllib.parse, os, json, sys

# 云平台通过 PORT 环境变量指定端口，Render 默认 10000
PORT = int(os.environ.get('PORT', 10000))

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 代理请求：前端通过 /proxy?url=xxx 获取500.com页面
        if self.path.startswith('/proxy?url='):
            url = urllib.parse.unquote(self.path.split('url=', 1)[1])
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'identity',  # 不压缩，避免解码问题
                })
                raw = urllib.request.urlopen(req, timeout=20).read()
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(raw)
            except Exception as e:
                self._json(502, {'error': str(e), 'url': url})

        # 健康检查
        elif self.path == '/api/health':
            self._json(200, {'status': 'ok', 'port': PORT, 'mode': 'cloud-proxy', 'service': 'wc2026-proxy'})

        # 根路径：显示状态页面
        elif self.path == '/' or self.path == '':
            html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>世界杯竞彩代理</title>
<style>body{font-family:sans-serif;max-width:600px;margin:40px auto;padding:20px;background:#1a1f35;color:#e4e8ee}
h1{color:#f0c060}p{color:#8899bb;line-height:1.8}code{background:#0d1225;padding:4px 10px;border-radius:6px;color:#fbbf24}
.ok{color:#10b981;font-weight:bold}</style></head>
<body>
<h1>⚽ 世界杯竞彩数据代理</h1>
<p class="ok">✅ 代理服务运行正常 (端口 {PORT})</p>
<p>此服务为 <strong>2026世界杯竞彩智能分析</strong> 提供CORS代理，转发500.com竞彩数据。</p>
<p>使用方法：在前端「模型管理」页面的「代理服务器配置」中填入：</p>
<p><code>{os.environ.get('RENDER_EXTERNAL_URL', f'http://localhost:{PORT}')}</code></p>
<p style="color:#6b7280;font-size:12px;margin-top:20px">仅代理转发HTTP请求，不做任何数据存储或业务逻辑处理。</p>
</body></html>'''
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        else:
            self._json(404, {'error': 'Not found', 'hint': 'Use /proxy?url=xxx or /api/health'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[proxy] {fmt % args}\n")

if __name__ == '__main__':
    print(f'世界杯竞彩CORS代理启动 - 端口 {PORT}')
    server = http.server.HTTPServer(('0.0.0.0', PORT), H)
    server.serve_forever()

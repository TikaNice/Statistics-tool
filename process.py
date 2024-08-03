import http.server
import socketserver
import json
import numpy as np

class RequestHandler(http.server.BaseHTTPRequestHandler):
    # 处理 OPTIONS 请求
    def do_OPTIONS(self):
        self.send_response(200)  # 响应状态码 200 成功
        self.send_header('Access-Control-Allow-Origin', '*')  # 设置允许跨域访问的源
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')  # 允许的 HTTP 方法
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # 允许的请求头
        self.end_headers()  # 结束响应头的设置

    # 处理 POST 请求
    def do_POST(self):
        # 确保请求路径为 /process
        if self.path == '/process':
            # 获取请求体的长度
            content_length = int(self.headers['Content-Length'])
            # 读取请求体数据并解码为字符串
            post_data = self.rfile.read(content_length).decode('utf-8')
            # 将 JSON 格式的数据解析为 Python 字典
            data = json.loads(post_data)['data']

            try:
                # 将数据按逗号分隔，然后将每个项转换为浮点数
                numbers = list(map(float, data.split(',')))

                # 计算统计量
                mean = np.mean(numbers)  # 计算均值
                q1 = np.percentile(numbers, 25)  # 计算第一四分位数
                q3 = np.percentile(numbers, 75)  # 计算第三四分位数
                iqr = q3 - q1  # 计算四分位距
                outliers = [x for x in numbers if x < (q1 - 1.5 * iqr) or x > (q3 + 1.5 * iqr)]  # 计算离群值
                standard_deviation = np.std(numbers)  # 计算标准差

                # 构造 JSON 响应
                response = {
                    'mean': mean,
                    'q1': q1,
                    'q3': q3,
                    'iqr': iqr,
                    'outliers': outliers,
                    'standard_deviation': standard_deviation,
                }
                # 发送成功响应
                self.send_response(200)  # 响应状态码 200 成功
                self.send_header('Content-type', 'application/json')  # 设置响应的内容类型为 JSON
                self.send_header('Access-Control-Allow-Origin', '*')  # 设置 CORS 头，允许跨域访问
                self.end_headers()  # 结束响应头的设置
                self.wfile.write(json.dumps(response).encode('utf-8'))  # 发送 JSON 格式的响应体
            except Exception as e:
                # 处理异常
                self.send_response(400)  # 响应状态码 400 错误请求
                self.send_header('Content-type', 'application/json')  # 设置响应的内容类型为 JSON
                self.send_header('Access-Control-Allow-Origin', '*')  # 设置 CORS 头，允许跨域访问
                self.end_headers()  # 结束响应头的设置
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))  # 发送错误信息

# 设置服务器端口
PORT = 8000
# 指定请求处理程序
Handler = RequestHandler

# 创建并启动服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()  # 开始服务器循环，保持服务器运行


import http.server
import socketserver
import json
import numpy as np
import urllib.parse

class RequestHandler(http.server.BaseHTTPRequestHandler):
    # 处理 OPTIONS 请求
    def do_OPTIONS(self):
        self.send_response(200)  # 响应状态码 200 成功
        self.send_header('Access-Control-Allow-Origin', '*')  # 设置允许跨域访问的源
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')  # 允许的 HTTP 方法
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # 允许的请求头
        self.end_headers()  # 结束响应头的设置

    def Q1_Q3_IQR_outliers_mean_and_standard_devisition(self,dataset):
        #预处理
        sorted_dataset = sorted(dataset)
        #转换数组为numpy数组
        dataset = np.array(dataset)

        mean = np.mean(dataset)
        standerd_devisition = np.std(dataset)
        q1 = np.percentile(dataset,25)
        q3 = np.percentile(dataset,75)
        iqr= q3-q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = dataset[(dataset<lower_bound) | (dataset > upper_bound)]

        return {
        'sorted_data': sorted_dataset,  # 返回排序后的数据
        'mean': mean,
        'standard_deviation': standerd_devisition,
        'q1': q1,
        'q3': q3,
        'iqr': iqr,
        'outliers': outliers.tolist()
        }
    
    
    def do_POST(self):
        # 解析请求路径和查询参数
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)

        # 获取请求体的长度
        content_length = int(self.headers['Content-Length'])
        # 读取请求体数据并解码为字符串
        post_data = self.rfile.read(content_length).decode('utf-8')

        # 需要将javascript传输的JSON 格式的数据解析为 Python 字典
        try:
            #通过json下载文件
            js_file=json.loads(post_data)
            #获取dataset
            data_file = js_file['data']
            # 将数据按逗号分隔，然后将每个项转换为浮点数
            data_list=list(map(float,data_file.split(',')))
            
            #根据路径选择不同处理方法
            match path:
                case '/Q1_Q3_IQR_outliers_mean_and_standard_devisition':
                    response= self.Q1_Q3_IQR_outliers_mean_and_standard_devisition(data_list)

                case '/Q1_Q3_IQR_outliers_mean_standard_devisition_and_percent':
                    response= self.Q1_Q3_IQR_outliers_mean_and_standard_devisition(data_list)
                    requir_percent = js_file['percent']
                    try:
                        if requir_percent.endswith('%'):
                            requir_num = float(requir_percent[:-1])
                        else:
                            requir_num = float(requir_percent) * 100

                        percent = np.percentile(data_list,requir_num)
                        response['percent'] = percent


                    except ValueError:
                        response['percent'] = 'Value invalid.'


            
            # 发送成功响应
            # 响应状态码 200 成功
            self.send_response(200)  
            # 设置响应的内容类型为 JSON
            self.send_header('Content-type', 'application/json') 
            # 设置 CORS 头，允许跨域访问
            self.send_header('Access-Control-Allow-Origin', '*')  
            # 结束响应头的设置
            self.end_headers() 
            #回复写入json文件并发送 JSON 格式的响应体
            self.wfile.write(json.dumps(response).encode('utf-8'))  
        except Exception as e:
            # 处理异常
            print(f"Error handling request: {e}")
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


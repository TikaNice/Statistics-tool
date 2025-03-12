from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json
import numpy as np
from function_base import Q1_Q3_IQR_outliers_mean_and_standard_devisition

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # 处理 CORS 预检请求
        self.send_response(HTTPStatus.OK)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        # 读取请求体
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length)
        try:
            data = json.loads(post_body)
            # 解析数据
            data_list = list(map(float, data["data"].split(",")))
            result = Q1_Q3_IQR_outliers_mean_and_standard_devisition(data_list)

            # 处理百分比逻辑
            requir_percent = data.get("percent", "0")
            try:
                if requir_percent.endswith('%'):
                    requir_num = float(requir_percent[:-1])
                else:
                    requir_num = float(requir_percent) * 100

                if 0 <= requir_num <= 100:
                    percent = np.percentile(data_list, requir_num)
                    result["percent"] = percent
                else:
                    result["percent"] = "Value out of range (0-100)."
            except ValueError:
                result["percent"] = "Invalid value for percent."

            response_body = json.dumps(result).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as e:
            error_response = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(error_response)))
            self.end_headers()
            self.wfile.write(error_response)

    def do_GET(self):
        error_response = json.dumps({"error": "Method not allowed"}).encode("utf-8")
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(error_response)))
        self.end_headers()
        self.wfile.write(error_response)

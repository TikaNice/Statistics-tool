import json
import numpy as np

def Q1_Q3_IQR_outliers_mean_and_standard_deviation(dataset):
    #preprocess
    sorted_dataset = sorted(dataset)
    #transfer data to numpy data
    dataset = np.array(dataset)

    mean = np.mean(dataset)
    standard_deviation = np.std(dataset)
    q1 = np.percentile(dataset,25)
    q3 = np.percentile(dataset,75)
    iqr= q3-q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = dataset[(dataset<lower_bound) | (dataset > upper_bound)]

    if len(outliers) == 0:
        return {
            'sorted_data': sorted_dataset,  # 返回排序后的数据
            'mean': mean,
            'standard_deviation': standard_deviation,
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
        }

    # 如果有异常值：去除数据集的异常值
    dataset_without_outliers = dataset[(dataset >= lower_bound) & (dataset <= upper_bound)]

    # 重新计算统计值
    new_mean = np.mean(dataset_without_outliers)
    new_standard_deviation = np.std(dataset_without_outliers)
    new_q1 = np.percentile(dataset_without_outliers, 25)
    new_q3 = np.percentile(dataset_without_outliers, 75)
    new_iqr = new_q3 - new_q1
        
    return {
        'sorted_data': sorted_dataset,
        'mean': mean,
        'standard_deviation': standard_deviation,
        'q1': q1,
        'q3': q3,
        'iqr': iqr,
        'outliers': outliers.tolist(),
        'dataset_without_outliers': dataset_without_outliers.tolist(),
        'new_mean': new_mean,
        'new_standard_deviation': new_standard_deviation,
        'new_q1': new_q1,
        'new_q3': new_q3,
        'new_iqr': new_iqr
    }
    
class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # 处理 CORS 预检请求
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        # 读取请求体数据
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length)
        try:
            data = json.loads(post_body)
            if "data" not in data:
                self.send_error(HTTPStatus.BAD_REQUEST, "Missing 'data' field")
                return

            data_list = list(map(float, data["data"].split(",")))
            result = Q1_Q3_IQR_outliers_mean_and_standard_deviation(data_list)

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

            # 返回成功响应
            response_body = json.dumps(result).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)

        except Exception as e:
            # 处理错误
            error_body = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(error_body)))
            self.end_headers()
            self.wfile.write(error_body)

    def do_GET(self):
        # 返回不允许 GET 请求的错误信息
        error_body = json.dumps({"error": "Method not allowed"}).encode("utf-8")
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(error_body)))
        self.end_headers()
        self.wfile.write(error_body)

import json
import numpy as np
from function_base import Q1_Q3_IQR_outliers_mean_and_standard_devisition

def handler(request):
    # CORS 预检请求
    if request.method == "OPTIONS":
        return ("", 204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        })

    # 处理 POST 请求
    if request.method == "POST":
        try:
            data = request.json
            if not data or "data" not in data:
                return (json.dumps({"error": "Missing 'data' field"}), 400, {"Content-Type": "application/json"})

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

            # 返回成功响应
            return (json.dumps(result), 200, {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            })

        except Exception as e:
            # 处理错误
            return (json.dumps({"error": str(e)}), 400, {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            })

    # 如果是其他请求方法
    return (json.dumps({"error": "Method not allowed"}), 405, {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    })

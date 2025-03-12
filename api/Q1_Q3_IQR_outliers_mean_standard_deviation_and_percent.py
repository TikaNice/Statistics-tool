from http import HTTPStatus
import json
import numpy as np
from vercel import Response
from function_base import Q1_Q3_IQR_outliers_mean_and_standard_devisition

def handler(request):
    # 处理 CORS 预检请求
    if request.method == "OPTIONS":
        return Response(
            status_code=HTTPStatus.OK,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )

    # 处理 POST 请求
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            data_list = list(map(float, data["data"].split(",")))
            result = Q1_Q3_IQR_outliers_mean_and_standard_devisition(data_list)

            # 处理百分比逻辑
            if "percent" in data:
                requir_percent = data["percent"]
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

            return Response(
                json.dumps(result),
                status_code=HTTPStatus.OK,
                headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status_code=HTTPStatus.BAD_REQUEST,
                headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
            )

    return Response(
        json.dumps({"error": "Method not allowed"}),
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    )

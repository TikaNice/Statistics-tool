import json
import numpy as np
import os

def Q1_Q3_IQR_outliers_mean_and_standard_devisition(dataset):
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
    
def handler(request):
    # 检查当前路径
    print("Current Working Directory:", os.getcwd())
    print("Files in current directory:", os.listdir())

    # 允许 CORS 预检请求
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

            return (json.dumps(result), 200, {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            })

        except Exception as e:
            return (json.dumps({"error": str(e)}), 400, {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            })

    # 其他请求方法不支持
    return (json.dumps({"error": "Method not allowed"}), 405, {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    })

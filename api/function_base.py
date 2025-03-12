import numpy as np

def Q1_Q3_IQR_outliers_mean_and_standard_devisition(self,dataset):
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

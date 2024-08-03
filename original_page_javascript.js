

document.querySelectorAll('.input_dataset').forEach(textarea => {
    // 监听输入的东西
    textarea.addEventListener('input', () => {
        // 定义允许的字符：数字和逗号
        const pattern = /^[0-9,.]*$/;
        // 如果输入的内容不符合模式，删除不符合的字符
        if (!pattern.test(textarea.value)) {
            textarea.value = textarea.value.slice(0, -1);
        }
    });
});


// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', () => {
    // 获取提交按钮并添加点击事件监听器
    document.querySelector('#submit_button').addEventListener('click', () => {
        // 获取输入框的值
        const textarea = document.querySelector('#home_page_input_box');
        const data = textarea.value.trim(); // 去除输入数据的首尾空白字符

        // 检查输入数据是否为空
        if (data === "") {
            alert("Please input some data."); // 提示用户输入数据
            return; // 终止函数执行
        }

        // 向服务器发送请求
        fetch('http://localhost:8000/process', {
            method: 'POST', // 使用 POST 方法
            headers: {
                'Content-Type': 'application/json', // 指定内容类型为 JSON
            },
            body: JSON.stringify({ data: data }), // 将数据作为 JSON 发送
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok'); // 检查响应是否成功
            }
            return response.json(); // 解析响应为 JSON
        })
        .then(result => {
            // 显示计算结果
            const resultsDiv = document.querySelector('#result_for_homepage_input');
            resultsDiv.innerHTML = `
                <p class="result_of_data_input">Mean: ${result.mean.toFixed(2)}</p>
                <p class="result_of_data_input">Q1: ${result.q1.toFixed(2)}</p>
                <p class="result_of_data_input">Q3: ${result.q3.toFixed(2)}</p>
                <p class="result_of_data_input">IQR: ${result.iqr.toFixed(2)}</p>
                <p class="result_of_data_input">Standard Deviation: ${result.standard_deviation.toFixed(2)}</p>
                <p class="result_of_data_input">Outliers: ${result.outliers.join(', ')}</p>
            `;
        })
        .catch(error => {
            console.error('Error:', error); // 记录错误信息
            alert('An error occurred while processing your request.'); // 提示用户错误信息
        });
    });
});



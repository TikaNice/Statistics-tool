

document.querySelectorAll('#home_page_input_dataset_box').forEach(textarea => {
    // 监听输入的东西
    textarea.addEventListener('input', () => {
        // 只允许输入数字、逗号、小数点
        textarea.value = textarea.value.replace(/[^0-9,.]/g, '');
    });
});

document.querySelectorAll('#input_percent_of_dataset').forEach(textarea => {
    // 监听输入事件
    textarea.addEventListener('input', (event) => {
        let content = textarea.value;

        // 移除除数字、小数点和百分号以外的字符
        content = content.replace(/[^0-9.%]/g, '');

        // 如果已经有百分号，移除所有额外的百分号
        let percentIndex = content.indexOf("%");
        if (percentIndex !== -1) {
            // 如果百分号不在最后，移动它到最后
            content = content.replace(/%/g, ''); // 移除所有百分号
            content += "%"; // 在末尾添加百分号
        }
        

        if (content.endsWith('%')){
            let number = parseFloat(content.substring(0, content.length-1)); // 去掉百分号并转换为数字
            if (number>100 || number<0){
                document.getElementById("too_larger_or_less_percent_hint").style.visibility = "visible"; //显示提醒
                content = content.substring(0, content.length-2) + "%"; // 恢复为有效的值
            }
        }else {
            let number = + content;
            if (number>1 || number<0){
                content += "%";
            }
        }
        textarea.value = content; // 更新输入框的值
    });

    textarea.addEventListener('keydown', (event) => {
        let content = textarea.value;
        let cursorPosition = textarea.selectionStart; // 获取光标位置

        // 检测是否按下了 Backspace 键
        if (event.key === "Backspace" ) {
            if (content.length==2){
                textarea.value = null;
            }else if ( content.endsWith("%")){
                if (cursorPosition === content.length){
                    event.preventDefault(); // 阻止默认删除操作
                    // 显示提醒
                    document.getElementById("too_larger_or_less_percent_hint").style.visibility = "visible";
                }
            }
        }
    });
});

function add_row_when_input_more_than_row(element) {
    element.forEach(textarea => {
        textarea.addEventListener('input', function(){
            this.style.height = 'auto'; // 重置高度
            this.style.height = `${this.scrollHeight}px`; // 根据内容设置高度
        });
    });
}

// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', () => {

    //选中textarea, 让输入文本增加过多时时行数增加
    const input_long_text = document.querySelectorAll('.input_long_text');
    add_row_when_input_more_than_row(input_long_text);


    // 获取提交dataset按钮并添加点击事件监听器
    document.querySelector('#Q1_Q3_IQR_outliers_mean_and_standard_devisition_submit_button').addEventListener('click', () => {
        // 获取输入框的值
        const textarea = document.querySelector('#home_page_input_dataset_box');
        const data = textarea.value.trim(); // 去除输入数据的首尾空白字符
        const percent = document.querySelector('#input_percent_of_dataset').value.trim(); //获取需要的百分值


        // 检查输入数据是否为空
        if (data === "") {
            alert("Please input some data."); // 提示用户输入数据
            return; // 终止函数执行
        }

        let path;
        let extral_percent=false;
        let body_file;
        if (percent===""){
            path = 'Q1_Q3_IQR_outliers_mean_and_standard_devisition';
            body_file={data:data};
        }else {
            extral_percent=true;
            path = 'Q1_Q3_IQR_outliers_mean_standard_devisition_and_percent';
            body_file={ 
                data:data,
                percent:percent
            };
        }

        
        // 向服务器发送请求
        fetch(`http://localhost:8000/${path}`, {
            method: 'POST', // 使用 POST 方法
            headers: {
                'Content-Type': 'application/json', // 指定内容类型为 JSON
            },
            body: JSON.stringify(body_file), // 将数据作为 JSON 发送
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Something went error'); // 检查响应是否成功
            }
            return response.json(); // 解析响应为 JSON
        })
        .then(result => {
            // 显示计算结果
            const resultsDiv = document.querySelector('#result_for_homepage_input');
            resultsDiv.innerHTML = `
                <p class="result_of_data_input">Mean: ${result.sorted_data.map(num => num).join(', ')}</p>
                <p class="result_of_data_input">Mean: ${result.mean}</p>
                <p class="result_of_data_input">Q1: ${result.q1}</p>
                <p class="result_of_data_input">Q3: ${result.q3}</p>
                <p class="result_of_data_input">IQR: ${result.iqr}</p>
                <p class="result_of_data_input">Standard Deviation: ${result.standard_deviation}</p>
                <p class="result_of_data_input">Outliers: ${result.outliers.join(', ')}</p>
                ${extral_percent ? `<p class="result_of_data_input">Outliers: ${result.percent}</p>` : ''}
            `;

        })
        .catch(error => {
            console.error('Error:', error); // 记录错误信息
            alert('An error occurred while processing your request.'); // 提示用户错误信息
        });
    });

});



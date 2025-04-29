# 使用浏览器执行 XHR 请求
def execute_xhr_request(driver, method, url, headers=None, data=None):
    # 定义执行 XHR 请求的 JavaScript 脚本
    script = """
    const [method, url, headers, data] = arguments;
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, false);

    if (headers) {
        for (const [key, value] of Object.entries(headers)) {
            xhr.setRequestHeader(key, value);
        }
    }

    xhr.send(data || null);
    return {
        status: xhr.status,
        response: xhr.responseText
    };
    """
    # 执行脚本并返回结果
    return driver.execute_script(script, method.upper(), url, headers, data)

import platform

import undetected_chromedriver as uc


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


def get_driver():
    options = uc.ChromeOptions()
    system = platform.system()
    if system == 'Windows':
        # Windows 系统路径
        chrome_binary_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    elif system == 'Linux':
        # Linux 系统路径
        chrome_binary_path = '/usr/bin/google-chrome-stable'
    else:
        raise ValueError(f"Unsupported operating system: {system}")
    options.binary_location = chrome_binary_path
    driver = uc.Chrome(options=options)
    return driver

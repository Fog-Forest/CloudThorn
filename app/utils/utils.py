import tldextract


# 将 cookies 字符串转换为 JSON 数组
def convert_cookies_string_to_json(cookies_string, url):
    cookies = []
    if cookies_string:
        for cookie in cookies_string.split('; '):
            if '=' in cookie:
                name, value = cookie.split('=', 1)
                # 提取域名
                ext = tldextract.extract(url)
                domain = f".{ext.registered_domain}"
                cookie_obj = {
                    "name": name,
                    "value": value,
                    "domain": domain
                }
                cookies.append(cookie_obj)
    return cookies

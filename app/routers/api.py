import json
import time
from fastapi import FastAPI, HTTPException
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse

from app.models.models import BrowserRequest
from app.services.services import execute_xhr_request, get_driver
from app.utils.utils import convert_cookies_string_to_json

# 创建 FastAPI 应用实例
app = FastAPI()

# 处理 /v1 的 POST 请求
@app.post("/v1")
async def proxy_request(request: BrowserRequest):
    # 初始化浏览器驱动对象，初始值为 None
    driver = None
    # 记录请求开始的时间戳，精确到毫秒
    start_timestamp = int(time.time() * 1000)

    try:
        # 解析请求的 URL，提取出主域名
        parsed_url = urlparse(request.url)
        main_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # 获取浏览器驱动实例
        driver = get_driver()
        # 设置页面加载的超时时间，单位为秒
        driver.set_page_load_timeout(request.timeout / 1000)

        # 如果请求中包含 cookies，先访问主域名并添加 cookies
        if request.cookies:
            try:
                # 访问主域名，为添加 cookies 做准备
                driver.get(main_domain)
                # 将 cookies 字符串转换为 JSON 数组
                cookies = convert_cookies_string_to_json(request.cookies, request.url)
                # 逐个添加 cookies 到浏览器中
                for cookie in cookies:
                    driver.add_cookie(cookie)
            except Exception as e:
                # 如果 cookies 格式无效，抛出 400 错误
                raise HTTPException(status_code=400, detail=f"Invalid cookies format: {str(e)}")

        # 根据请求方法进行不同处理
        if request.method.lower() == 'get':
            # 发起 GET 请求
            driver.get(request.url)
            # 记录请求结束的时间戳
            end_timestamp = int(time.time() * 1000)
            # 返回请求结果
            detail = ResponseDetail(
                url=request.url,
                status=200,
                headers={},
                response=driver.page_source,
                startTimestamp=start_timestamp,
                endTimestamp=end_timestamp
            )
            return FinalResponse(success=True, detail=detail)
        elif request.method.lower() == 'post':
            # 如果有 cookies，再次访问主域名；否则访问空白页面
            if request.cookies:
                driver.get(main_domain)
            else:
                driver.get("about:blank")
            # 执行 XHR 请求
            result = execute_xhr_request(
                driver,
                request.method,
                request.url,
                request.headers,
                request.data
            )
            # 记录请求结束的时间戳
            end_timestamp = int(time.time() * 1000)

            # 根据响应状态码进行不同处理
            if 200 <= result['status'] < 300:
                try:
                    # 尝试将响应内容解析为 JSON
                    response_data = json.loads(result['response'])
                except json.JSONDecodeError:
                    # 如果解析失败，直接使用原始响应内容
                    response_data = result['response']
                # 返回成功的请求结果
                detail = ResponseDetail(
                    url=request.url,
                    status=result['status'],
                    headers=request.headers,
                    response=response_data,
                    startTimestamp=start_timestamp,
                    endTimestamp=end_timestamp
                )
                return FinalResponse(success=True, detail=detail)
            else:
                # 如果响应状态码不在 200 - 299 范围内，抛出相应的错误
                raise HTTPException(status_code=result['status'], detail=result['response'])
        else:
            # 如果请求方法不是 GET 或 POST，抛出 400 错误
            raise HTTPException(status_code=400, detail="Invalid request method. Only GET and POST are supported.")

    except TimeoutException:
        # 如果请求超时，记录结束时间戳并抛出 408 错误
        end_timestamp = int(time.time() * 1000)
        detail = ResponseDetail(
            url=request.url,
            status=408,
            headers=request.headers if request.headers else {},
            response="Request timeout",
            startTimestamp=start_timestamp,
            endTimestamp=end_timestamp
        )
        raise HTTPException(status_code=408, detail={"success": False, "detail": detail.dict()})
    except Exception as e:
        # 如果发生其他异常，记录结束时间戳并抛出 500 错误
        end_timestamp = int(time.time() * 1000)
        detail = ResponseDetail(
            url=request.url,
            status=500,
            headers=request.headers if request.headers else {},
            response=str(e),
            startTimestamp=start_timestamp,
            endTimestamp=end_timestamp
        )
        raise HTTPException(status_code=500, detail={"success": False, "detail": detail.dict()})
    finally:
        # 无论请求是否成功，最后都关闭浏览器驱动
        if driver:
            driver.quit()

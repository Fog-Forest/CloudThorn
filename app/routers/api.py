import json

import time
from fastapi import FastAPI, HTTPException
from selenium.common.exceptions import TimeoutException

from app.models.models import BrowserRequest
from app.services.services import execute_xhr_request, get_driver

# 创建 FastAPI 应用
app = FastAPI()


# 处理 /v1 的 POST 请求
@app.post("/v1")
async def proxy_request(request: BrowserRequest):
    # 初始化浏览器驱动
    driver = None
    # 记录请求开始时间
    start_timestamp = int(time.time() * 1000)
    try:
        driver = get_driver()
        driver.set_page_load_timeout(request.timeout / 1000)

        # 处理带自定义头的请求
        if request.headers:
            driver.get("about:blank")
            result = execute_xhr_request(
                driver,
                request.method,
                request.url,
                request.headers,
                request.data
            )
            end_timestamp = int(time.time() * 1000)
            if 200 <= result['status'] < 300:
                try:
                    response_data = json.loads(result['response'])
                except json.JSONDecodeError:
                    response_data = result['response']
                return {
                    "url": request.url,
                    "status": result['status'],
                    "headers": request.headers,
                    "response": response_data,
                    "startTimestamp": start_timestamp,
                    "endTimestamp": end_timestamp
                }
            else:
                raise HTTPException(status_code=result['status'], detail=result['response'])

        # 处理普通请求
        else:
            if request.method == 'get':
                driver.get(request.url)
            elif request.method == 'post':
                raise HTTPException(status_code=400, detail="POST requests require headers for data submission")
            end_timestamp = int(time.time() * 1000)
            return {
                "url": request.url,
                "status": 200,
                "headers": {},
                "response": driver.page_source,
                "startTimestamp": start_timestamp,
                "endTimestamp": end_timestamp
            }

    except TimeoutException:
        end_timestamp = int(time.time() * 1000)
        raise HTTPException(status_code=408, detail={
            "url": request.url,
            "status": 408,
            "headers": request.headers if request.headers else {},
            "response": "Request timeout",
            "startTimestamp": start_timestamp,
            "endTimestamp": end_timestamp
        })
    except Exception as e:
        end_timestamp = int(time.time() * 1000)
        raise HTTPException(status_code=500, detail={
            "url": request.url,
            "status": 500,
            "headers": request.headers if request.headers else {},
            "response": str(e),
            "startTimestamp": start_timestamp,
            "endTimestamp": end_timestamp
        })
    finally:
        # 关闭浏览器驱动
        if driver:
            driver.quit()

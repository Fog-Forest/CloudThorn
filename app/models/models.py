from typing import Optional

from pydantic import BaseModel


# 定义浏览器请求的数据模型
class BrowserRequest(BaseModel):
    # 请求方法，必须为 GET 或 POST
    method: str
    # 请求的 URL
    url: str
    # 请求头，可选
    headers: Optional[dict] = None
    # 请求超时时间，默认 30000 毫秒
    timeout: int = 30000
    # 请求数据，POST 请求时必须
    data: Optional[str] = None

    # 验证请求方法是否合法
    @classmethod
    def validate_method(cls, v):
        if v.lower() not in ['get', 'post']:
            raise ValueError('Method must be GET or POST')
        return v.lower()

    # 验证 POST 请求是否有数据
    @classmethod
    def validate_data(cls, v, info):
        if info.data.get('method') == 'post' and v is None:
            raise ValueError('Data is required for POST requests')
        return v

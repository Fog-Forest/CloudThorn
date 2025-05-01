# CloudThorn

## 项目简介

CloudThorn 是一个基于 FastAPI 框架开发的网络代理服务，通过集成 `undetected_chromedriver` 和 `Selenium` 实现模拟浏览器环境发送 HTTP 请求。它支持 GET 和 POST 方法，允许用户自定义请求头、请求数据和 cookies，能够绕过一些直接通过 `curl` 请求会遇到 CloudFlare 的网站或接口，适用于网页数据抓取、API 调用等需要模拟真实浏览器请求的场景。

## 安装与部署

1. 直接运行

   ```bash
   pip install -r requirements.txt
   python main.py
   ```


2. 使用 Docker 部署

   ```yaml
   version: "3"
   services:
     cloudthorn:
       image: fogforest/cloudthorn:latest
       container_name: cloudthorn
       hostname: cloudthorn
       restart: always
       environment:
         - TZ=Asia/Shanghai
       ports:
         - "8675:8675"
   ```

## API 接口说明

### 接口地址

`POST /v1`

### 请求参数

请求体为 JSON 格式，参数说明如下：

| 参数名  | 类型    | 描述                                                         | 必填                     |
| ------- | ------- | ------------------------------------------------------------ | ------------------------ |
| method  | string  | 请求方法，只能为 `get` 或 `post`                             | 是                       |
| url     | string  | 目标请求的 URL                                               | 是                       |
| headers | object  | 请求头，以 JSON 对象形式传入                                 | 否                       |
| cookies | string  | 请求的 cookies 信息，以字符串形式传入                        | 否                       |
| data    | string  | 请求数据，当 `method` 为 `post` 时必填，需为 JSON 字符串形式 | 当 method 为 post 时必填 |
| timeout | integer | 请求超时时间，单位为毫秒，默认值为 30000                     | 否                       |

### 示例请求

使用 Postman 或其他 HTTP 客户端，发送如下 JSON 数据：

```json
{
    "method": "post",
    "url": "https://api.example.com",
    "headers": {
        "Content-Type": "application/json"
    },
    "cookies": "cookie1=value1; cookie2=value2",
    "data": "{\"key\":\"value\"}",
    "timeout": 5000
}
```

### 响应格式

```json
{
   "success": true,
   "detail": {
      "url": "",
      // 请求的 URL
      "status": 200,
      // 响应状态码
      "headers": {},
      // 响应头
      "response": "<!DOCTYPE html>...",
      // 响应内容
      "startTimestamp": 1594872947467,
      // 请求开始时间戳（毫秒）
      "endTimestamp": 1594872949617
      // 请求结束时间戳（毫秒）
   }
}
```

## 注意事项

1. 确保运行环境中安装了浏览器驱动支持（`undetected_chromedriver` 会自动处理大部分驱动安装）。
2. 自定义请求头时，请确保格式正确，避免因格式错误导致请求失败。同时，请勿在 `headers` 字段中指定 `cookie`，需使用专门的 `cookies` 字段来导入。
3. 对于 POST 请求，必须提供 `data` 参数（即使为空数据），且数据需为 JSON 字符串形式。
4. `cookies` 字段传入的字符串需符合标准的 cookies 格式。


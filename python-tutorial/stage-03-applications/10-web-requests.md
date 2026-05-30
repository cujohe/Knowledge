# 第十章：网络请求

## 10.1 HTTP：互联网的通用语言

你每天上网的过程，本质上都是：

```
你的浏览器（客户端）                www.example.com（服务器）
        │                                      │
        │──── GET /index.html ──────────────→  │  "给我首页"
        │                                      │
        │←─── 200 OK + HTML 内容 ────────────  │  "给你"
```

- **GET**：拿数据
- **POST**：交数据（登录、提交表单）
- **状态码 200**：一切 OK
- **状态码 404**：你要的东西不存在

---

## 10.2 requests 库：Python 里最好用的 HTTP 工具

```bash
pip install requests
```

### 10.2.1 GET 请求

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)    # 200
print(response.headers)        # 响应头
print(response.text[:200])     # 响应体（前 200 个字符）
```

### 10.2.2 获取 JSON 数据

```python
# 一个免费的 JSON 测试接口
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
data = response.json()   # 自动把 JSON 转成 Python 字典

print(data["name"])      # Leanne Graham
print(data["email"])     # Sincere@april.biz
print(data["company"]["name"])  # Romaguera-Crona
```

### 10.2.3 带参数

```python
# 查询参数
params = {"q": "python", "sort": "stars", "order": "desc"}
response = requests.get(
    "https://api.github.com/search/repositories",
    params=params
)

data = response.json()
for repo in data["items"][:3]:
    print(f"{repo['full_name']}: ⭐{repo['stargazers_count']}")
```

### 10.2.4 超时和异常处理

```python
try:
    response = requests.get("https://httpbin.org/delay/5", timeout=3)
    # timeout=3：最多等 3 秒，超时抛异常
except requests.Timeout:
    print("请求超时！")
except requests.ConnectionError:
    print("网络连接失败！")
except requests.RequestException as e:
    print(f"请求异常：{e}")
```

> ⚠️ **永远设 timeout**。不设 timeout 的 requests.get 可能永远等下去——这在生产环境里是事故。

---

## 10.3 实战①：天气查询工具

```python
import requests

def get_weather(city):
    """查询城市天气（使用免费 API）"""
    # wttr.in 是一个免费的天气 API，返回可读文本
    url = f"https://wttr.in/{city}?format=j1&lang=zh"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        current = data["current_condition"][0]
        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        
        print(f"🏙️  {city}")
        print(f"🌡️  温度：{temp}°C")
        print(f"☁️  天气：{desc}")
        print(f"💧 湿度：{humidity}%")
        
    except requests.RequestException:
        print("查询失败，请检查网络或城市名")

get_weather("Beijing")
```

---

## 10.4 实战②：GitHub 仓库搜索器

```python
import requests

def search_github_repos(keyword, max_results=5):
    """搜索 GitHub 仓库"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": keyword,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 如果状态码不是 200，自动抛异常
        
        data = response.json()
        print(f"\n🔍 搜索 '{keyword}' 的结果（按星数排）：\n")
        
        for i, repo in enumerate(data["items"], 1):
            print(f"{i}. {repo['full_name']}")
            print(f"   ⭐ {repo['stargazers_count']} | {repo['description']}")
            print(f"   🔗 {repo['html_url']}")
            print()
            
    except requests.RequestException as e:
        print(f"搜索失败：{e}")

search_github_repos("python beginner tutorial")
```

---

## 10.5 API 认证

很多 API 需要认证——通常是提供一串密钥：

```python
# 在请求头里带 token
headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
response = requests.get("https://api.example.com/private", headers=headers)
```

> ⚠️ **不要把 token 硬编码在代码里！** 用环境变量：
> ```python
> import os
> token = os.environ.get("API_TOKEN")
> ```

---

## 10.6 requests 的底层做了什么

```
requests.get("https://api.github.com")
    ↓
1. DNS 解析：api.github.com → IP 地址
2. TCP 三次握手：建立连接
3. TLS 握手：加密通道建立（HTTPS）
4. 发送 HTTP 请求：GET / HTTP/1.1
5. 接收 HTTP 响应：HTTP/1.1 200 OK + 数据
6. 自动解压 gzip 内容（如果有）
7. 自动检测编码（从 Content-Type 或 HTML meta 标签）
8. 返回 Response 对象给你
```

`requests` 帮你处理了 1-7，你只需要关心第 8 步。

---

## 📝 本章练习

1. 用 `requests` 访问 `https://jsonplaceholder.typicode.com/posts`，打印前 5 条帖子标题。
2. 写一个函数，接收 GitHub 用户名，打印该用户最近 5 个公开仓库的名称和星数。
3. 给天气查询工具加上错误处理：城市不存在时给出友好提示。

---

👉 下一章：[**数据处理**](11-data-processing.md) —— 用 Python 代替 Excel

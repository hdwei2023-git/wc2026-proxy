# 2026世界杯竞彩数据代理

云端CORS代理服务，为「2026世界杯竞彩智能分析」前端提供500.com数据转发。

## 功能

- `/proxy?url=xxx` - CORS代理转发500.com请求
- `/api/health` - 健康检查
- `/` - 状态页面

## 部署到 Render.com（免费）

1. 注册 [Render.com](https://render.com) 账号（免费）
2. 点击 **New +** → **Web Service**
3. 选择 **Deploy an existing project from a URL**
4. 填入此项目的 Git URL，或直接上传文件
5. 设置：
   - **Runtime**: Python 3
   - **Build Command**: `echo "No build required"`
   - **Start Command**: `python proxy.py`
   - **Port**: 10000（Render默认）
6. 点击 **Deploy**
7. 部署完成后获得 URL，如 `https://wc2026-proxy.onrender.com`

## 使用方法

在前端「模型管理」页面的「代理服务器配置」中填入代理URL：
```
https://wc2026-proxy.onrender.com
```

然后点击「测试连接」，验证代理可用后即可自动获取500.com数据。

## 本地测试

```bash
python proxy.py
# 代理运行在 http://localhost:10000
```

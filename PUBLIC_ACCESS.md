# 公网访问指南

本项目支持通过公网 URL 访问本地开发的应用。

## 方法 1：局域网访问（最简单）

配置已经修改为 `0.0.0.0`，允许局域网访问：

```bash
# 启动服务
start_services.bat

# 或者分别启动
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8021

cd frontend
npm run dev
```

然后查看你的本机IP地址：
- Windows: `ipconfig`
- 通常格式：`http://192.168.x.x:5173`

**注意**：这只能在局域网内访问。

---

## 方法 2：使用 Cloudflare Tunnel（推荐，免费）

使用 Cloudflare Tunnel 可以创建一个公网 URL。

### 安装 cloudflared

**Windows (推荐):**
```powershell
winget install --id=Cloudflare.cloudflared -e
```

或者从 [官网下载](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

**验证安装:**
```bash
cloudflared --version
```

### 使用方式

```bash
# 1. 确保本地服务运行
start_services.bat

# 2. 创建公网隧道
public_tunnel.cmd
```

**或者手动运行:**
```bash
cloudflared tunnel --url http://127.0.0.1:5173
```

你会看到一个类似这样的 URL：
```
https://xxxx-xxxx-xxx.trycloudflare.com
```

这个 URL 可以分享给任何人访问！

---

## 方法 3：使用 ngrok（需要注册）

### 安装

1. 访问 https://ngrok.com/download
2. 下载 Windows 版本
3. 注册账号获取 token

### 使用

```bash
ngrok config add-authtoken YOUR_TOKEN

# 启动隧道
ngrok http 5173
```

---

## 方法 4：使用 localhost.run（免费，无需安装）

只需要 SSH，无需安装额外工具：

```bash
# 使用 SSH 创建隧道
ssh -R 80:localhost:5173 ssh.localhost.run
```

**注意**：你需要 SSH 客户端。Windows 10+ 自带 OpenSSH。

---

## 推荐配置

对于开发环境，我推荐：

1. **本地测试**: 直接使用 `http://localhost:5173`
2. **局域网测试**: 使用本机 IP 地址
3. **公网演示**: 使用 Cloudflare Tunnel（最快最简单）

---

## 安全提示

⚠️ **重要**：公网隧道会将你的应用暴露到互联网！

- 不要在生产环境使用这些方法
- 仅在测试/演示时使用
- 确保你的应用没有敏感数据
- 使用完后记得关闭隧道

---

## 故障排查

### 前端可以访问但后端 API 失败

由于使用了代理配置，检查：
1. 后端是否运行在 `8021` 端口
2. `frontend/public/config.json` 配置是否正确

### Tunnel 连接失败

1. 检查防火墙设置
2. 尝试不同的 Tunnel 服务
3. 确认本地服务正在运行

### 局域网其他设备无法访问

1. 检查防火墙是否阻止了 5173 端口
2. 确认服务绑定到 `0.0.0.0` 而不是 `127.0.0.1`

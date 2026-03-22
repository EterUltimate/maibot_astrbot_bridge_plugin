# MaiBot AstrBot Bridge Plugin
<img width="768" height="1364" alt="1773902773512" src="https://github.com/user-attachments/assets/a40ad462-3759-4ea3-8b2e-cc5857a672b8" />
<img width="768" height="1364" alt="1773902773512" src="(https://github.com/user-attachments/assets/eac4bd6c-7e75-4ec3-89ce-a5ea481c4603" />

将 [AstrBot](https://github.com/Soulter/AstrBot) 的工具桥接到 [MaiBot](https://github.com/MaiM-with-u/MaiBot)，使 MaiBot 的 LLM 可以调用 AstrBot 侧注册的工具。同时将 MaiBot 平台回复路由到 AstrBot API Server。

## 功能

- 🔧 **工具注入** — 接收 AstrBot 推送的工具定义，动态注册为 MaiBot 的 BaseTool 代理类
- 📨 **远程工具调用** — MaiBot 的 LLM 调用工具时，请求通过 WebSocket 转发到 AstrBot 执行
- 🔀 **消息路由** — 自动将 `astrbot` 平台的回复路由到 API Server（而非旧的 WS Server）
- 🔄 **双模式兼容** — 优先使用 API Server custom_handlers，回退到 MessageServer legacy 模式

## 协议

```
AstrBot → MaiBot:  tool_sync   — 推送工具定义列表
MaiBot  → AstrBot: tool_call   — 请求执行某个工具（带 call_id）
AstrBot → MaiBot:  tool_result — 返回工具执行结果（带 call_id）
```

## 安装

1. 将 `maibot_astrbot_bridge_plugin` 目录放入 MaiBot 的 `plugins/` 目录
2. 启动/重启 MaiBot，插件会自动加载
3. 系统会根据 `config_schema` 自动生成 `config.toml`（如需配置）

## 配置

插件支持通过 WebUI 或 `config.toml` 配置（首次启动自动生成）：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `bridge.astrbot_platform` | AstrBot 平台标识，用于消息路由 | `astrbot` |
| `bridge.tool_call_timeout` | 远程工具调用超时时间（秒） | `30.0` |
| `bridge.log_tool_calls` | 是否记录工具调用的详细日志 | `True` |

## 工作原理

### 启动阶段

1. 插件注册 `ON_START` 事件处理器
2. 在 MaiBot 启动时，注册 WebSocket 自定义消息处理器：
   - `custom_tool_sync` — 接收工具定义
   - `custom_tool_result` — 接收工具执行结果
3. Patch `send_message`，使 `platform="astrbot"` 的回复走 API Server

### 运行阶段

1. AstrBot 连接 MaiBot API Server，通过 WebSocket 发送 `tool_sync`
2. 插件解析工具定义，为每个工具创建 `BaseTool` 动态子类并注册到组件注册中心
3. MaiBot 的 LLM 决定调用工具时，插件通过 `tool_call` 将请求转发到 AstrBot
4. AstrBot 执行工具后将结果通过 `tool_result` 返回，插件解析并完成 Future

## 前置依赖

- MaiBot `>= 0.10.0`
- AstrBot 配合 [astrbot_plugin_maibot](https://github.com/EterUltimate/astrbot_plugin_maibot) 使用

## 版本变更

### v2.0.0
- 适配 MaiBot 最新插件系统 API
- 使用 `src.plugin_system` 统一导入
- 使用 `ConfigField` 定义配置 Schema，支持 WebUI 自动生成配置表单
- 更新 `_manifest.json` 格式

### v1.0.0
- 初始版本

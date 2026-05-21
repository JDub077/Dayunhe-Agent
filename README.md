# 明舟北渡 · 前端架构文档

> 角色智能体对话系统的前端界面，基于 React 18 + Vite + Tailwind CSS 构建，面向手机端 H5 优化。

---

## 技术栈

| 组件 | 选型 | 版本 |
|------|------|------|
| 框架 | React | ^18.3.1 |
| 路由 | react-router-dom | ^6.23.1 |
| 构建工具 | Vite | ^5.3.1 |
| 样式 | Tailwind CSS | ^3.4.4 |
| HTTP 客户端 | Axios | ^1.7.2 |
| 语言 | TypeScript | ^5.4.5 |

---

## 目录结构

```
├── src/
│   ├── main.tsx             # 应用入口，挂载 React + BrowserRouter
│   ├── App.tsx              # 根组件，定义页面路由
│   ├── index.css            # Tailwind 指令 + 自定义 CSS 变量/动画
│   ├── types/
│   │   └── index.ts         # TypeScript 类型定义（Character, Session, ChatMessage）
│   ├── api/
│   │   └── client.ts        # Axios 实例封装，统一响应拦截和超时降级
│   └── pages/
│       ├── HomePage.tsx     # 角色选择首页
│       └── ChatPage.tsx     # 对话页面
├── vite.config.ts           # Vite 配置（端口、代理）
├── tailwind.config.js       # Tailwind 主题扩展（自定义颜色/动画）
├── postcss.config.js        # PostCSS 配置
├── tsconfig.json            # TypeScript 编译配置
├── index.html               # HTML 入口
└── package.json             # 依赖与脚本
```

---

## 页面路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | HomePage | 角色列表，点击卡片进入对话 |
| `/chat/:characterId` | ChatPage | 与指定角色的对话界面 |

---

## 核心模块说明

### 1. API 客户端 `src/api/client.ts`

Axios 实例封装：

- `baseURL: '/api/v1'` — 相对路径，由 Vite dev server proxy 转发到后端
- `timeout: 35000` — 35 秒超时（匹配后端 LLM 调用）
- **响应拦截器**：统一返回 `res.data`（即后端的 `ResponseWrapper`）
- **降级处理**：超时错误（`ECONNABORTED`）时返回兜底文案 `（角色望着河水，一时陷入沉思……）`

### 2. 类型定义 `src/types/index.ts`

```typescript
interface Character {
  id: string
  name: string
  title?: string
  era?: string
  avatar_url?: string
  tagline?: string
  tags?: string[]
  knowledge_nodes?: string[]
}

interface Session {
  session_id: string
  character_id: string
  status: string
  created_at: string
}

interface ChatMessage {
  message_id: string
  role: 'user' | 'assistant'
  content: string
  character_id?: string
  emotion_tag?: string
  created_at: string
}
```

### 3. 首页 `src/pages/HomePage.tsx`

**功能**：
- 页面加载时 `useEffect` 调用 `GET /characters` 获取角色列表
- 渲染角色卡片网格（头像 + 姓名 + 标签 + 身份）
- 点击卡片 → `navigate(/chat/${character.id})`

**UI 特点**：
- 宣纸纹理背景（`paper-texture` 类）
- 角色卡片带序号徽章、hover 上浮动画
- 淡入动画（`animate-fade-in-up`）， stagger 延迟

### 4. 对话页 `src/pages/ChatPage.tsx`

**功能**：
- 进入时 `POST /sessions` 创建新会话，获取 `session_id`
- 同时 `GET /chat/history` 拉取该会话历史消息
- 发送消息：本地先 append 用户消息 → 调 `POST /chat` → 收到回复 append 角色消息
- 自动滚动到底部
- 支持 `Enter` 发送，`Shift+Enter` 换行

**UI 特点**：
- 顶部角色信息栏（返回按钮 + 头像 + 姓名 + 在线状态）
- 消息气泡：用户右对齐（深色），角色左对齐（白色带头像）
- 时间戳显示（`HH:mm` 格式）
- 发送中状态：三点加载动画
- 空会话提示：引导用户打招呼

---

## 样式系统

### Tailwind 配置扩展

在 `tailwind.config.js` 中自定义了主题：

```javascript
colors: {
  paper: '#f7f3ee',    // 宣纸底色
  ink: '#2c2420',      // 墨色文字
  wood: '#8b6f4e',     // 木质 UI 元素
  jade: '#4a7c6f',     // 在线状态指示
}
```

### 自定义 CSS 动画（`src/index.css`）

| 动画名 | 效果 | 用途 |
|--------|------|------|
| `fade-in-up` | 从下方淡入上浮 | 页面元素入场 |
| `ink-spread` | 墨迹晕染扩散 | 消息气泡出现 |
| `pulse-glow` | 呼吸发光 | 在线状态指示 |

### 工具类

- `.paper-texture` — 宣纸纹理背景
- `.ink-border` — 墨线边框
- `.no-scrollbar` — 隐藏滚动条（移动端优化）

---

## 开发启动

```bash
cd /Users/jdub/Code/2026-Dayunhe-Agent/Dayunhe-Agent

# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev

# 3. 验证
open http://localhost:5173
```

**注意**：前端开发服务器默认代理 `/api` 到 `http://localhost:8000`，因此需**同时启动后端**才能完整测试对话功能。

---

## 构建与部署

```bash
npm run build
```

构建产物输出到 `dist/` 目录。生产部署时：

1. 修改 `vite.config.ts` 中的 `proxy` 配置，或在前端 `.env` 中设置 `VITE_API_BASE`
2. 配置 Nginx 反向代理 `/api` 到后端服务
3. 静态文件由 Nginx 直接托管

---

## 后续扩展方向

| 功能 | 建议修改位置 | 说明 |
|------|-------------|------|
| 角色详情页 | 新增 `CharacterDetailPage.tsx` | 点击角色卡片先展示背景故事，再进入对话 |
| 会话列表 | 新增 `SessionsPage.tsx` | 展示历史会话，支持继续对话 |
| 消息已读/未读 | `ChatPage.tsx` + WebSocket | 实时显示对方输入状态 |
| 语音输入 | `ChatPage.tsx` 输入区 | 集成 Web Speech API |
| 分享功能 | `ChatPage.tsx` | 生成对话截图或分享链接 |
| PWA 支持 | `vite.config.ts` + manifest | 添加 Service Worker，支持离线访问 |
| 主题切换 | `index.css` + Tailwind dark mode | 支持暗黑/明亮主题 |

---

## 常见问题

**Q：前端页面空白，控制台报错？**
A：检查后端是否已启动（`localhost:8000`），以及 `vite.config.ts` 中的 `proxy` 配置是否正确。

**Q：修改样式后没有生效？**
A：Tailwind 使用 JIT 模式，确保类名写完整。若仍无效，尝试重启 `npm run dev`。

**Q：对话消息发送后没有回复？**
A：检查浏览器 Network 面板，确认 `POST /chat` 请求是否成功。若返回 401，说明后端 `.env` 中 `DASHSCOPE_API_KEY` 未配置或已过期。

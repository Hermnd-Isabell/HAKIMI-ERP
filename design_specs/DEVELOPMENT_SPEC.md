# HAKIMI ERP 团队开发规范与技术方案 (Development Specification)

> **版本：** 1.0  
> **日期：** 2026-07-28  
> **适用对象：** 全体开发成员

---

## 1. 技术栈与版本要求 (Tech Stack)

为了确保环境一致性，所有成员必须安装以下指定版本的软件：

### 1.1 后端 (Backend)
*   **语言：** Python 3.12+
*   **数据库：** MySQL 8.0+ (字符集建议使用 `utf8mb4`)
*   **核心框架建议：** FastAPI 或 Flask (基于 API 规范的高性能选型)
*   **依赖管理：** `pip` + `requirements.txt` (必须使用虚拟环境 `venv`)

### 1.2 前端 (Frontend)
*   **框架：** Vue 3 (Composition API)
*   **构建工具：** Vite
*   **UI 组件库建议：** Element Plus (适合 ERP 高密度表单)
*   **包管理：** `npm` 或 `pnpm`

### 1.3 基础设施
*   **Git：** 2.x+
*   **API 调试：** Postman 或 Bruno (导入 `refer_docs` 中的 API 契约)

---

## 2. Git 分支管理策略 (Git Workflow)

根据项目要求，采用四分支协同模式，**严格禁止在主分支直接提交代码**。

### 2.1 分支结构
1.  **`main` (生产分支)：** 
    *   仅存放经过完整测试、可发布的代码。
    *   **红线：** 严禁任何直接改动，仅接收来自 `dev` 的合并请求。
2.  **`dev` (集成分支)：**
    *   各模块代码的中转站。
    *   用于前端和后端的联调测试。
3.  **`frontend` (前端基础分支)：**
    *   所有前端功能开发的基座。
4.  **`backend` (后端基础分支)：**
    *   所有后端逻辑与数据库变更的基座。

### 2.2 开发流程
1.  **从 `frontend` 或 `backend` 检出功能分支：** `git checkout -b feature/login`
2.  **本地开发与提交：** 遵循 `CORE_PRINCIPLES.md` 的规范。
3.  **推送到远程：** `git push origin feature/login`
4.  **发起 PR (Pull Request)：** 将功能分支合并回对应的基础分支 (`frontend`/`backend`)。
5.  **定期同步：** 基础分支稳定后，合并至 `dev` 进行跨端联调。

---

## 3. 环境连接与上传指南 (Setup & Upload)

### 3.1 仓库初始化与上传
如果你是第一次克隆项目：
```bash
git clone https://github.com/BluesOctopus/HAKIMI-ERP.git
cd erp-sep-hakimi
git checkout -b dev origin/main  # 创建并切换到本地 dev 分支
```

**上传代码步骤：**
```bash
git add .
git commit -m "feat: [模块名] 简要描述变更内容"
git push origin [你的分支名]
```

### 3.2 数据库连接配置
*   后端应在项目根目录创建 `.env` 文件（严禁上传至 Git）：
    ```env
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=你的密码
    DB_NAME=hakimi_erp
    ```
*   数据库初始化脚本请存放在 `database/` 目录下，并以 `01_schema.sql`, `02_data.sql` 命名。

---

## 4. 目录结构规范 (Project Structure)

```text
HAKIMI-ERP/
├── backend/            # Python 3.12 后端源码
│   ├── app/            # 核心逻辑
│   ├── database/       # SQL 脚本与迁移
│   ├── .env.example    # 环境变量模板
│   └── requirements.txt
├── frontend/           # Vue 3 前端源码
│   ├── src/
│   │   ├── api/        # 对接后端 API
│   │   ├── components/ # 公共组件
│   │   └── views/      # 业务页面
│   └── package.json
├── refer_docs/         # 原始设计文档 (只读)
├── CORE_PRINCIPLES.md  # 核心原则 (最高优先级)
└── DEVELOPMENT_SPEC.md # 本开发规范
```

---

## 5. 多人协作红线 (Collaboration Rules)

1.  **代码审查 (Code Review)：** 任何进入 `dev` 分支的代码必须经过至少一名其他成员的 Review。
2.  **Commit 信息：** 必须包含前缀（`feat:`, `fix:`, `docs:`, `refactor:`）。
3.  **依赖同步：** 后端新增包后必须运行 `pip freeze > requirements.txt`；前端新增包后必须提交 `package-lock.json` 或 `pnpm-lock.yaml`。
4.  **接口兼容：** 若后端修改字段名，必须确保前端分支同步修改，否则严禁合并至 `dev`。

---

**“规范的目的是为了让我们可以像一个人一样编写代码。”**

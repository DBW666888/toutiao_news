# 新闻资讯 (Toutiao News)

基于 **FastAPI + Vue 3** 的全栈新闻资讯平台，提供新闻浏览、分类检索、收藏管理、浏览历史、AI 智能问答等功能。

---

## 技术栈

### 后端

| 技术 | 说明 |
|------|------|
| **Python 3.9+** | 编程语言 |
| **FastAPI** | Web 框架 |
| **SQLAlchemy 2.0（异步）** | ORM 框架 |
| **MySQL 8.0+** | 关系型数据库 |
| **Redis** | 缓存数据库 |
| **Alembic** | 数据库迁移管理 |
| **PyJWT / UUID Token** | 用户认证 |
| **Passlib (bcrypt)** | 密码加密 |
| **aiomysql** | MySQL 异步驱动 |

### 前端

| 技术 | 说明 |
|------|------|
| **Vue 3** | 前端框架 |
| **Vite** | 构建工具 |
| **Pinia** | 状态管理（持久化） |
| **Vue Router 4** | 前端路由 |
| **Vant 4** | 移动端 UI 组件库 |
| **Axios** | HTTP 请求库 |
| **vue-i18n** | 国际化（中/英） |
| **marked + DOMPurify** | Markdown 渲染 |

---

## 项目结构

```
toutiao_backend/
├── main.py                       # FastAPI 应用入口
├── config/
│   ├── db_conf.py                # 数据库连接配置
│   └── cache_conf.py             # Redis 缓存配置
├── models/
│   ├── users.py                  # 用户 & 令牌 ORM 模型
│   ├── news.py                   # 新闻 & 分类 ORM 模型
│   ├── favorite.py               # 收藏 ORM 模型
│   └── history.py                # 浏览历史 ORM 模型
├── schemas/
│   ├── base.py                   # Pydantic 基础模型
│   ├── users.py                  # 用户请求/响应模型
│   ├── favorite.py               # 收藏请求/响应模型
│   └── history.py                # 历史请求/响应模型
├── crud/
│   ├── users.py                  # 用户数据库操作
│   ├── news.py                   # 新闻数据库操作
│   ├── favorite.py               # 收藏数据库操作
│   └── history.py                # 历史数据库操作
├── routers/
│   ├── users.py                  # 用户认证接口
│   ├── news.py                   # 新闻资讯接口
│   ├── favorite.py               # 收藏功能接口
│   └── history.py                # 浏览历史接口
├── utils/
│   ├── auth.py                   # 用户认证依赖
│   ├── security.py               # 密码加密/验证
│   ├── response.py               # 统一响应格式
│   ├── exception.py              # 异常处理器实现
│   └── exception_handlers.py     # 全局异常注册
├── cache/
│   └── news_cache.py             # 新闻缓存管理
└── xwzx-news/                    # 前端项目（Vue 3 + Vite）
    ├── src/
    │   ├── views/                # 页面视图
    │   ├── router/               # 路由配置
    │   ├── store/                # Pinia 状态管理
    │   ├── components/           # 公共组件
    │   ├── i18n/                 # 国际化配置
    │   └── config/               # API 配置
    └── package.json
```

---

## 功能特性

- **用户系统**：注册、登录、个人信息管理、密码修改
- **新闻浏览**：分类展示、列表分页、新闻详情
- **收藏管理**：添加/取消收藏、收藏列表、清空收藏
- **浏览历史**：自动记录、历史列表、删除/清空
- **AI 问答**：基于 Markdown 渲染的智能对话
- **多语言支持**：中文 / English 切换
- **响应式设计**：适配移动端的 Vant UI
- **数据缓存**：Redis 缓存新闻分类、列表和详情
- **全局异常处理**：统一的异常捕获与响应格式

---

## 快速开始

### 前置要求

- Python 3.9+
- MySQL 8.0+
- Redis
- Node.js 16+（前端）

### 1. 克隆项目

```bash
git clone https://github.com/your-username/toutiao_backend.git
cd toutiao_backend
```

### 2. 后端配置

创建虚拟环境并安装依赖：

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

修改数据库配置 [config/db_conf.py](file:///e:/AI%20development/tech-selfstudy/FastAPI/toutiao_backend/config/db_conf.py)：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://root:your_password@localhost:3306/news_app?charset=utf8mb4"
```

修改 Redis 配置 [config/cache_conf.py](file:///e:/AI%20development/tech-selfstudy/FastAPI/toutiao_backend/config/cache_conf.py)（如需）：

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

初始化数据库表（使用 Alembic 或手动创建）：

> 项目使用 SQLAlchemy ORM，可参考 `models/` 下的模型定义创建对应数据库表。

启动后端服务：

```bash
uvicorn main:app --reload --port 8000
```

访问 API 文档：http://localhost:8000/docs

### 3. 前端配置

```bash
cd xwzx-news
npm install
```

修改 API 地址 [src/config/api.js](file:///e:/AI%20development/tech-selfstudy/FastAPI/toutiao_backend/xwzx-news/src/config/api.js)（如需）：

```javascript
const API_BASE_URL = 'http://localhost:8000'
```

启动开发服务器：

```bash
npm run dev
```

---

## API 接口概览

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/user/register` | 用户注册 | 否 |
| POST | `/api/user/login` | 用户登录 | 否 |
| GET | `/api/user/info` | 获取用户信息 | 是 |
| PUT | `/api/user/update` | 更新用户信息 | 是 |
| PUT | `/api/user/password` | 修改密码 | 是 |
| GET | `/api/news/categories` | 获取新闻分类 | 否 |
| GET | `/api/news/list` | 获取新闻列表 | 否 |
| GET | `/api/news/detail` | 获取新闻详情 | 否 |
| POST | `/api/favorite/add` | 添加收藏 | 是 |
| DELETE | `/api/favorite/remove` | 取消收藏 | 是 |
| GET | `/api/favorite/list` | 获取收藏列表 | 是 |
| GET | `/api/favorite/check` | 检查是否已收藏 | 是 |
| DELETE | `/api/favorite/clear` | 清空收藏 | 是 |
| POST | `/api/history/add` | 添加浏览记录 | 是 |
| DELETE | `/api/history/remove` | 删除浏览记录 | 是 |
| GET | `/api/history/list` | 获取浏览历史 | 是 |
| DELETE | `/api/history/clear` | 清空浏览历史 | 是 |

> 完整 API 文档可在启动后端后访问 `http://localhost:8000/docs` 查看 Swagger UI。

---

## 开发计划

- [x] 用户认证系统
- [x] 新闻分类与列表
- [x] 新闻详情与相关推荐
- [x] 收藏功能
- [x] 浏览历史
- [x] Redis 缓存优化
- [x] 前端国际化
- [x] AI 智能问答


---

## License

[MIT](LICENSE)


# FastAPI 学习项目

本项目记录了 FastAPI 框架的学习过程，主要分为以下三个阶段：

## first
基础功能学习阶段，涵盖了：
- **基础路由与参数**: 路径参数 (`Path`)、查询参数 (`Query`) 的使用。
- **模型验证**: 利用 Pydantic 的 `BaseModel` 和 `Field` 进行请求数据校验。
- **多种响应类型**: 实践 `HTMLResponse`、`FileResponse` 以及自定义 `response_model`。
- **错误处理**: 学习 `HTTPException` 的抛出与捕获。

## second
数据库集成学习阶段，重点在于：
- **SQLAlchemy 异步集成**: 配置 `aiomysql` 异步驱动连接 MySQL。
- **ORM 模型**: 学习声明式模型定义、自动创建表结构。
- **异步 Session 管理**: 实现数据库连接池与依赖注入 (`Depends`)。
- **复杂查询**: 实践分页查询、聚合函数 (`count`, `sum`, `avg`) 以及模糊匹配。

## third
业务逻辑进阶阶段，主要包括：
- **完整 CRUD 操作**: 深入实践数据的增、删、改、查。
- **异步事务处理**: 学习在异步环境下安全地提交和回滚事务。
- **数据一致性**: 结合 Pydantic 模型与 SQLAlchemy 模型进行数据转换与更新。

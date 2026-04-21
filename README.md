
# 招标管理系统

一个完整的招标管理系统，支持供应商管理、标书管理、应标管理、评审管理和中标管理。

## 技术栈

- **后端**: Python 3.11 + FastAPI + SQLAlchemy
- **前端**: Jinja2 模板 + HTML/CSS（内置）
- **数据库**: PostgreSQL 15
- **外部集成**: 钉钉API、邮件服务

## 项目结构

```
招标管理系统/
├── backend/              # 后端项目（内置前端）
│   ├── src/
│   │   ├── templates/    # Jinja2 模板
│   │   ├── api/routes/   # API路由
│   │   ├── services/     # 业务服务
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic Schema
│   │   ├── external/     # 外部集成
│   │   ├── utils/        # 工具函数
│   │   ├── config/       # 配置
│   │   └── main.py       # 应用入口
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/             # 旧版前端（备用）
├── PRD.md               # 产品需求
├── TASKS.json           # 任务清单
├── TECH_DESIGN.md       # 技术设计
├── TEST_CASES.md        # 测试用例
└── README.md
```

## 功能特性

### 供应商管理
- 供应商信息录入
- 供应商评级管理
- 供应商标签管理

### 标书管理
- 标书创建和编辑
- 附件上传
- 供应商邀请
- 标书发布

### 应标管理
- 应标提交
- 文件上传
- 应标验证

### 评审管理
- 评审人员指派
- 钉钉通知
- 在线评分
- 进度追踪

### 中标管理
- 评分汇总
- 权重设置
- 结果审核
- 结果公示

## 快速开始

### 后端（内置前端）

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

启动后访问：http://127.0.0.1:8000

## API文档

启动后端后访问: http://localhost:8000/docs

## GitHub仓库

https://github.com/jeffreytanhao-eng/bidding-system

## 许可证

MIT


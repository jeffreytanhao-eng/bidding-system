# 技术设计文档

## 1. 技术栈

### 1.1 技术选型
| 层级 | 技术选择 | 选择理由 |
|------|----------|----------|
| 前端 | React 18 + TypeScript + Ant Design | 企业级UI组件库，开发效率高，类型安全 |
| 后端 | Python 3.11 + FastAPI | 高性能异步框架，钉钉SDK支持好，开发效率高 |
| 数据库 | PostgreSQL 15 | 关系型数据库，支持JSON字段，适合复杂业务查询 |
| 文件存储 | MinIO / 阿里云OSS | 标书、应标文件存储，支持大文件 |
| 缓存 | Redis | 会话管理、钉钉token缓存、评审进度状态 |
| 消息队列 | RabbitMQ | 邮件发送异步处理 |
| 钉钉集成 | dingtalk-sdk | 官方Python SDK，支持组织架构、消息推送 |
| 邮件服务 | SMTP (企业邮箱) | 标书发布、中标通知 |
| 部署 | Docker + Kubernetes | 容器化部署，便于扩展 |

### 1.2 版本要求
- Python: >= 3.11
- Node.js: >= 18.x
- PostgreSQL: >= 15
- Redis: >= 7.0

## 2. 系统架构

### 2.1 架构图
```
┌─────────────────────────────────────────────────────────────────────┐
│                         前端层 (React SPA)                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │供应商管理│ │ 标书管理 │ │ 应标管理 │ │ 评审中心 │ │ 中标管理 │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ HTTPS / REST API
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API网关层 (Nginx)                            │
│                      负载均衡 + SSL终结                             │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API层 (FastAPI)                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │ 供应商路由   │ │ 标书路由    │ │ 应标路由    │ │ 评审路由    │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                  │
│  │ 中标路由    │ │ 钉钉路由    │ │ 系统路由    │                  │
│  └─────────────┘ └─────────────┘ └─────────────┘                  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         服务层 (Business Logic)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │ 供应商服务   │ │ 标书服务    │ │ 应标服务    │ │ 评审服务    │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                  │
│  │ 中标服务    │ │ 钉钉服务    │ │ 邮件服务    │                  │
│  └─────────────┘ └─────────────┘ └─────────────┘                  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         数据层                                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │ PostgreSQL  │ │   Redis     │ │   MinIO     │ │  RabbitMQ   │  │
│  │ (主数据库)  │ │ (缓存/会话) │ │ (文件存储)  │ │ (消息队列)  │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

外部集成：
┌─────────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────┐     ┌─────────────────────┐               │
│  │   钉钉开放平台       │     │    企业邮箱SMTP     │               │
│  │ - 组织架构同步       │     │ - 标书发布通知      │               │
│  │ - 消息推送           │     │ - 中标通知         │               │
│  └─────────────────────┘     └─────────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 模块划分
| 模块名 | 职责 | 依赖模块 |
|--------|------|----------|
| api/routes | API路由定义 | services |
| services | 业务逻辑处理 | models, utils, external |
| models | 数据模型定义（SQLAlchemy ORM） | - |
| schemas | Pydantic数据校验模型 | - |
| utils | 工具函数（文件处理、日志等） | - |
| external | 外部集成（钉钉、邮件） | - |
| config | 配置管理 | - |

## 3. API设计

### 3.1 接口列表

#### 供应商管理API
| 接口ID | 方法 | 路径 | 功能描述 | 对应功能ID |
|--------|------|------|----------|-----------|
| API001 | POST | /api/suppliers | 创建供应商 | F001 |
| API002 | PUT | /api/suppliers/{id} | 更新供应商信息 | F002 |
| API003 | GET | /api/suppliers | 获取供应商列表 | F006 |
| API004 | GET | /api/suppliers/{id} | 获取供应商详情 | F006 |
| API005 | POST | /api/suppliers/{id}/tags | 添加供应商标签 | F003 |
| API006 | DELETE | /api/suppliers/{id}/tags/{tag_id} | 删除供应商标签 | F003 |
| API007 | PUT | /api/suppliers/{id}/rating | 更新供应商评级 | F004 |
| API008 | POST | /api/suppliers/{id}/cooperations | 添加合作记录 | F005 |
| API009 | GET | /api/suppliers/export | 导出供应商 | F007 |
| API010 | POST | /api/suppliers/import | 导入供应商 | F007 |

#### 标书管理API
| 接口ID | 方法 | 路径 | 功能描述 | 对应功能ID |
|--------|------|------|----------|-----------|
| API011 | POST | /api/tenders | 创建标书 | F008 |
| API012 | PUT | /api/tenders/{id} | 更新标书 | F009 |
| API013 | GET | /api/tenders | 获取标书列表 | F013 |
| API014 | GET | /api/tenders/{id} | 获取标书详情 | F013 |
| API015 | POST | /api/tenders/{id}/attachments | 上传标书附件 | F010 |
| API016 | DELETE | /api/tenders/{id}/attachments/{att_id} | 删除标书附件 | F010 |
| API017 | POST | /api/tenders/{id}/invitees | 选择邀请供应商 | F011 |
| API018 | POST | /api/tenders/{id}/publish | 发布标书（发送邮件） | F012 |

#### 应标管理API
| 接口ID | 方法 | 路径 | 功能描述 | 对应功能ID |
|--------|------|------|----------|-----------|
| API019 | GET | /api/bids/submit/{token} | 获取应标入口（供应商端） | F014 |
| API020 | POST | /api/bids | 提交应标 | F015, F016 |
| API021 | GET | /api/tenders/{id}/bids | 获取应标列表 | F017 |
| API022 | GET | /api/bids/{id} | 获取应标详情 | F017 |

#### 评审管理API
| 接口ID | 方法 | 路径 | 功能描述 | 对应功能ID |
|--------|------|------|----------|-----------|
| API023 | POST | /api/dingtalk/sync | 同步钉钉组织架构 | F019 |
| API024 | GET | /api/dingtalk/departments | 获取钉钉部门列表 | F019 |
| API025 | GET | /api/dingtalk/users | 获取钉钉用户列表 | F019 |
| API026 | POST | /api/tenders/{id}/reviewers | 指派评审人员 | F020 |
| API027 | POST | /api/tenders/{id}/start-review | 启动评审 | F021 |
| API028 | GET | /api/reviews/my | 获取我的评审任务 | F021 |
| API029 | POST | /api/reviews/{id}/score | 提交评审评分 | F022, F023 |
| API030 | GET | /api/tenders/{id}/review-progress | 获取评审进度 | F025 |
| API031 | POST | /api/tenders/{id}/remind | 催办评审 | F026 |

#### 中标管理API
| 接口ID | 方法 | 路径 | 功能描述 | 对应功能ID |
|--------|------|------|----------|-----------|
| API032 | POST | /api/tenders/{id}/summary | 汇总评分 | F027 |
| API033 | PUT | /api/tenders/{id}/weights | 设置评分权重 | F028 |
| API034 | GET | /api/tenders/{id}/recommendation | 获取推荐名单 | F029 |
| API035 | POST | /api/tenders/{id}/approve | 审核中标 | F030 |
| API036 | POST | /api/tenders/{id}/announce | 公示中标 | F031 |

#### 系统管理API
| 接口ID | 方法 | 路径 | 功能描述 | 对应功能ID |
|--------|------|------|----------|-----------|
| API037 | POST | /api/settings/dingtalk | 配置钉钉集成 | F035 |
| API038 | POST | /api/settings/email | 配置邮件服务 | F036 |
| API039 | GET | /api/users | 获取用户列表 | F037 |
| API040 | PUT | /api/users/{id}/role | 更新用户角色 | F037 |

### 3.2 核心接口详情

#### API001: 创建供应商
```json
// Request
POST /api/suppliers
Authorization: Bearer {token}
Content-Type: application/json
{
  "name": "北京科技有限公司",
  "contact_person": "张三",
  "contact_phone": "13800138000",
  "contact_email": "zhangsan@example.com",
  "address": "北京市朝阳区xxx",
  "business_scope": "IT设备供应",
  "tags": ["IT设备", "硬件"],
  "initial_rating": "B"
}

// Response 201
{
  "code": 0,
  "data": {
    "id": "uuid-xxx",
    "name": "北京科技有限公司",
    "contact_person": "张三",
    "contact_phone": "13800138000",
    "contact_email": "zhangsan@example.com",
    "address": "北京市朝阳区xxx",
    "business_scope": "IT设备供应",
    "rating": "B",
    "tags": ["IT设备", "硬件"],
    "created_at": "2026-04-20T10:00:00Z"
  }
}
```

#### API018: 发布标书（发送邮件）
```json
// Request
POST /api/tenders/{id}/publish
Authorization: Bearer {token}
Content-Type: application/json
{
  "email_subject": "【招标通知】XX项目招标公告",
  "email_content": "尊敬的供应商...",
  "deadline": "2026-05-01T18:00:00Z"
}

// Response 200
{
  "code": 0,
  "data": {
    "tender_id": "uuid-xxx",
    "status": "published",
    "sent_count": 15,
    "failed_count": 0,
    "sent_at": "2026-04-20T10:00:00Z"
  }
}
```

#### API029: 提交评审评分
```json
// Request
POST /api/reviews/{id}/score
Authorization: Bearer {token}
Content-Type: application/json
{
  "scores": {
    "price": 85,
    "qualification": 90,
    "experience": 80,
    "service": 88
  },
  "total_score": 85.75,
  "comment": "价格合理，资质齐全，有相关项目经验",
  "recommendation": "recommend"
}

// Response 200
{
  "code": 0,
  "data": {
    "review_id": "uuid-xxx",
    "status": "completed",
    "submitted_at": "2026-04-20T10:00:00Z"
  }
}
```

#### API032: 汇总评分
```json
// Request
POST /api/tenders/{id}/summary
Authorization: Bearer {token}

// Response 200
{
  "code": 0,
  "data": {
    "tender_id": "uuid-xxx",
    "summary": [
      {
        "supplier_id": "uuid-1",
        "supplier_name": "供应商A",
        "business_score": 85.5,
        "technical_score": 90.0,
        "weighted_score": 88.2,
        "rank": 1
      },
      {
        "supplier_id": "uuid-2",
        "supplier_name": "供应商B",
        "business_score": 80.0,
        "technical_score": 85.0,
        "weighted_score": 83.0,
        "rank": 2
      }
    ],
    "weights": {
      "business": 0.4,
      "technical": 0.6
    }
  }
}
```

## 4. 数据库设计

### 4.1 表结构

#### suppliers 表（供应商）
```sql
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(50),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(100),
    address VARCHAR(500),
    business_scope TEXT,
    rating VARCHAR(1) DEFAULT 'C' CHECK (rating IN ('A', 'B', 'C', 'D')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'blacklist')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_suppliers_name ON suppliers(name);
CREATE INDEX idx_suppliers_rating ON suppliers(rating);
CREATE INDEX idx_suppliers_status ON suppliers(status);
```

#### supplier_tags 表（供应商标签）
```sql
CREATE TABLE supplier_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 供应商-标签关联表
CREATE TABLE supplier_tag_relations (
    supplier_id UUID REFERENCES suppliers(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES supplier_tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (supplier_id, tag_id)
);

CREATE INDEX idx_supplier_tags_supplier ON supplier_tag_relations(supplier_id);
```

#### supplier_cooperations 表（供应商合作记录）
```sql
CREATE TABLE supplier_cooperations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    supplier_id UUID NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
    tender_id UUID REFERENCES tenders(id),
    project_name VARCHAR(200) NOT NULL,
    contract_amount DECIMAL(15, 2),
    contract_date DATE,
    performance_rating VARCHAR(1) CHECK (performance_rating IN ('A', 'B', 'C', 'D')),
    performance_comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cooperations_supplier ON supplier_cooperations(supplier_id);
```

#### tenders 表（标书）
```sql
CREATE TABLE tenders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    requirements TEXT,
    budget DECIMAL(15, 2),
    deadline TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'reviewing', 'completed', 'cancelled')),
    business_weight DECIMAL(3, 2) DEFAULT 0.4,
    technical_weight DECIMAL(3, 2) DEFAULT 0.6,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    published_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_tenders_status ON tenders(status);
CREATE INDEX idx_tenders_deadline ON tenders(deadline);
CREATE INDEX idx_tenders_created_by ON tenders(created_by);
```

#### tender_attachments 表（标书附件）
```sql
CREATE TABLE tender_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
    filename VARCHAR(200) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_attachments_tender ON tender_attachments(tender_id);
```

#### tender_invitees 表（标书邀请供应商）
```sql
CREATE TABLE tender_invitees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
    supplier_id UUID NOT NULL REFERENCES suppliers(id),
    invite_token VARCHAR(100) UNIQUE NOT NULL,
    email_sent BOOLEAN DEFAULT FALSE,
    email_sent_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(tender_id, supplier_id)
);

CREATE INDEX idx_invitees_tender ON tender_invitees(tender_id);
CREATE INDEX idx_invitees_token ON tender_invitees(invite_token);
```

#### bids 表（应标）
```sql
CREATE TABLE bids (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
    supplier_id UUID NOT NULL REFERENCES suppliers(id),
    quote_amount DECIMAL(15, 2),
    delivery_period VARCHAR(100),
    contact_person VARCHAR(50),
    contact_phone VARCHAR(20),
    technical_summary TEXT,
    status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('submitted', 'reviewing', 'passed', 'rejected')),
    submitted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(tender_id, supplier_id)
);

CREATE INDEX idx_bids_tender ON bids(tender_id);
CREATE INDEX idx_bids_supplier ON bids(supplier_id);
```

#### bid_files 表（应标文件）
```sql
CREATE TABLE bid_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bid_id UUID NOT NULL REFERENCES bids(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('business', 'technical')),
    filename VARCHAR(200) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_bid_files_bid ON bid_files(bid_id);
CREATE INDEX idx_bid_files_type ON bid_files(type);
```

#### reviewers 表（评审人员）
```sql
CREATE TABLE reviewers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    dingtalk_user_id VARCHAR(100),
    review_type VARCHAR(20) NOT NULL CHECK (review_type IN ('business', 'technical')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'notified', 'in_progress', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(tender_id, user_id, review_type)
);

CREATE INDEX idx_reviewers_tender ON reviewers(tender_id);
CREATE INDEX idx_reviewers_user ON reviewers(user_id);
CREATE INDEX idx_reviewers_status ON reviewers(status);
```

#### review_scores 表（评审评分）
```sql
CREATE TABLE review_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reviewer_id UUID NOT NULL REFERENCES reviewers(id) ON DELETE CASCADE,
    bid_id UUID NOT NULL REFERENCES bids(id),
    price_score INTEGER CHECK (price_score BETWEEN 0 AND 100),
    qualification_score INTEGER CHECK (qualification_score BETWEEN 0 AND 100),
    experience_score INTEGER CHECK (experience_score BETWEEN 0 AND 100),
    service_score INTEGER CHECK (service_score BETWEEN 0 AND 100),
    total_score DECIMAL(5, 2),
    comment TEXT,
    recommendation VARCHAR(20) CHECK (recommendation IN ('recommend', 'neutral', 'not_recommend')),
    submitted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(reviewer_id, bid_id)
);

CREATE INDEX idx_scores_reviewer ON review_scores(reviewer_id);
CREATE INDEX idx_scores_bid ON review_scores(bid_id);
```

#### bid_results 表（中标结果）
```sql
CREATE TABLE bid_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tender_id UUID NOT NULL REFERENCES tenders(id),
    winner_bid_id UUID NOT NULL REFERENCES bids(id),
    winner_supplier_id UUID NOT NULL REFERENCES suppliers(id),
    final_score DECIMAL(5, 2) NOT NULL,
    rank INTEGER NOT NULL,
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMP,
    announced_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_results_tender ON bid_results(tender_id);
CREATE INDEX idx_results_supplier ON bid_results(winner_supplier_id);
```

#### users 表（用户）
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    dingtalk_user_id VARCHAR(100) UNIQUE,
    role VARCHAR(20) DEFAULT 'reviewer' CHECK (role IN ('admin', 'tender_manager', 'reviewer')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_dingtalk ON users(dingtalk_user_id);
```

#### system_settings 表（系统配置）
```sql
CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    description VARCHAR(200),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_by UUID REFERENCES users(id)
);

-- 初始化配置
INSERT INTO system_settings (key, value, description) VALUES
('dingtalk_app_key', '', '钉钉应用AppKey'),
('dingtalk_app_secret', '', '钉钉应用AppSecret'),
('smtp_host', '', 'SMTP服务器地址'),
('smtp_port', '587', 'SMTP端口'),
('smtp_username', '', 'SMTP用户名'),
('smtp_password', '', 'SMTP密码'),
('smtp_from', '', '发件人邮箱');
```

### 4.2 ER图
```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  suppliers  │───┐   │   tenders   │───┐   │    bids     │
└─────────────┘   │   └─────────────┘   │   └─────────────┘
      │           │         │           │         │
      │           │         │           │         │
      ▼           │         ▼           │         ▼
┌─────────────┐   │   ┌─────────────┐   │   ┌─────────────┐
│supplier_tags│   │   │tender_      │   │   │ bid_files   │
└─────────────┘   │   │invitees     │   │   └─────────────┘
      │           │   └─────────────┘   │         │
      │           │         │           │         │
      ▼           │         ▼           │         ▼
┌─────────────┐   │   ┌─────────────┐   │   ┌─────────────┐
│cooperations │   │   │ reviewers   │───┘   │review_scores│
└─────────────┘   │   └─────────────┘       └─────────────┘
                  │         │                     │
                  │         │                     │
                  ▼         ▼                     ▼
            ┌─────────────────────────────────────────┐
            │              bid_results                 │
            └─────────────────────────────────────────┘
```

## 5. 文件结构

```
bidding-system/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── suppliers.py      # API001-API010
│   │   │   │   ├── tenders.py        # API011-API018
│   │   │   │   ├── bids.py           # API019-API022
│   │   │   │   ├── reviews.py        # API023-API031
│   │   │   │   ├── results.py        # API032-API036
│   │   │   │   └── system.py         # API037-API040
│   │   │   └── deps.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── supplier_service.py
│   │   │   ├── tender_service.py
│   │   │   ├── bid_service.py
│   │   │   ├── review_service.py
│   │   │   ├── result_service.py
│   │   │   ├── dingtalk_service.py
│   │   │   └── email_service.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── supplier.py
│   │   │   ├── tender.py
│   │   │   ├── bid.py
│   │   │   ├── review.py
│   │   │   ├── result.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── supplier.py
│   │   │   ├── tender.py
│   │   │   ├── bid.py
│   │   │   ├── review.py
│   │   │   └── common.py
│   │   ├── external/
│   │   │   ├── __init__.py
│   │   │   ├── dingtalk_client.py
│   │   │   └── email_client.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── database.py
│   │   │   ├── file_storage.py
│   │   │   └── logger.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── suppliers/
│   │   │   ├── tenders/
│   │   │   ├── bids/
│   │   │   ├── reviews/
│   │   │   └── settings/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 6. 安全设计

| 安全项 | 实现方案 |
|--------|----------|
| 认证 | JWT Token + 钉钉扫码登录 |
| 授权 | 基于角色的访问控制（RBAC） |
| 密码安全 | bcrypt加密存储 |
| 文件安全 | 文件类型白名单、大小限制、病毒扫描 |
| 接口安全 | 限流、请求签名、HTTPS |
| 数据安全 | 敏感字段加密、操作日志审计 |
| SQL注入防护 | ORM参数化查询 |
| XSS防护 | 输入过滤、输出转义 |

## 7. 钉钉集成方案

### 7.1 集成功能
- 组织架构同步：定时同步部门、用户信息
- 消息推送：评审任务通知、催办提醒
- 扫码登录：用户快速登录系统

### 7.2 技术实现
```python
# dingtalk_client.py
from dingtalk.sdk import DingTalkClient

class DingTalkService:
    def __init__(self, app_key: str, app_secret: str):
        self.client = DingTalkClient(app_key, app_secret)
    
    async def sync_organization(self):
        """同步组织架构"""
        departments = await self.client.get_department_list()
        for dept in departments:
            users = await self.client.get_department_users(dept.id)
            # 保存到数据库
    
    async def send_work_notice(self, user_id: str, message: dict):
        """发送工作通知"""
        return await self.client.send_corp_message(
            agent_id=self.agent_id,
            userid_list=[user_id],
            msg=message
        )
```

## 8. 邮件服务方案

### 8.1 邮件场景
- 标书发布通知（含应标链接）
- 中标通知
- 系统通知

### 8.2 技术实现
```python
# email_client.py
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    async def send_tender_notice(self, to_emails: list, tender_info: dict):
        """发送标书通知"""
        message = MIMEMultipart()
        message['Subject'] = f"【招标通知】{tender_info['title']}"
        message['From'] = self.username
        message['To'] = ', '.join(to_emails)
        
        # 构建邮件内容（含应标链接）
        html_content = self._render_tender_template(tender_info)
        message.attach(MIMEText(html_content, 'html'))
        
        await aiosmtplib.send(
            message,
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=True
        )
```

## 9. 技术可行性说明

### 9.1 可行性评估
- 所有PRD功能均可通过上述技术方案实现
- 钉钉开放平台提供完整的API支持
- Python生态支持良好，开发效率高

### 9.2 风险点
| 风险 | 影响 | 应对方案 |
|------|------|----------|
| 钉钉API限流 | 消息推送延迟 | 实现消息队列，控制发送频率 |
| 大文件上传 | 系统性能 | 使用分片上传，限制文件大小 |
| 并发评审 | 数据一致性 | 使用Redis锁机制 |

### 9.3 待确认项
- 钉钉企业应用需要企业管理员审批
- 企业邮箱SMTP配置需要IT部门支持

## 10. 版本历史
| 版本 | 日期 | 修改内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-04-20 | 初始版本 | 开发专家Agent |

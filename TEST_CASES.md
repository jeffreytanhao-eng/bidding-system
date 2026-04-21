# 测试用例文档

## 1. 测试策略
- **测试框架**: pytest (后端) + Jest (前端)
- **覆盖率目标**: >= 80%
- **测试类型**: 单元测试 + 集成测试 + E2E测试

## 2. 功能测试用例

### F001: 供应商信息录入

#### TC-F001-01: 正常创建供应商
| 项目 | 内容 |
|------|------|
| 前置条件 | 管理员已登录 |
| 输入 | name="北京科技公司", contact_person="张三", contact_phone="13800138000" |
| 执行步骤 | POST /api/suppliers |
| 预期结果 | HTTP 201, 返回供应商ID |
| 后置验证 | 数据库存在对应记录 |

#### TC-F001-02: 创建供应商-必填字段缺失
| 项目 | 内容 |
|------|------|
| 前置条件 | 管理员已登录 |
| 输入 | contact_person="张三" (缺少name) |
| 预期结果 | HTTP 422, "供应商名称不能为空" |

### F003: 供应商标签管理

#### TC-F003-01: 添加标签
| 项目 | 内容 |
|------|------|
| 前置条件 | 供应商已存在 |
| 输入 | tag_name="IT设备" |
| 预期结果 | HTTP 200, 标签关联成功 |

#### TC-F003-02: 重复添加同一标签
| 项目 | 内容 |
|------|------|
| 前置条件 | 供应商已有"IT设备"标签 |
| 输入 | tag_name="IT设备" |
| 预期结果 | HTTP 200, 不重复添加 |

### F012: 标书发布与邮件发送

#### TC-F012-01: 正常发布标书
| 项目 | 内容 |
|------|------|
| 前置条件 | 标书已创建，已选择供应商 |
| 输入 | email_subject="招标通知", deadline="2026-05-01" |
| 预期结果 | HTTP 200, sent_count=15 |
| 后置验证 | 邮件发送队列有记录 |

#### TC-F012-02: 发布标书-未选择供应商
| 项目 | 内容 |
|------|------|
| 前置条件 | 标书已创建，未选择供应商 |
| 预期结果 | HTTP 400, "请先选择邀请供应商" |

### F019: 钉钉组织架构同步

#### TC-F019-01: 正常同步
| 项目 | 内容 |
|------|------|
| 前置条件 | 钉钉配置正确 |
| 执行步骤 | POST /api/dingtalk/sync |
| 预期结果 | HTTP 200, 返回同步的部门和用户数量 |

#### TC-F019-02: 钉钉配置错误
| 项目 | 内容 |
|------|------|
| 前置条件 | AppKey/AppSecret错误 |
| 执行步骤 | POST /api/dingtalk/sync |
| 预期结果 | HTTP 500, "钉钉API认证失败" |

### F022/F023: 评审打分

#### TC-F022-01: 商务评审打分
| 项目 | 内容 |
|------|------|
| 前置条件 | 评审人员已指派，评审已启动 |
| 输入 | price_score=85, qualification_score=90, comment="价格合理" |
| 预期结果 | HTTP 200, 保存成功 |

#### TC-F022-02: 评分超出范围
| 项目 | 内容 |
|------|------|
| 输入 | price_score=150 (超过100) |
| 预期结果 | HTTP 422, "评分范围0-100" |

### F027: 评分汇总

#### TC-F027-01: 正常汇总
| 项目 | 内容 |
|------|------|
| 前置条件 | 所有评审人员已完成评分 |
| 执行步骤 | POST /api/tenders/{id}/summary |
| 预期结果 | HTTP 200, 返回按得分排序的供应商列表 |

#### TC-F027-02: 部分评审未完成
| 项目 | 内容 |
|------|------|
| 前置条件 | 有评审人员未完成评分 |
| 执行步骤 | POST /api/tenders/{id}/summary |
| 预期结果 | HTTP 400, "存在未完成的评审" |

## 3. API集成测试

### API001-010: 供应商管理API

```python
# test_supplier_api.py

async def test_create_supplier(client, auth_header):
    """测试创建供应商"""
    response = client.post("/api/suppliers", 
        headers=auth_header,
        json={
            "name": "测试供应商",
            "contact_person": "张三",
            "contact_phone": "13800138000",
            "contact_email": "test@example.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == 0
    assert "id" in data["data"]

async def test_list_suppliers_with_filter(client, auth_header):
    """测试供应商筛选"""
    response = client.get("/api/suppliers?rating=A&tag=IT设备",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"], list)
```

### API011-018: 标书管理API

```python
# test_tender_api.py

async def test_publish_tender(client, auth_header, sample_tender, sample_suppliers):
    """测试发布标书"""
    # 先选择供应商
    client.post(f"/api/tenders/{sample_tender.id}/invitees",
        headers=auth_header,
        json={"supplier_ids": [s.id for s in sample_suppliers]}
    )
    
    # 发布
    response = client.post(f"/api/tenders/{sample_tender.id}/publish",
        headers=auth_header,
        json={
            "email_subject": "【招标通知】测试项目",
            "deadline": "2026-05-01T18:00:00Z"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["sent_count"] == len(sample_suppliers)
```

### API019-022: 应标管理API

```python
# test_bid_api.py

async def test_submit_bid_without_auth(client, sample_invitee):
    """测试供应商应标（无需登录）"""
    response = client.post("/api/bids",
        json={
            "invite_token": sample_invitee.invite_token,
            "quote_amount": 100000,
            "delivery_period": "30天",
            "contact_person": "李四",
            "contact_phone": "13900139000"
        }
    )
    assert response.status_code == 201

async def test_submit_bid_expired_deadline(client, expired_tender):
    """测试超过截止时间应标"""
    response = client.post("/api/bids",
        json={
            "invite_token": expired_tender.invite_token,
            "quote_amount": 100000
        }
    )
    assert response.status_code == 400
    assert "已超过应标截止时间" in response.json()["message"]
```

### API023-031: 评审管理API

```python
# test_review_api.py

async def test_assign_reviewers(client, auth_header, sample_tender):
    """测试指派评审人员"""
    response = client.post(f"/api/tenders/{sample_tender.id}/reviewers",
        headers=auth_header,
        json={
            "business_reviewers": ["user_id_1", "user_id_2"],
            "technical_reviewers": ["user_id_3", "user_id_4"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 4

async def test_submit_review_score(client, auth_header, sample_reviewer, sample_bid):
    """测试提交评审评分"""
    response = client.post(f"/api/reviews/{sample_reviewer.id}/score",
        headers=auth_header,
        json={
            "price_score": 85,
            "qualification_score": 90,
            "experience_score": 80,
            "service_score": 88,
            "comment": "综合评价良好",
            "recommendation": "recommend"
        }
    )
    assert response.status_code == 200
```

### API032-036: 中标管理API

```python
# test_result_api.py

async def test_calculate_summary(client, auth_header, completed_review_tender):
    """测试评分汇总"""
    response = client.post(f"/api/tenders/{completed_review_tender.id}/summary",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["summary"]) > 0
    # 验证排序
    scores = [s["weighted_score"] for s in data["data"]["summary"]]
    assert scores == sorted(scores, reverse=True)

async def test_approve_result(client, auth_header, sample_tender, winner_bid):
    """测试审核中标"""
    response = client.post(f"/api/tenders/{sample_tender.id}/approve",
        headers=auth_header,
        json={"winner_bid_id": winner_bid.id}
    )
    assert response.status_code == 200
```

## 4. 边界测试用例

| 用例ID | 场景 | 输入 | 预期结果 |
|--------|------|------|----------|
| B001 | 供应商名称过长 | name="a"*201 | 422, "名称最多200字符" |
| B002 | 手机号格式错误 | contact_phone="123" | 422, "手机号格式不正确" |
| B003 | 邮箱格式错误 | contact_email="invalid" | 422, "邮箱格式不正确" |
| B004 | 评分超出范围 | score=150 | 422, "评分范围0-100" |
| B005 | 标书截止时间已过 | deadline=过去时间 | 422, "截止时间必须晚于当前时间" |
| B006 | 权重和不等于1 | business=0.3, technical=0.5 | 422, "权重和必须等于1" |
| B007 | 空必填字段 | name="" | 422, "名称不能为空" |

## 5. 安全测试用例

| 用例ID | 场景 | 攻击方式 | 预期结果 |
|--------|------|----------|----------|
| S001 | 未授权访问 | 不带token访问/api/suppliers | 401 Unauthorized |
| S002 | 越权访问 | 普通用户访问管理员接口 | 403 Forbidden |
| S003 | SQL注入 | name="test'; DROP TABLE suppliers;--" | 请求被拒绝或转义 |
| S004 | XSS攻击 | description="<script>alert(1)</script>" | 输入被转义 |
| S005 | 应标令牌伪造 | 使用无效token应标 | 400, "无效的应标令牌" |

## 6. 性能测试用例

| 用例ID | 场景 | 并发数 | 预期响应时间 |
|--------|------|--------|--------------|
| P001 | 供应商列表查询 | 100 | < 500ms |
| P002 | 标书创建 | 50 | < 1000ms |
| P003 | 评分汇总计算 | 20 | < 2000ms |
| P004 | 邮件批量发送 | 100供应商 | < 30s |

## 7. 钉钉集成测试

```python
# test_dingtalk_integration.py

async def test_sync_organization(dingtalk_service):
    """测试组织架构同步"""
    result = await dingtalk_service.sync_organization()
    assert result["departments_synced"] > 0
    assert result["users_synced"] > 0

async def test_send_work_notice(dingtalk_service, test_user):
    """测试发送工作通知"""
    result = await dingtalk_service.send_work_notice(
        user_id=test_user.dingtalk_user_id,
        message={
            "msgtype": "text",
            "text": {"content": "您有新的评审任务"}
        }
    )
    assert result["errcode"] == 0
```

## 8. 测试数据

### 测试账号
| 类型 | 用户名 | 密码 | 角色 |
|------|--------|------|------|
| 管理员 | admin@test.com | Admin123! | admin |
| 招标负责人 | manager@test.com | Manager123! | tender_manager |
| 评审人员 | reviewer@test.com | Reviewer123! | reviewer |

### 测试供应商
```json
{
  "supplier_1": {
    "name": "测试供应商A",
    "contact_person": "张三",
    "contact_phone": "13800138001",
    "contact_email": "supplier_a@test.com",
    "rating": "A"
  },
  "supplier_2": {
    "name": "测试供应商B",
    "contact_person": "李四",
    "contact_phone": "13800138002",
    "contact_email": "supplier_b@test.com",
    "rating": "B"
  }
}
```

## 9. 版本历史
| 版本 | 日期 | 修改内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2026-04-20 | 初始版本 | 项目管理Agent |

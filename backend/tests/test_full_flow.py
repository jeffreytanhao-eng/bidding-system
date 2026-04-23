import requests
import json
import sys
import io
from datetime import datetime, timedelta
from uuid import uuid4

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:8000/api/v1"
UPLOAD_URL = "http://localhost:8000/api/tenders/upload"

passed = 0
failed = 0
errors = []

# 健康检查
try:
    r = requests.get("http://localhost:8000/health", timeout=5)
    if r.status_code != 200:
        print("服务器未运行，请先启动服务器")
        sys.exit(1)
except Exception:
    print("服务器未运行，请先启动服务器")
    sys.exit(1)

# 生成唯一编号
run_id = datetime.now().strftime("%Y%m%d%H%M%S")


def log_test(name, success, detail=""):
    global passed, failed
    if success:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        errors.append(f"{name}: {detail}")
        print(f"  ❌ {name} - {detail}")


def api_call(method, url, data=None, expected_status=200):
    try:
        if method == "GET":
            r = requests.get(url, timeout=10)
        elif method == "POST":
            r = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            r = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            r = requests.delete(url, timeout=10)
        else:
            return None, f"Unsupported method: {method}"

        if r.status_code != expected_status:
            try:
                detail = r.json().get("detail", r.text[:200])
            except Exception:
                detail = r.text[:200]
            return None, f"Status {r.status_code} (expected {expected_status}): {detail}"

        try:
            return r.json(), None
        except Exception:
            return r.text, None
    except Exception as e:
        return None, str(e)


print("=" * 60)
print("招标管理系统 - 全流程集成测试")
print("=" * 60)

# ============================================================
# 阶段1: 创建供应商
# ============================================================
print("\n📌 阶段1: 创建供应商")

suppliers_data = [
    {
        "name": "华建科技有限公司",
        "contact_person": "张明",
        "contact_phone": "13800001111",
        "contact_email": "zhangming@huajian.com",
        "address": "北京市朝阳区建国路88号",
        "business_scope": "建筑工程,装修装饰"
    },
    {
        "name": "鼎盛电子科技公司",
        "contact_person": "李红",
        "contact_phone": "13800002222",
        "contact_email": "lihong@dingsheng.com",
        "address": "上海市浦东新区张江路100号",
        "business_scope": "电子设备,智能化系统"
    },
    {
        "name": "绿洲环保工程公司",
        "contact_person": "王强",
        "contact_phone": "13800003333",
        "contact_email": "wangqiang@lvzhou.com",
        "address": "广州市天河区天河路200号",
        "business_scope": "环保工程,水处理"
    }
]

supplier_ids = []
for i, s_data in enumerate(suppliers_data):
    resp, err = api_call("POST", f"{BASE_URL}/suppliers", s_data)
    log_test(f"创建供应商: {s_data['name']}", err is None, err)
    if resp and resp.get("data"):
        sid = resp["data"].get("id")
        if sid:
            supplier_ids.append(sid)

log_test("成功创建3个供应商", len(supplier_ids) == 3, f"实际创建: {len(supplier_ids)}")

# 查询供应商列表
resp, err = api_call("GET", f"{BASE_URL}/suppliers")
log_test("查询供应商列表", err is None, err)
if resp and resp.get("data"):
    log_test("供应商列表数量>=3", len(resp["data"]) >= 3, f"实际: {len(resp['data'])}")

# 更新供应商评级
if supplier_ids:
    resp, err = api_call("PUT", f"{BASE_URL}/suppliers/{supplier_ids[0]}/rating?rating=A")
    log_test("更新供应商评级为A", err is None, err)

# ============================================================
# 阶段2: 上传标书文件 + 创建标书
# ============================================================
print("\n📌 阶段2: 上传标书文件 & 创建标书")

tender_content = f"""
项目编号：ZB-{run_id}-001
项目名称：智慧办公大楼装修改造工程采购项目
预算金额：2,800,000.00元
投标截止时间：2026-06-30 14:00
采购方式：公开招标

一、项目概况
本项目为智慧办公大楼装修改造工程，位于某某市某某区，建筑面积约8000平方米。
主要施工内容包括室内装修、水电改造、空调系统安装、智能化系统部署等。
工程要求在6个月内完成，质量标准达到国家现行规范要求。

二、投标人资格要求
1. 具有独立法人资格
2. 具有建筑装修装饰工程专业承包二级及以上资质
3. 近三年内有不少于3个类似项目业绩
"""

try:
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(tender_content)
        tmp_path = f.name

    with open(tmp_path, 'rb') as f:
        r = requests.post(UPLOAD_URL, files={'file': ('test_tender.txt', f, 'text/plain')}, timeout=10)

    os.unlink(tmp_path)

    upload_ok = r.status_code == 200
    log_test("上传标书文件", upload_ok, f"Status: {r.status_code}")

    if upload_ok:
        upload_data = r.json().get("data", {})
        log_test("提取标书编号", upload_data.get("tender_no") == f"ZB-{run_id}-001",
                 f"实际: {upload_data.get('tender_no')}")
        log_test("提取标书名称", upload_data.get("title") is not None,
                 f"实际: {upload_data.get('title')}")
        log_test("提取预算金额", upload_data.get("budget") == 2800000.0,
                 f"实际: {upload_data.get('budget')}")
        log_test("提取采购方式", upload_data.get("procurement_method") == "public_bidding",
                 f"实际: {upload_data.get('procurement_method')}")
        log_test("提取截止时间", upload_data.get("deadline") is not None,
                 f"实际: {upload_data.get('deadline')}")
        log_test("提取项目描述", upload_data.get("description") is not None,
                 f"实际: {upload_data.get('description')}")
except Exception as e:
    log_test("上传标书文件", False, str(e))

# 通过API创建标书
deadline = (datetime.now() + timedelta(days=30)).isoformat()
tender_data = {
    "tender_no": f"ZB-{run_id}-001",
    "title": "智慧办公大楼装修改造工程采购项目",
    "description": "本项目为智慧办公大楼装修改造工程，建筑面积约8000平方米",
    "budget": 2800000.00,
    "deadline": deadline,
    "procurement_method": "public_bidding",
}

resp, err = api_call("POST", f"{BASE_URL}/tenders", tender_data)
log_test("创建标书", err is None, err)

tender_id = None
if resp and resp.get("data"):
    tender_id = resp["data"].get("id")
    log_test("标书ID已生成", tender_id is not None, "ID为空")
    log_test("标书状态为draft", resp["data"].get("status") == "draft",
             f"实际: {resp['data'].get('status')}")

# 查询标书列表
resp, err = api_call("GET", f"{BASE_URL}/tenders")
log_test("查询标书列表", err is None, err)

# 查询单个标书
if tender_id:
    resp, err = api_call("GET", f"{BASE_URL}/tenders/{tender_id}")
    log_test("查询单个标书详情", err is None, err)

# ============================================================
# 阶段3: 选择邀请供应商 & 发布标书
# ============================================================
print("\n📌 阶段3: 选择邀请供应商 & 发布标书")

if tender_id and len(supplier_ids) >= 3:
    resp, err = api_call("POST", f"{BASE_URL}/tenders/{tender_id}/invitees", supplier_ids[:3])
    log_test("选择3家邀请供应商", err is None, err)

    invite_tokens = []
    if resp and resp.get("data"):
        for inv in resp["data"]:
            token = inv.get("invite_token")
            if token:
                invite_tokens.append(token)
        log_test("获取邀请令牌", len(invite_tokens) == 3, f"实际: {len(invite_tokens)}")
else:
    invite_tokens = []
    log_test("选择邀请供应商", False, "缺少tender_id或supplier_ids")

# ============================================================
# 阶段4: 供应商应标
# ============================================================
print("\n📌 阶段4: 供应商应标")

bid_ids = []
bid_quotes = [2500000.00, 2650000.00, 2720000.00]
for i, token in enumerate(invite_tokens):
    bid_data = {
        "invite_token": token,
        "quote_amount": bid_quotes[i],
        "delivery_period": f"{5 + i}个月",
        "contact_person": suppliers_data[i]["contact_person"],
        "contact_phone": suppliers_data[i]["contact_phone"],
        "technical_summary": f"供应商{i+1}技术方案：采用先进工艺，确保质量达标，工期合理。"
    }
    resp, err = api_call("POST", f"{BASE_URL}/bids", bid_data)
    log_test(f"供应商{i+1}提交应标 (报价: ¥{bid_quotes[i]:,.0f})", err is None, err)
    if resp and resp.get("data"):
        bid_id = resp["data"].get("id")
        if bid_id:
            bid_ids.append(bid_id)

log_test("3家供应商全部应标", len(bid_ids) == 3, f"实际: {len(bid_ids)}")

# 查询标书下的应标列表
if tender_id:
    resp, err = api_call("GET", f"{BASE_URL}/bids/tender/{tender_id}")
    log_test("查询标书应标列表", err is None, err)
    if resp and resp.get("data"):
        log_test("应标数量为3", len(resp["data"]) == 3, f"实际: {len(resp['data'])}")

# ============================================================
# 阶段5: 指派评审人员 & 评审
# ============================================================
print("\n📌 阶段5: 指派评审人员 & 评审")

reviewer_ids = []
reviewer_user_ids = []

# 先创建评审用户
for i in range(2):
    user_data = {
        "username": f"reviewer_{run_id}_{i+1}",
        "email": f"reviewer_{run_id}_{i+1}@company.com",
        "phone": f"139{run_id}{i+1}",
        "role": "reviewer"
    }
    resp, err = api_call("POST", f"{BASE_URL}/users", user_data)
    log_test(f"创建评审用户: {user_data['username']}", err is None, err)
    if resp and resp.get("data"):
        uid = resp["data"].get("id")
        if uid:
            reviewer_user_ids.append(uid)

log_test("成功创建2名评审用户", len(reviewer_user_ids) == 2, f"实际: {len(reviewer_user_ids)}")

if tender_id and len(reviewer_user_ids) >= 2:
    reviewers_payload = [
        {"user_id": reviewer_user_ids[0], "review_type": "business"},
        {"user_id": reviewer_user_ids[1], "review_type": "technical"},
    ]

    resp, err = api_call("POST", f"{BASE_URL}/tender/{tender_id}/reviewers", reviewers_payload)
    log_test("指派2名评审人员", err is None, err)

    if resp and resp.get("data"):
        for r in resp["data"]:
            rid = r.get("id")
            if rid:
                reviewer_ids.append(rid)
        log_test("获取评审人员ID", len(reviewer_ids) == 2, f"实际: {len(reviewer_ids)}")

    # 提交评分 - 每个评审人员对每个应标评分
    print("\n  📝 评审人员评分中...")
    for r_idx, reviewer_id in enumerate(reviewer_ids):
        for b_idx, bid_id in enumerate(bid_ids):
            base_price = 75 + r_idx * 5 + b_idx * 3
            base_qual = 80 + r_idx * 3 - b_idx * 2
            base_exp = 78 + b_idx * 4 - r_idx * 2
            base_svc = 82 + r_idx * 2 + b_idx * 1

            score_data = {
                "price_score": min(base_price, 100),
                "qualification_score": min(base_qual, 100),
                "experience_score": min(base_exp, 100),
                "service_score": min(base_svc, 100),
                "comment": f"评审{r_idx+1}对应标{b_idx+1}的评审意见",
                "recommendation": "recommend" if b_idx == 0 else "neutral"
            }

            resp, err = api_call("POST",
                                 f"{BASE_URL}/{reviewer_id}/score?bid_id={bid_id}",
                                 score_data)
            log_test(f"评审{r_idx+1}对应标{b_idx+1}评分", err is None, err)

    # 查询评审进度
    resp, err = api_call("GET", f"{BASE_URL}/tender/{tender_id}/progress")
    log_test("查询评审进度", err is None, err)

# ============================================================
# 阶段6: 计算评分汇总 & 中标
# ============================================================
print("\n📌 阶段6: 评分汇总 & 中标审批")

if tender_id:
    # 设置权重
    resp, err = api_call("PUT",
                         f"{BASE_URL}/tender/{tender_id}/weights?business_weight=0.4&technical_weight=0.6")
    log_test("设置评审权重(商务0.4/技术0.6)", err is None, err)

    # 计算评分汇总
    resp, err = api_call("POST", f"{BASE_URL}/tender/{tender_id}/summary")
    log_test("计算评分汇总", err is None, err)

    summary_data = None
    if resp and resp.get("data"):
        summary_data = resp["data"]
        if isinstance(summary_data, dict) and "summary" in summary_data:
            summary_data = summary_data["summary"]

        if isinstance(summary_data, list) and len(summary_data) > 0:
            winner = summary_data[0]
            log_test(f"推荐中标: {winner.get('supplier_name', 'N/A')} (加权分: {winner.get('weighted_score', 0):.2f})",
                     True)

            # 审批中标
            winner_bid_id = winner.get("bid_id")
            if winner_bid_id:
                approver_id = str(uuid4())
                resp, err = api_call("POST",
                                     f"{BASE_URL}/tender/{tender_id}/approve?winner_bid_id={winner_bid_id}&approver_id={approver_id}")
                log_test("审批中标结果", err is None, err)

                # 公告中标
                resp, err = api_call("POST", f"{BASE_URL}/tender/{tender_id}/announce")
                log_test("公告中标结果", err is None, err)

                # 验证标书状态
                resp, err = api_call("GET", f"{BASE_URL}/tenders/{tender_id}")
                if resp and resp.get("data"):
                    final_status = resp["data"].get("status")
                    log_test("标书最终状态为completed", final_status == "completed",
                             f"实际: {final_status}")
        else:
            log_test("评分汇总数据", False, f"数据格式异常: {type(summary_data)}")

# ============================================================
# 阶段7: 数据一致性验证
# ============================================================
print("\n📌 阶段7: 数据一致性验证")

resp, err = api_call("GET", f"{BASE_URL}/suppliers")
if resp and resp.get("data"):
    log_test("供应商总数>=3", len(resp["data"]) >= 3, f"实际: {len(resp['data'])}")

resp, err = api_call("GET", f"{BASE_URL}/tenders")
if resp and resp.get("data"):
    log_test("标书总数>=1", len(resp["data"]) >= 1, f"实际: {len(resp['data'])}")

if tender_id:
    resp, err = api_call("GET", f"{BASE_URL}/bids/tender/{tender_id}")
    if resp and resp.get("data"):
        log_test("应标总数=3", len(resp["data"]) == 3, f"实际: {len(resp['data'])}")

# ============================================================
# 测试结果汇总
# ============================================================
print("\n" + "=" * 60)
print(f"测试结果: ✅ 通过 {passed}  ❌ 失败 {failed}  总计 {passed + failed}")
print("=" * 60)

if errors:
    print("\n失败详情:")
    for e in errors:
        print(f"  - {e}")

sys.exit(1 if failed > 0 else 0)

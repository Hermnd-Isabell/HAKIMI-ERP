# HAKIMI-ERP 页面 × SQL 语句清单

> 依据：《系统设计报告》第4章（4.1–4.9 共 9 个页面）×《第二阶段-逻辑模型设计报告》第6章数据字典（20 张表）。
> SQL 均为 **MySQL 8.0** 语法；表名使用实际数据库中的 snake_case（与 `01_init.sql` 一致），`:参数` 表示前端/后端传入的绑定变量。
>
> 注意：逻辑模型报告中的字段与 `01_init.sql` 有少量差异（如 `personal_phoneNum` → 实际为 `personal_phone`），以下一律以已建库的实际字段名为准。

---

## 4.1 首页（Home / Welcome Page）

**用途**：驾驶舱指标卡片。页面本身没有录入，只有若干聚合统计查询（指标卡数字）。按"未清应收 / 逾期 / 在途交货 / 本月订单"四类核心指标编写：

```sql
-- 卡片1：未清应收总额与笔数
SELECT COUNT(*) AS open_ar_count,
       SUM(receivable_amount - received_amount) AS total_unpaid
FROM open_account_receivable
WHERE status = 'ACTIVE';

-- 卡片2：逾期应收（到期日已过且未收清）
SELECT COUNT(*) AS overdue_count,
       SUM(receivable_amount - received_amount) AS overdue_amount
FROM open_account_receivable
WHERE due_date < CURDATE()
  AND receivable_amount > received_amount;

-- 卡片3：在途/执行中交货单数量（对应里程碑 Picking/Shipped/In Transit）
SELECT COUNT(*) AS active_delivery_count
FROM delivery
WHERE delivery_status IN ('PICKING', 'SHIPPED', 'IN_TRANSIT');

-- 卡片4：本月新增销售订单数与净值合计
SELECT COUNT(*) AS month_order_count,
       COALESCE(SUM(net_value), 0) AS month_net_value
FROM sales_order
WHERE created_time >= DATE_FORMAT(CURDATE(), '%Y-%m-01');
```

> 指标卡片点击跳转对应模块，无额外 SQL。

---

## 4.2 创建业务伙伴（Create Business Partner）

**对应实体**：BusinessPartner、Contact、BPRelationship（P1.1 / P1.2 / P1.3）

### ① 保存前——自动生成 BP 编号（页面显示 Auto-generated）
```sql
SELECT LPAD(COALESCE(MAX(CAST(bp_id AS UNSIGNED)), 0) + 1, 6, '0') AS next_bp_id
FROM business_partner;
```

### ② 保存（Save）——插入业务伙伴主记录（Address Tab 各区块字段）
```sql
INSERT INTO business_partner
  (bp_id, bp_type, bp_role, bp_name, search_term,
   street, house_number, country, city, district, postal_code,
   telephone, mobile_phone, fax, email, status)
VALUES
  (:bpId, :bpType, :bpRole, :bpName, :searchTerm,
   :street, :houseNo, :country, :city, :district, :postalCode,
   :phone, :mobile, :fax, :email, 'ACTIVE');
```

### ③ 创建联系人（P1.2）
```sql
INSERT INTO contact
  (contact_id, bp_id, contact_type, contact_role, first_name, last_name,
   department, position, personal_phone, email, status)
VALUES
  (:contactId, :bpId, :contactType, :contactRole, :firstName, :lastName,
   :department, :position, :phone, :email, 'ACTIVE');
```

### ④ 建立 BP 关系（P1.3，配合 4.7 的 F4 弹窗选择关系类别）
```sql
INSERT INTO bp_relationship
  (relation_id, relationship_type, bp_from, bp_to, valid_from, valid_to)
VALUES
  (:relationId, :relType, :bpFrom, :bpTo, :validFrom, :validTo);
```

### ⑤ 辅助查询——名称唯一性/重复校验（失焦校验用）
```sql
SELECT bp_id, bp_name FROM business_partner
WHERE bp_name = :bpName OR search_term = :searchTerm;
```

---

## 4.3 未清应收账款列表（Unpaid Accounts Receivable）

**对应实体**：Invoice、OpenAccountReceivable（D5.1、D5.4）

### ① 顶部 4 张汇总卡片
```sql
SELECT
  SUM(receivable_amount - received_amount)                              AS total_unpaid,
  COUNT(*)                                                              AS open_count,
  SUM(CASE WHEN due_date < CURDATE()
           THEN receivable_amount - received_amount ELSE 0 END)         AS overdue_amount,
  SUM(CASE WHEN received_amount > 0
           THEN received_amount ELSE 0 END)                             AS total_received
FROM open_account_receivable;
```

### ② 表格主查询（筛选：客户名 / 发票号 / 状态 / 到期日区间；分页）
```sql
SELECT
  i.invoice_id                                   AS invoice_no,
  bp.bp_name                                     AS customer_name,
  i.invoice_date,
  ar.due_date,
  ar.receivable_amount                           AS invoice_amount,
  ar.received_amount,
  (ar.receivable_amount - ar.received_amount)    AS unpaid_amount,
  CASE
    WHEN ar.received_amount >= ar.receivable_amount THEN 'Paid'
    WHEN ar.due_date < CURDATE()                    THEN 'Overdue'
    WHEN ar.received_amount > 0                     THEN 'Partially Paid'
    ELSE 'Unpaid'
  END                                            AS status,
  ROUND(ar.received_amount / ar.receivable_amount * 100, 1)
                                                 AS collection_progress
FROM open_account_receivable ar
JOIN invoice i          ON ar.invoice_id = i.invoice_id
JOIN delivery d         ON i.delivery_id = d.delivery_id
JOIN sales_order so     ON d.sales_order_id = so.sales_order_id
JOIN business_partner bp ON so.customer_id = bp.bp_id
WHERE (:customerName IS NULL OR bp.bp_name LIKE CONCAT('%', :customerName, '%'))
  AND (:invoiceNo    IS NULL OR i.invoice_id = :invoiceNo)
  AND (:startDate    IS NULL OR ar.due_date >= :startDate)
  AND (:endDate      IS NULL OR ar.due_date <= :endDate)
ORDER BY ar.due_date ASC
LIMIT :pageSize OFFSET :offset;   -- 10行/页，offset = (page-1)*pageSize

-- 分页器总数（与上面相同的 FROM/WHERE）
SELECT COUNT(*) AS total
FROM open_account_receivable ar
JOIN invoice i           ON ar.invoice_id = i.invoice_id
JOIN delivery d          ON i.delivery_id = d.delivery_id
JOIN sales_order so      ON d.sales_order_id = so.sales_order_id
JOIN business_partner bp ON so.customer_id = bp.bp_id
WHERE (:customerName IS NULL OR bp.bp_name LIKE CONCAT('%', :customerName, '%'))
  AND (:invoiceNo    IS NULL OR i.invoice_id = :invoiceNo)
  AND (:startDate    IS NULL OR ar.due_date >= :startDate)
  AND (:endDate      IS NULL OR ar.due_date <= :endDate);
```

> Auto Refresh（30s）= 前端定时重发以上查询；导出 = 去掉 LIMIT 重查一次。

---

## 4.4 交货状态监控（Delivery Status Monitoring）

**对应实体**：Delivery、DeliveryItem、GoodsIssue（D4.1、D4.2）

```sql
-- 表格主查询（筛选：交货单号/订单号/客户名/状态）
SELECT
  d.delivery_id,
  d.sales_order_id,
  bp.bp_name                                  AS customer_name,
  d.planned_delivery_date                     AS delivery_date,
  d.planned_GI_date,
  d.delivery_status                           AS status,   -- CREATING/PICKING/SHIPPED/IN_TRANSIT/COMPLETED
  d.picking_date,
  d.actual_GI_date,
  COALESCE(del.delivered_qty, 0)              AS delivered_qty,
  COALESCE(ord.total_qty, 0)                  AS total_qty     -- Delivered/Total 列
FROM delivery d
JOIN sales_order so       ON d.sales_order_id = so.sales_order_id
JOIN business_partner bp  ON so.customer_id = bp.bp_id
LEFT JOIN (
  SELECT delivery_id, SUM(delivery_quantity) AS delivered_qty
  FROM delivery_item GROUP BY delivery_id
) del ON del.delivery_id = d.delivery_id
LEFT JOIN (
  SELECT sales_order_id, SUM(order_quantity) AS total_qty
  FROM sales_order_item GROUP BY sales_order_id
) ord ON ord.sales_order_id = so.sales_order_id
WHERE (:deliveryNo IS NULL OR d.delivery_id = :deliveryNo)
  AND (:orderNo    IS NULL OR d.sales_order_id = :orderNo)
  AND (:customer   IS NULL OR bp.bp_name LIKE CONCAT('%', :customer, '%'))
  AND (:status     IS NULL OR d.delivery_status = :status)
ORDER BY d.delivery_id DESC
LIMIT :pageSize OFFSET :offset;

-- 总数（同 FROM/WHERE，略）
```

> 里程碑进度条（Created→Picked→Shipped→Completed）节点时间：分别取 `delivery` 的创建（可用 delivery_id 生成时间或后端记录）、`picking_date`、`actual_GI_date`、以及全部行项完成时间。

---

## 4.5 交货详情页（Delivery Details）

### ① 抬头 + 信息卡片 + Shipment Information
```sql
SELECT
  d.delivery_id, d.delivery_status, d.delivery_type,
  d.planned_delivery_date, d.planned_GI_date, d.actual_GI_date,
  d.picking_date, d.shipping_point,
  bp.bp_name        AS ship_to_name,
  bp.street, bp.house_number, bp.city, bp.district,
  bp.country, bp.postal_code,                        -- Ship-to Address
  c.first_name, c.last_name, c.personal_phone, c.email  -- Contact
FROM delivery d
LEFT JOIN business_partner bp ON d.ship_to_party = bp.bp_id
LEFT JOIN contact c           ON c.bp_id = bp.bp_id AND c.status = 'ACTIVE'
WHERE d.delivery_id = :deliveryId;
```

### ② Order Items 表格
```sql
SELECT
  di.item_no, di.material_id,
  m.material_name                       AS description,
  di.delivery_quantity                  AS qty,
  di.sales_unit,
  di.item_description,
  CASE WHEN gi.goods_issue_time IS NOT NULL THEN 'Shipped' ELSE 'Loading' END AS item_status
FROM delivery_item di
JOIN material m         ON di.material_id = m.material_id
LEFT JOIN goods_issue gi ON gi.delivery_item_id = di.delivery_item_id
WHERE di.delivery_id = :deliveryId
ORDER BY di.item_no;
```

### ③ 里程碑时间戳（Shipped 节点时间）
```sql
SELECT MIN(gi.goods_issue_time) AS shipped_time
FROM goods_issue gi
JOIN delivery_item di ON gi.delivery_item_id = di.delivery_item_id
WHERE di.delivery_id = :deliveryId;
```

### ④ 过账发货（PGI 操作，监控页/详情页触发）
```sql
-- 写入库明细
INSERT INTO goods_issue (goods_issue_id, delivery_item_id, goods_issue_time, actual_quantity, posting_date, warehouse)
VALUES (:giId, :deliveryItemId, NOW(), :qty, CURDATE(), :warehouse);

-- 更新交货单状态与实际发货日期（规则 DEL-04/DEL-07）
UPDATE delivery
SET delivery_status = 'SHIPPED', actual_GI_date = NOW()
WHERE delivery_id = :deliveryId
  AND delivery_status = 'READY_FOR_GI';
```

> Download POD / Print：用查询 ①② 的结果在前端生成 PDF，无额外 SQL。

---

## 4.6 应收账款详情页（Unpaid Receivable Details）

**对应实体**：Invoice、Receipt、OpenAccountReceivable（D5.1、D5.2、D5.4）

### ① 金额卡片 + 催收进度
```sql
SELECT
  i.invoice_id, i.invoice_date, i.total_amount,
  ar.receivable_amount                          AS invoice_amount,
  ar.received_amount,
  (ar.receivable_amount - ar.received_amount)   AS unpaid_amount,
  ar.due_date,
  GREATEST(DATEDIFF(CURDATE(), ar.due_date), 0) AS days_overdue,
  ROUND(ar.received_amount / ar.receivable_amount * 100, 1) AS collection_ratio
FROM open_account_receivable ar
JOIN invoice i ON ar.invoice_id = i.invoice_id
WHERE i.invoice_id = :invoiceId;
```

### ② Customer & Terms 区块（客户信息、联系人、付款条件、信用相关）
```sql
SELECT
  bp.bp_id, bp.bp_name, bp.country, bp.city, bp.street, bp.house_number,
  c.first_name, c.last_name, c.personal_phone, c.email,
  fd.payment_terms, fd.reconciliation_account
FROM invoice i
JOIN delivery d            ON i.delivery_id = d.delivery_id
JOIN sales_order so        ON d.sales_order_id = so.sales_order_id
JOIN business_partner bp   ON so.customer_id = bp.bp_id
LEFT JOIN customer_finance_data fd ON fd.bp_id = bp.bp_id
LEFT JOIN contact c        ON c.bp_id = bp.bp_id AND c.status = 'ACTIVE'
WHERE i.invoice_id = :invoiceId;
```

> 信用额度 / 风险等级字段当前 20 张表中没有，属页面占位数据；如需落库，可在 `customer_finance_data` 加 `credit_limit`、`risk_level` 两列。

### ③ Payment History 表格
```sql
SELECT receipt_date  AS date,
       payment_method AS method,
       receipt_amount AS amount,
       reference_no   AS reference
FROM receipt
WHERE invoice_id = :invoiceId
ORDER BY receipt_date DESC;
```

### ④ Collect 按钮——登记一笔收款（对应 P4.2，规则 FIN-07/FIN-08，须在同一事务中执行）
```sql
-- 1. 写收款台账
INSERT INTO receipt (receipt_id, invoice_id, receipt_date, receipt_amount, payment_method, payer, currency, reference_no)
VALUES (:receiptId, :invoiceId, NOW(), :amount, :method, :payer, :currency, :refNo);

-- 2. 累加已收金额
UPDATE open_account_receivable
SET received_amount = received_amount + :amount
WHERE invoice_id = :invoiceId;

-- 3. 全额核销（balance = 0）→ 结清迁移
INSERT INTO closed_account_receivable (closed_ar_id, invoice_id, receivable_amount, received_amount, created_time, closed_time)
SELECT LPAD(COALESCE(MAX(CAST(closed_ar_id AS UNSIGNED)),0)+1, 8, '0'),
       invoice_id, receivable_amount, received_amount, created_time, NOW()
FROM open_account_receivable
WHERE invoice_id = :invoiceId AND received_amount >= receivable_amount;

DELETE FROM open_account_receivable
WHERE invoice_id = :invoiceId AND received_amount >= receivable_amount;

-- 4. 联动更新发票状态（FIN-08）
UPDATE invoice SET status = 'CLEARED'
WHERE invoice_id = :invoiceId
  AND NOT EXISTS (SELECT 1 FROM open_account_receivable WHERE invoice_id = :invoiceId);
```

---

## 4.7 F4 搜索帮助弹窗（Relationship Category）

**对应实体**：BPRelationship（D1.3）

> 说明：关系类别字典（BBP002 等 34 个条目）属于配置数据，当前 20 张表中没有独立的关系类别表。两种做法：
> - **简单做法**（推荐小学期）：从 `bp_relationship` 取已有类别；
> - **规范做法**：新建 `relationship_category(rel_cat, direction, description)` 配置表并预置数据。

```sql
-- ① 弹窗表格：列出可选关系类别（去重）
SELECT DISTINCT relationship_type AS rel_cat FROM bp_relationship;

-- 规范做法下：
-- SELECT rel_cat, direction, description FROM relationship_category
-- WHERE (:keyword IS NULL OR description LIKE CONCAT('%', :keyword, '%'));

-- ② 底部条目计数
SELECT COUNT(DISTINCT relationship_type) AS entries_found FROM bp_relationship;

-- ③ 确认选择后回填：查某 BP 在某类别下的关系记录
SELECT relation_id, relationship_type, bp_from, bp_to, valid_from, valid_to
FROM bp_relationship
WHERE relationship_type = :relCat
  AND (bp_from = :bpId OR bp_to = :bpId);

-- ④ F4 弹窗通用形态——搜业务伙伴（其他字段的 F4 复用此模式）
SELECT bp_id, bp_name, country, city
FROM business_partner
WHERE status = 'ACTIVE'
  AND (:keyword IS NULL
       OR bp_name LIKE CONCAT('%', :keyword, '%')
       OR search_term LIKE CONCAT('%', :keyword, '%'))
LIMIT 50;
```

---

## 4.8 创建报价单行项目（Create Quotation: Item Data）

**对应实体**：Quotation、QuotationItem、Material（D3.2、D2）

### ① 打开页面——报价单抬头
```sql
SELECT quotation_id, quotation_type, status, customer_id, sales_org,
       distribution_channel, division, currency, valid_from, valid_to, net_value
FROM quotation
WHERE quotation_id = :quotationId;
```

### ② 行项目导航（< > 切换）
```sql
SELECT qi.*, m.material_name AS description, m.base_unit
FROM quotation_item qi
JOIN material m ON qi.material_id = m.material_id
WHERE qi.quotation_id = :quotationId
ORDER BY qi.item_no;
```

### ③ Material 字段输入/F4——带出物料与标准价（定价元素 PR00 来源）
```sql
SELECT material_id, material_name, base_unit, standard_price
FROM material
WHERE material_id = :materialId;
```

### ④ 新行项号自动生成（10, 20, 30…）
```sql
SELECT COALESCE(MAX(CAST(item_no AS UNSIGNED)), 0) + 10 AS next_item_no
FROM quotation_item
WHERE quotation_id = :quotationId;
```

### ⑤ Update 按钮——重算价格（Net = 单价 × (1 - 折扣)；金额 = 数量 × 净价）
```sql
UPDATE quotation_item
SET net_price            = unit_price * (1 - COALESCE(discount, 0) / 100),
    expected_order_value = order_quantity * unit_price * (1 - COALESCE(discount, 0) / 100)
WHERE quotation_item_id = :itemId;
```

### ⑥ Save——插入行项目
```sql
INSERT INTO quotation_item
  (quotation_item_id, quotation_id, material_id, item_no,
   order_quantity, sales_unit, unit_price, discount, net_price,
   expected_order_value, item_description)
VALUES
  (:itemId, :quotationId, :materialId, :itemNo,
   :qty, :unit, :unitPrice, :discount, :netPrice,
   :qty * :netPrice, :itemDesc);
```

### ⑦ 保存后回写抬头净值（金额继承，规则 GEN-01）
```sql
UPDATE quotation q
SET net_value = (
  SELECT COALESCE(SUM(expected_order_value), 0)
  FROM quotation_item
  WHERE quotation_id = q.quotation_id
)
WHERE q.quotation_id = :quotationId;
```

### ⑧ Delete Item
```sql
DELETE FROM quotation_item WHERE quotation_item_id = :itemId;
-- 删除后再执行 ⑦ 重算抬头净值
```

> **Pricing Elements 表格说明**：SAP 的定价条件矩阵（PR00/K004/SKTO/VPRS…）在当前 20 张表里没有独立的定价条件表。小学期建议：用 `quotation_item` 的 `unit_price`（PR00）、`discount`（折扣行）、`net_price`（净值行）三列模拟展示；如要完整实现，需要新增 `pricing_condition` 表（cond_type, amount, currency, per, uom, condition_value, is_active）。

---

## 4.9 成功提示弹窗（Success Modal）

**纯反馈组件，本身无 SQL**。它展示的是上一个写操作的结果（单号、凭证号）。涉及的查询只有两处：

```sql
-- ① "Display" 按钮：按刚返回的单号查刚创建的记录（以收款为例）
SELECT receipt_id, invoice_id, receipt_date, receipt_amount, payment_method, reference_no
FROM receipt
WHERE receipt_id = :newId;

-- ② 文案中的单号：直接来自写操作的返回值，例如
SELECT LPAD(COALESCE(MAX(CAST(receipt_id AS UNSIGNED)), 0) + 1, 10, '0') AS new_receipt_id
FROM receipt;
```

> "Post Next Payment" = 关闭弹窗、清空表单，回到 4.6-④ 的流程，无新 SQL。

---

## 附：页面—表对照速查

| 页面 | 读 | 写 |
|---|---|---|
| 4.1 首页 | open_account_receivable、delivery、sales_order | — |
| 4.2 创建业务伙伴 | business_partner（查重/编号） | business_partner、contact、bp_relationship |
| 4.3 未清应收列表 | open_account_receivable、invoice、delivery、sales_order、business_partner | — |
| 4.4 交货监控 | delivery、delivery_item、sales_order、sales_order_item、business_partner | — |
| 4.5 交货详情 | delivery、business_partner、contact、delivery_item、material、goods_issue | goods_issue、delivery（PGI） |
| 4.6 应收详情 | open_account_receivable、invoice、business_partner、contact、customer_finance_data、receipt | receipt、open/closed_account_receivable、invoice |
| 4.7 F4 弹窗 | bp_relationship、business_partner | — |
| 4.8 报价行项目 | quotation、quotation_item、material | quotation_item、quotation |
| 4.9 成功弹窗 | （上一步单据的回查） | — |

**两处设计缺口**（页面有、数据库没有，需和老师确认或自行扩展）：
1. 关系类别字典表（4.7 的 34 个条目）→ 建议加 `relationship_category` 配置表；
2. 定价条件表（4.8 的 Pricing Elements 矩阵）→ 建议加 `pricing_condition` 表或用行项三字段模拟；
3. 信用额度/风险等级（4.6）→ 建议在 `customer_finance_data` 加列。

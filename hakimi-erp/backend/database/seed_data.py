# -*- coding: utf-8 -*-
"""HAKIMI-ERP 测试数据批量导入脚本"""
import sys, os
# 调整路径以导入 app 模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.auth import User
from app.models.customer import BusinessPartner, CustomerSalesData, CustomerFinanceData, Contact
from app.models.material import Material
from app.models.sales import Inquiry, InquiryItem, Quotation, QuotationItem, SalesOrder, SalesOrderItem
from app.models.logistics import Delivery, DeliveryItem, GoodsIssue
from app.models.finance import Invoice, InvoiceItem, OpenAccountReceivable, Receipt
from app.services.auth_service import auth_service
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

db = SessionLocal()

try:
    # ──────────────────────────────────────────────
    # 0. Default System User
    # ──────────────────────────────────────────────
    if not db.query(User).filter(User.username == "admin").first():
        db.add(User(
            username="admin",
            email="admin@hakimi-erp.local",
            password_hash=auth_service.hash_password("admin123"),
            full_name="System Administrator",
            role="ADMIN",
            is_active=True,
        ))
        db.flush()
        print("  [OK] Default system user created (admin / admin123)")

    # ──────────────────────────────────────────────
    # 1. Business Partners (客户)
    # ──────────────────────────────────────────────
    customers = [
        {"bp_id": "BP00001", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "上海华联集团有限公司", "city": "上海", "district": "浦东新区", "street": "世纪大道", "house_number": "100号", "telephone": "021-58880001", "mobile_phone": "13800001001", "email": "contact@hualian.com", "search_term": "华联"},
        {"bp_id": "BP00002", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "北京首钢贸易有限公司", "city": "北京", "district": "朝阳区", "street": "建国路", "house_number": "88号", "telephone": "010-62220001", "mobile_phone": "13900002001", "email": "info@shougang-trade.com", "search_term": "首钢贸易"},
        {"bp_id": "BP00003", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "深圳创新科技有限公司", "city": "深圳", "district": "南山区", "street": "科技园南路", "house_number": "16号", "telephone": "0755-86660001", "mobile_phone": "13700003001", "email": "sales@innovate-sz.com", "search_term": "创新科技"},
        {"bp_id": "BP00004", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "广州卓越制造有限公司", "city": "广州", "district": "天河区", "street": "中山大道", "house_number": "200号", "telephone": "020-85550001", "mobile_phone": "13600004001", "email": "gm@zhuoyue-mfg.com", "search_term": "卓越制造"},
        {"bp_id": "BP00005", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "成都蜀锦纺织集团", "city": "成都", "district": "锦江区", "street": "蜀都大道", "house_number": "55号", "telephone": "028-87770001", "mobile_phone": "13500005001", "email": "cd@shujin-textile.com", "search_term": "蜀锦纺织"},
        {"bp_id": "BP00006", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "武汉长江物流有限公司", "city": "武汉", "district": "江岸区", "street": "沿江大道", "house_number": "120号", "telephone": "027-82220001", "mobile_phone": "13400006001", "email": "wh@changjiang-log.com", "search_term": "长江物流"},
        {"bp_id": "BP00007", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "杭州西湖电子有限公司", "city": "杭州", "district": "西湖区", "street": "文三路", "house_number": "300号", "telephone": "0571-87710001", "mobile_phone": "13300007001", "email": "hz@xihu-electronics.com", "search_term": "西湖电子"},
        {"bp_id": "BP00008", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "南京紫金化工有限公司", "city": "南京", "district": "鼓楼区", "street": "中山北路", "house_number": "45号", "telephone": "025-83330001", "mobile_phone": "13200008001", "email": "nj@zijin-chem.com", "search_term": "紫金化工"},
        {"bp_id": "BP00009", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "重庆麻辣食品有限公司", "city": "重庆", "district": "渝中区", "street": "解放碑步行街", "house_number": "8号", "telephone": "023-68880001", "mobile_phone": "13100009001", "email": "cq@mala-food.com", "search_term": "麻辣食品"},
        {"bp_id": "BP00010", "bp_type": "ORGANIZATION", "bp_role": "SOLD_TO", "bp_name": "青岛海风机械有限公司", "city": "青岛", "district": "市南区", "street": "香港中路", "house_number": "20号", "telephone": "0532-86690001", "mobile_phone": "13000010001", "email": "qd@haifeng-mach.com", "search_term": "海风机械"},
    ]

    for c in customers:
        bp = BusinessPartner(**c)
        db.add(bp)
    db.flush()
    print(f"  [OK] {len(customers)} Business Partners created")

    # ──────────────────────────────────────────────
    # 2. Customer Sales Data
    # ──────────────────────────────────────────────
    sales_orgs = [
        {"bp_id": "BP00001", "sales_org": "1000", "distribution_channel": "10", "division": "01", "currency": "CNY", "price_group": "PG01", "delivery_priority": "01", "shipping_condition": "01", "delivering_plant": "PL01", "incoterms": "FOB"},
        {"bp_id": "BP00002", "sales_org": "1000", "distribution_channel": "10", "division": "02", "currency": "CNY", "price_group": "PG02", "delivery_priority": "02", "shipping_condition": "01", "delivering_plant": "PL02", "incoterms": "CIF"},
        {"bp_id": "BP00003", "sales_org": "2000", "distribution_channel": "10", "division": "01", "currency": "CNY", "price_group": "PG01", "delivery_priority": "01", "shipping_condition": "01", "delivering_plant": "PL01", "incoterms": "FOB"},
        {"bp_id": "BP00004", "sales_org": "2000", "distribution_channel": "20", "division": "01", "currency": "CNY", "price_group": "PG03", "delivery_priority": "03", "shipping_condition": "02", "delivering_plant": "PL03", "incoterms": "EXW"},
        {"bp_id": "BP00005", "sales_org": "3000", "distribution_channel": "10", "division": "01", "currency": "CNY", "price_group": "PG01", "delivery_priority": "01", "shipping_condition": "01", "delivering_plant": "PL01", "incoterms": "FOB"},
        {"bp_id": "BP00006", "sales_org": "3000", "distribution_channel": "20", "division": "02", "currency": "CNY", "price_group": "PG02", "delivery_priority": "02", "shipping_condition": "01", "delivering_plant": "PL02", "incoterms": "CIF"},
        {"bp_id": "BP00007", "sales_org": "1000", "distribution_channel": "10", "division": "01", "currency": "CNY", "price_group": "PG01", "delivery_priority": "01", "shipping_condition": "01", "delivering_plant": "PL01", "incoterms": "FOB"},
        {"bp_id": "BP00008", "sales_org": "2000", "distribution_channel": "10", "division": "01", "currency": "CNY", "price_group": "PG01", "delivery_priority": "01", "shipping_condition": "01", "delivering_plant": "PL01", "incoterms": "FOB"},
        {"bp_id": "BP00009", "sales_org": "3000", "distribution_channel": "10", "division": "01", "currency": "CNY", "price_group": "PG01", "delivery_priority": "01", "shipping_condition": "01", "delivering_plant": "PL01", "incoterms": "FOB"},
        {"bp_id": "BP00010", "sales_org": "1000", "distribution_channel": "20", "division": "02", "currency": "CNY", "price_group": "PG02", "delivery_priority": "02", "shipping_condition": "01", "delivering_plant": "PL02", "incoterms": "CIF"},
    ]
    for s in sales_orgs:
        db.add(CustomerSalesData(**s))
    db.flush()
    print(f"  [OK] {len(sales_orgs)} Customer Sales Data created")

    # ──────────────────────────────────────────────
    # 3. Customer Finance Data
    # ──────────────────────────────────────────────
    for bp_id in [f"BP0000{i}" for i in range(1, 11)]:
        db.add(CustomerFinanceData(
            bp_id=bp_id, company_code="C100",
            reconciliation_account=f"11220{str(random.randint(1000,9999))}",
            payment_terms="NET30", bank_country="CN",
            bank_key="ICBC", bank_account=f"622202{random.randint(1000000000,9999999999)}",
            iban=f"CN{random.randint(100000000000,999999999999)}",
        ))
    db.flush()
    print(f"  [OK] 10 Customer Finance Data created")

    # ──────────────────────────────────────────────
    # 4. Contacts
    # ──────────────────────────────────────────────
    contact_names = [
        ("张", "伟", "采购部", "采购经理"), ("李", "娜", "销售部", "销售主管"),
        ("王", "强", "物流部", "物流经理"), ("赵", "敏", "财务部", "财务总监"),
        ("周", "杰", "技术部", "技术总监"), ("吴", "芳", "行政部", "行政主管"),
        ("郑", "超", "生产部", "生产经理"), ("冯", "磊", "质检部", "质检主管"),
        ("陈", "静", "市场部", "市场经理"), ("孙", "明", "采购部", "采购专员"),
    ]
    for idx, (fn, ln, dept, pos) in enumerate(contact_names):
        db.add(Contact(
            contact_id=f"CT{str(idx+1).zfill(5)}", bp_id=f"BP{str(idx+1).zfill(5)}",
            contact_type="WORK", contact_role=dept, first_name=fn, last_name=ln,
            department=dept, position=pos, personal_phone=f"138{random.randint(10000000,99999999)}",
            email=f"{fn}{ln}@company{idx+1}.com", status="ACTIVE",
        ))
    db.flush()
    print(f"  [OK] {len(contact_names)} Contacts created")

    # ──────────────────────────────────────────────
    # 5. Materials
    # ──────────────────────────────────────────────
    materials_data = [
        {"material_id": "MAT0001", "material_name": "高碳钢钢管", "description": "直径50mm×壁厚3mm，Q235B标准", "base_unit": "KG", "standard_price": Decimal("28.50"), "weight": Decimal("3.850"), "volume": Decimal("0.012"), "search_term": "钢管 高碳钢"},
        {"material_id": "MAT0002", "material_name": "不锈钢法兰", "description": "DN100 PN16 304不锈钢", "base_unit": "PC", "standard_price": Decimal("185.00"), "weight": Decimal("2.300"), "volume": Decimal("0.005"), "search_term": "法兰 不锈钢"},
        {"material_id": "MAT0003", "material_name": "工业轴承6205", "description": "深沟球轴承，内径25mm×外径52mm", "base_unit": "PC", "standard_price": Decimal("12.80"), "weight": Decimal("0.128"), "volume": Decimal("0.001"), "search_term": "轴承 6205"},
        {"material_id": "MAT0004", "material_name": "电动执行器", "description": "220V AC 扭矩50Nm，开关型", "base_unit": "SET", "standard_price": Decimal("1280.00"), "weight": Decimal("4.500"), "volume": Decimal("0.025"), "search_term": "执行器 电动"},
        {"material_id": "MAT0005", "material_name": "铜芯电缆YJV-4×16", "description": "交联聚乙烯绝缘电力电缆 4芯16平方", "base_unit": "M", "standard_price": Decimal("45.00"), "weight": Decimal("0.850"), "volume": Decimal("0.003"), "search_term": "电缆 YJV"},
        {"material_id": "MAT0006", "material_name": "环氧树脂涂料", "description": "双组份防腐涂料，灰色，20kg/桶", "base_unit": "BARREL", "standard_price": Decimal("320.00"), "weight": Decimal("22.000"), "volume": Decimal("0.030"), "search_term": "涂料 环氧"},
        {"material_id": "MAT0007", "material_name": "精密螺丝刀套装", "description": "45合1套装，铬钒钢材质", "base_unit": "SET", "standard_price": Decimal("68.00"), "weight": Decimal("0.650"), "volume": Decimal("0.002"), "search_term": "螺丝刀 套装"},
        {"material_id": "MAT0008", "material_name": "液压阀组", "description": "三位四通电磁换向阀，NG6", "base_unit": "PC", "standard_price": Decimal("520.00"), "weight": Decimal("1.800"), "volume": Decimal("0.008"), "search_term": "液压阀 电磁阀"},
        {"material_id": "MAT0009", "material_name": "铝合金散热片", "description": "100×100×25mm，自然散热", "base_unit": "PC", "standard_price": Decimal("15.00"), "weight": Decimal("0.150"), "volume": Decimal("0.002"), "search_term": "散热片 铝合金"},
        {"material_id": "MAT0010", "material_name": "光学传感器", "description": "对射型光电开关，检测距30m", "base_unit": "PC", "standard_price": Decimal("95.00"), "weight": Decimal("0.080"), "volume": Decimal("0.001"), "search_term": "传感器 光电"},
        {"material_id": "MAT0011", "material_name": "橡胶密封圈", "description": "丁腈橡胶 O型密封圈 50×3.5mm", "base_unit": "BAG", "standard_price": Decimal("2.50"), "weight": Decimal("0.005"), "volume": Decimal("0.000"), "search_term": "密封圈 O型圈"},
        {"material_id": "MAT0012", "material_name": "工业热风机", "description": "3kW 380V 风温可调0-350℃", "base_unit": "SET", "standard_price": Decimal("2450.00"), "weight": Decimal("15.000"), "volume": Decimal("0.080"), "search_term": "热风机 工业"},
        {"material_id": "MAT0013", "material_name": "高强度螺栓M16", "description": "8.8级 六角头螺栓 M16×80mm", "base_unit": "BOX", "standard_price": Decimal("85.00"), "weight": Decimal("5.000"), "volume": Decimal("0.005"), "search_term": "螺栓 M16"},
        {"material_id": "MAT0014", "material_name": "数字万用表", "description": "真有效值测量，CAT III 1000V", "base_unit": "PC", "standard_price": Decimal("380.00"), "weight": Decimal("0.420"), "volume": Decimal("0.003"), "search_term": "万用表 数字"},
        {"material_id": "MAT0015", "material_name": "工业显示屏10寸", "description": "10.1寸 TFT LCD 1024×600 触摸屏", "base_unit": "PC", "standard_price": Decimal("680.00"), "weight": Decimal("0.850"), "volume": Decimal("0.006"), "search_term": "显示屏 工业"},
    ]
    for m in materials_data:
        db.add(Material(**m))
    db.flush()
    print(f"  [OK] {len(materials_data)} Materials created")

    # ──────────────────────────────────────────────
    # 6. Sales Flow: Inquiry → Quotation → Sales Order → Delivery → Invoice
    # ──────────────────────────────────────────────
    today = date.today()

    for i in range(1, 9):
        bp_id = f"BP{str(i).zfill(5)}"
        # --- 6a. Inquiry ---
        inq = Inquiry(
            inquiry_id=f"INQ{str(i).zfill(5)}", inquiry_type="QT",
            status="CLOSED", customer_id=bp_id, sold_to_party=bp_id,
            sales_org="1000", distribution_channel="10", division="01",
            requested_delivery_date=today + timedelta(days=random.randint(5, 30)),
            valid_from=today - timedelta(days=random.randint(10, 30)),
            valid_to=today + timedelta(days=random.randint(10, 60)),
            currency="CNY", payment_terms="NET30", incoterms="FOB",
            net_value=Decimal("0.00"), created_by="ADMIN",
        )
        db.add(inq)
        db.flush()

        # Inquiry items (2-3 items per inquiry)
        mat_ids = random.sample([f"MAT{str(j).zfill(4)}" for j in range(1, 16)], random.randint(2, 3))
        total_inq_val = Decimal("0.00")
        for item_no, mat_id in enumerate(mat_ids, start=1):
            qty = Decimal(str(random.randint(10, 500)))
            # 从本地变量获取价格
            price = next(m["standard_price"] for m in materials_data if m["material_id"] == mat_id)
            net = qty * price
            total_inq_val += net
            db.add(InquiryItem(
                inquiry_item_id=f"II{str(i).zfill(3)}{str(item_no).zfill(3)}",
                inquiry_id=inq.inquiry_id, item_no=item_no * 10,
                material_id=mat_id, order_quantity=qty,
                sales_unit="PC", unit_price=price, discount=Decimal("0.00"), net_price=net,
            ))
        inq.net_value = total_inq_val
        db.flush()

        # --- 6b. Quotation ---
        qt = Quotation(
            quotation_id=f"QT{str(i).zfill(5)}", inquiry_id=inq.inquiry_id,
            quotation_type="QT", status="CLOSED", customer_id=bp_id,
            sold_to_party=bp_id, valid_from=today - timedelta(days=random.randint(5, 20)),
            valid_to=today + timedelta(days=random.randint(10, 60)),
            payment_terms="NET30", incoterms="FOB", net_value=total_inq_val * Decimal("0.95"),
        )
        db.add(qt)
        db.flush()
        for item_no, mat_id in enumerate(mat_ids, start=1):
            price = next(m["standard_price"] for m in materials_data if m["material_id"] == mat_id) * Decimal("0.95")
            qty = Decimal(str(random.randint(10, 500)))
            db.add(QuotationItem(
                quotation_item_id=f"QI{str(i).zfill(3)}{str(item_no).zfill(3)}",
                quotation_id=qt.quotation_id, item_no=item_no * 10,
                material_id=mat_id, order_quantity=qty,
                sales_unit="PC", unit_price=price, discount=Decimal("0.00"), net_price=qty * price,
            ))

        # --- 6c. Sales Order ---
        so = SalesOrder(
            sales_order_id=f"SO{str(i).zfill(5)}", quotation_id=qt.quotation_id,
            order_type="OR", status="OPEN",
            customer_id=bp_id, sold_to_party=bp_id,
            requested_delivery_date=today + timedelta(days=random.randint(3, 20)),
            payment_terms="NET30", incoterms="FOB", delivering_plant=f"PL{str(random.randint(1,3)).zfill(2)}",
            shipping_condition="01", delivery_priority="01",
            net_value=Decimal("0.00"),
        )
        db.add(so)
        db.flush()

        so_total = Decimal("0.00")
        for item_no, mat_id in enumerate(mat_ids, start=1):
            price = next(m["standard_price"] for m in materials_data if m["material_id"] == mat_id) * Decimal("0.95")
            qty = Decimal(str(random.randint(5, 200)))
            net = qty * price
            so_total += net
            db.add(SalesOrderItem(
                so_item_id=f"SI{str(i).zfill(3)}{str(item_no).zfill(3)}",
                sales_order_id=so.sales_order_id, item_no=item_no * 10,
                material_id=mat_id, item_category="TAN",
                order_quantity=qty, confirmed_quantity=qty,
                sales_unit="PC", plant=f"PL{str(random.randint(1,3)).zfill(2)}",
                unit_price=price, discount=Decimal("0.00"), net_price=net,
                availability_status="AVAILABLE",
            ))
        so.net_value = so_total
        db.flush()

        # --- 6d. Delivery ---
        dlv = Delivery(
            delivery_id=f"DLV{str(i).zfill(4)}", sales_order_id=so.sales_order_id,
            delivery_type="LF", delivery_status="PGI_DONE",
            ship_to_party=bp_id,
            planned_delivery_date=today + timedelta(days=random.randint(1, 10)),
            planned_gi_date=today + timedelta(days=random.randint(1, 10)),
            shipping_point=f"SP{str(random.randint(1,3)).zfill(2)}",
        )
        # Set actual GI date for some
        if i <= 6:
            dlv.actual_gi_date = datetime.utcnow() - timedelta(days=random.randint(1,5))
        db.add(dlv)
        db.flush()

        for item_no, mat_id in enumerate(mat_ids, start=1):
            qty = Decimal(str(random.randint(5, 100)))
            dli = DeliveryItem(
                delivery_item_id=f"DI{str(i).zfill(3)}{str(item_no).zfill(3)}",
                delivery_id=dlv.delivery_id, item_no=item_no * 10,
                material_id=mat_id,
                delivery_quantity=qty, sales_unit="PC",
            )
            db.add(dli)
            db.flush()

            # Goods Issue for completed deliveries
            if i <= 6:
                db.add(GoodsIssue(
                    goods_issue_id=f"GI{str(i).zfill(3)}{str(item_no).zfill(3)}",
                    delivery_item_id=dli.delivery_item_id,
                    actual_quantity=qty,
                    posting_date=today - timedelta(days=random.randint(1, 5)),
                    warehouse=f"WH{str(random.randint(1,3)).zfill(2)}",
                ))

        # --- 6e. Invoice ---
        inv = Invoice(
            invoice_id=f"INV{str(i).zfill(4)}", delivery_id=dlv.delivery_id,
            sales_order_id=so.sales_order_id,
            billing_type="F2", invoice_date=today - timedelta(days=random.randint(0, 5)),
            billing_date=today - timedelta(days=random.randint(0, 5)),
            sold_to_party=bp_id, payer=bp_id,
            currency="CNY", total_amount=so_total,
            status="OPEN" if i >= 7 else "CLEARED",
        )
        db.add(inv)
        db.flush()

        for item_no, mat_id in enumerate(mat_ids, start=1):
            price = next(m["standard_price"] for m in materials_data if m["material_id"] == mat_id) * Decimal("0.95")
            qty = Decimal(str(random.randint(5, 100)))
            tax = qty * price * Decimal("0.13")
            db.add(InvoiceItem(
                invoice_item_id=f"IVI{str(i).zfill(3)}{str(item_no).zfill(3)}",
                invoice_id=inv.invoice_id, item_no=item_no * 10,
                material_id=mat_id, quantity=qty,
                unit_price=price, tax_amount=tax,
                net_price=qty * price,
            ))

        # AR
        db.add(OpenAccountReceivable(
            open_ar_id=f"OAR{str(i).zfill(4)}", invoice_id=inv.invoice_id,
            receivable_amount=so_total,
            received_amount=so_total if i <= 6 else so_total * Decimal("0.4"),
            due_date=today + timedelta(days=30),
            status="CLEARED" if i <= 6 else "PARTIAL",
        ))

        # Receipt for paid ones
        if i <= 6:
            db.add(Receipt(
                receipt_id=f"RCP{str(i).zfill(4)}", invoice_id=inv.invoice_id,
                payer=bp_id, receipt_amount=so_total,
                receipt_date=datetime.utcnow() - timedelta(days=random.randint(1, 5)),
                payment_method="BANK_TRANSFER", currency="CNY",
                reference_no=f"REF{random.randint(100000, 999999)}",
            ))

        print(f"  [FLOW {i}/8] Inquiry→Quote→SO→Delivery→Invoice for {bp_id}")

    db.commit()
    print("\n========================================")
    print("  ALL TEST DATA INSERTED SUCCESSFULLY!")
    print("========================================")
    print("""
     Summary:
       10 Business Partners (客户)
       10 Customer Sales/FI Data
       10 Contacts (联系人)
       15 Materials (物料)
        8 Complete Sales Flows (询价→报价→销售订单→发货→开票)
        → 6 fully delivered & invoiced & paid
        → 2 with open AR (partial payment)
    """)

except Exception as e:
    db.rollback()
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

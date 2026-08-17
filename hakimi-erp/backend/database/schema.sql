-- ============================================
-- HAKIMI ERP Database Schema (generated from SQLAlchemy models)
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `hakimi_erp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `hakimi_erp`;

-- Table: business_partner
CREATE TABLE business_partner (
	bp_id VARCHAR(20) NOT NULL COMMENT '业务伙伴唯一标识码', 
	bp_type VARCHAR(10) NOT NULL COMMENT '伙伴类型: 组织/个人/公司', 
	bp_role VARCHAR(20) NOT NULL COMMENT '角色: SOLD_TO/SHIP_TO/PAYER', 
	bp_name VARCHAR(100) NOT NULL COMMENT '客户/公司/个人名称', 
	country VARCHAR(3) COMMENT '所属国家代码', 
	city VARCHAR(50) COMMENT '所在城市', 
	district VARCHAR(50) COMMENT '所在区县', 
	street VARCHAR(100) COMMENT '街道地址', 
	house_number VARCHAR(20) COMMENT '门牌号码', 
	postal_code VARCHAR(20) COMMENT '邮政编码', 
	language VARCHAR(3) COMMENT '通信语言', 
	time_zone VARCHAR(10) COMMENT '所在时区', 
	transportation_zone VARCHAR(20) COMMENT '运输区域代码', 
	telephone VARCHAR(20) COMMENT '固定联系电话', 
	mobile_phone VARCHAR(20) COMMENT '手机号码', 
	fax VARCHAR(20) COMMENT '传真号码', 
	email VARCHAR(100) COMMENT '电子邮箱地址', 
	status VARCHAR(20) COMMENT '交易状态: ACTIVE/BLOCK/ARCHIVED', 
	block_reason VARCHAR(255) COMMENT '冻结或禁止交易时填写的原因', 
	data_source VARCHAR(20) COMMENT '数据来源', 
	print_format VARCHAR(50) COMMENT '单据默认打印格式', 
	search_term VARCHAR(50) COMMENT '辅助检索用关键词', 
	created_time DATETIME COMMENT '记录创建时间', 
	last_changed_time DATETIME COMMENT '最后修改时间', 
	PRIMARY KEY (bp_id)
);

-- Table: material
CREATE TABLE material (
	material_id VARCHAR(20) NOT NULL, 
	material_name VARCHAR(100) NOT NULL, 
	description TEXT, 
	base_unit VARCHAR(10) NOT NULL COMMENT '基本计量单位', 
	standard_price DECIMAL(15, 2) COMMENT '标准价格', 
	weight DECIMAL(15, 3) COMMENT '重量', 
	volume DECIMAL(15, 3) COMMENT '体积', 
	search_term VARCHAR(50), 
	category VARCHAR(50) COMMENT '产品类别', 
	stock_quantity DECIMAL(15, 3) COMMENT '库存数量', 
	item_group VARCHAR(20) COMMENT '产品组', 
	status VARCHAR(10) COMMENT '状态', 
	PRIMARY KEY (material_id)
);

-- Table: pricing_condition
CREATE TABLE pricing_condition (
	condition_id VARCHAR(20) NOT NULL, 
	condition_type VARCHAR(10) NOT NULL COMMENT '条件类型', 
	condition_name VARCHAR(50) NOT NULL COMMENT '条件名称', 
	material_id VARCHAR(20) COMMENT '物料ID', 
	bp_id VARCHAR(20) COMMENT '客户ID', 
	amount DECIMAL(15, 2) COMMENT '金额', 
	rate DECIMAL(5, 2) COMMENT '百分比/折扣率', 
	currency VARCHAR(3), 
	valid_from DATE, 
	valid_to DATE, 
	status VARCHAR(10), 
	PRIMARY KEY (condition_id)
);

-- Table: sales_organization
CREATE TABLE sales_organization (
	sales_org_id VARCHAR(10) NOT NULL, 
	description VARCHAR(100) NOT NULL, 
	distribution_channel VARCHAR(10) NOT NULL, 
	division VARCHAR(10) NOT NULL, 
	currency VARCHAR(3), 
	country VARCHAR(3), 
	status VARCHAR(10), 
	PRIMARY KEY (sales_org_id, distribution_channel, division)
);

-- Table: storage_location
CREATE TABLE storage_location (
	sloc_id VARCHAR(10) NOT NULL, 
	sloc_name VARCHAR(100) NOT NULL, 
	plant VARCHAR(20) NOT NULL, 
	warehouse_no VARCHAR(10), 
	storage_type VARCHAR(20), 
	storage_bin VARCHAR(20), 
	description VARCHAR(255), 
	PRIMARY KEY (sloc_id)
);

-- Table: sys_user
CREATE TABLE sys_user (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	full_name VARCHAR(100), 
	`role` VARCHAR(20) NOT NULL, 
	is_active BOOL NOT NULL, 
	created_time DATETIME NOT NULL, 
	last_login_time DATETIME, 
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_sys_user_username ON sys_user (username);
CREATE UNIQUE INDEX ix_sys_user_email ON sys_user (email);

-- Table: bp_relationship
CREATE TABLE bp_relationship (
	relation_id VARCHAR(20) NOT NULL, 
	relationship_type VARCHAR(20) NOT NULL COMMENT '关系类型', 
	bp_from VARCHAR(20) NOT NULL, 
	bp_to VARCHAR(20) NOT NULL, 
	valid_from DATE, 
	valid_to DATE, 
	PRIMARY KEY (relation_id), 
	FOREIGN KEY(bp_from) REFERENCES business_partner (bp_id), 
	FOREIGN KEY(bp_to) REFERENCES business_partner (bp_id)
);

-- Table: contact
CREATE TABLE contact (
	contact_id VARCHAR(20) NOT NULL, 
	bp_id VARCHAR(20) NOT NULL, 
	contact_type VARCHAR(20), 
	contact_role VARCHAR(20), 
	first_name VARCHAR(50), 
	last_name VARCHAR(50), 
	department VARCHAR(50), 
	position VARCHAR(50), 
	personal_phone VARCHAR(20), 
	email VARCHAR(100), 
	status VARCHAR(10), 
	PRIMARY KEY (contact_id), 
	FOREIGN KEY(bp_id) REFERENCES business_partner (bp_id)
);

-- Table: customer_finance_data
CREATE TABLE customer_finance_data (
	bp_id VARCHAR(20) NOT NULL, 
	company_code VARCHAR(10) NOT NULL COMMENT '公司代码', 
	reconciliation_account VARCHAR(20) COMMENT '统驭科目', 
	sort_key VARCHAR(10), 
	payment_terms VARCHAR(10) COMMENT '付款条件', 
	bank_account_name VARCHAR(100), 
	bank_country VARCHAR(2), 
	bank_key VARCHAR(20), 
	bank_account VARCHAR(50), 
	iban VARCHAR(50), 
	bank_account_status VARCHAR(20), 
	card_type VARCHAR(10), 
	card_number VARCHAR(20), 
	preferred_card BOOL, 
	PRIMARY KEY (bp_id, company_code), 
	FOREIGN KEY(bp_id) REFERENCES business_partner (bp_id)
);

-- Table: customer_sales_data
CREATE TABLE customer_sales_data (
	bp_id VARCHAR(20) NOT NULL, 
	sales_org VARCHAR(10) NOT NULL COMMENT '销售组织代码', 
	distribution_channel VARCHAR(10) NOT NULL COMMENT '分销渠道代码', 
	division VARCHAR(10) NOT NULL COMMENT '产品组/事业部代码', 
	sales_office VARCHAR(10), 
	sales_group VARCHAR(10), 
	sales_district VARCHAR(10), 
	currency VARCHAR(3) COMMENT '交易货币', 
	price_group VARCHAR(10), 
	customer_pricing_procedure VARCHAR(20), 
	delivery_priority VARCHAR(2), 
	shipping_condition VARCHAR(10), 
	delivering_plant VARCHAR(20), 
	max_partial_deliveries INTEGER, 
	incoterms VARCHAR(5), 
	account_assignment_group VARCHAR(20), 
	tax_classification VARCHAR(20), 
	PRIMARY KEY (bp_id, sales_org, distribution_channel, division), 
	FOREIGN KEY(bp_id) REFERENCES business_partner (bp_id)
);

-- Table: inquiry
CREATE TABLE inquiry (
	inquiry_id VARCHAR(20) NOT NULL, 
	inquiry_type VARCHAR(20) NOT NULL, 
	status VARCHAR(20) COMMENT 'OPEN/CLOSED/CANCELLED', 
	customer_id VARCHAR(20) NOT NULL, 
	sold_to_party VARCHAR(20), 
	ship_to_party VARCHAR(20), 
	sales_area VARCHAR(100), 
	customer_reference VARCHAR(50), 
	customer_reference_date DATE, 
	sales_org VARCHAR(10), 
	distribution_channel VARCHAR(10), 
	division VARCHAR(10), 
	sales_office VARCHAR(10), 
	sales_group VARCHAR(10), 
	requested_delivery_date DATE, 
	valid_from DATE, 
	valid_to DATE, 
	pricing_date DATE, 
	currency VARCHAR(3), 
	delivering_plant VARCHAR(20), 
	incoterms VARCHAR(5), 
	delivery_location VARCHAR(100), 
	payment_terms VARCHAR(10), 
	max_partial_deliveries INTEGER, 
	net_value DECIMAL(15, 2), 
	inquiry_address VARCHAR(255), 
	remark TEXT, 
	search_term VARCHAR(20), 
	created_time DATETIME, 
	created_by VARCHAR(20), 
	PRIMARY KEY (inquiry_id), 
	FOREIGN KEY(customer_id) REFERENCES business_partner (bp_id)
);

-- Table: sys_user_session
CREATE TABLE sys_user_session (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	token VARCHAR(128) NOT NULL, 
	expires_at DATETIME NOT NULL, 
	created_time DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES sys_user (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_sys_user_session_token ON sys_user_session (token);
CREATE INDEX ix_sys_user_session_expires_at ON sys_user_session (expires_at);
CREATE INDEX ix_sys_user_session_user_id ON sys_user_session (user_id);

-- Table: inquiry_item
CREATE TABLE inquiry_item (
	inquiry_item_id VARCHAR(20) NOT NULL, 
	inquiry_id VARCHAR(20) NOT NULL, 
	item_no INTEGER NOT NULL COMMENT '行号: 10, 20, 30...', 
	material_id VARCHAR(20) NOT NULL, 
	item_description VARCHAR(255), 
	order_quantity DECIMAL(15, 3), 
	sales_unit VARCHAR(10), 
	expected_order_value DECIMAL(15, 2), 
	unit_price DECIMAL(15, 2), 
	discount DECIMAL(15, 2), 
	net_price DECIMAL(15, 2), 
	remark TEXT, 
	search_term VARCHAR(20), 
	PRIMARY KEY (inquiry_item_id), 
	CONSTRAINT uk_inquiry_item UNIQUE (inquiry_id, item_no), 
	FOREIGN KEY(inquiry_id) REFERENCES inquiry (inquiry_id), 
	FOREIGN KEY(material_id) REFERENCES material (material_id)
);

-- Table: quotation
CREATE TABLE quotation (
	quotation_id VARCHAR(20) NOT NULL, 
	inquiry_id VARCHAR(20), 
	quotation_type VARCHAR(20) NOT NULL, 
	status VARCHAR(20), 
	customer_id VARCHAR(20) NOT NULL, 
	sold_to_party VARCHAR(20), 
	ship_to_party VARCHAR(20), 
	sales_area VARCHAR(100), 
	customer_reference VARCHAR(50), 
	customer_reference_date DATE, 
	sales_org VARCHAR(10), 
	distribution_channel VARCHAR(10), 
	division VARCHAR(10), 
	sales_office VARCHAR(10), 
	sales_group VARCHAR(10), 
	requested_delivery_date DATE, 
	valid_from DATE, 
	valid_to DATE, 
	pricing_date DATE, 
	currency VARCHAR(3), 
	payment_terms VARCHAR(10), 
	incoterms VARCHAR(5), 
	delivering_plant VARCHAR(20), 
	max_partial_deliveries INTEGER, 
	net_value DECIMAL(15, 2), 
	quotation_address VARCHAR(255), 
	remark TEXT, 
	search_term VARCHAR(20), 
	created_time DATETIME, 
	created_by VARCHAR(20), 
	PRIMARY KEY (quotation_id), 
	FOREIGN KEY(inquiry_id) REFERENCES inquiry (inquiry_id), 
	FOREIGN KEY(customer_id) REFERENCES business_partner (bp_id)
);

-- Table: quotation_item
CREATE TABLE quotation_item (
	quotation_item_id VARCHAR(20) NOT NULL, 
	quotation_id VARCHAR(20) NOT NULL, 
	item_no INTEGER NOT NULL, 
	material_id VARCHAR(20) NOT NULL, 
	item_description VARCHAR(255), 
	order_quantity DECIMAL(15, 3), 
	sales_unit VARCHAR(10), 
	expected_order_value DECIMAL(15, 2), 
	unit_price DECIMAL(15, 2), 
	discount DECIMAL(15, 2), 
	net_price DECIMAL(15, 2), 
	remark TEXT, 
	search_term VARCHAR(20), 
	PRIMARY KEY (quotation_item_id), 
	CONSTRAINT uk_quotation_item UNIQUE (quotation_id, item_no), 
	FOREIGN KEY(quotation_id) REFERENCES quotation (quotation_id), 
	FOREIGN KEY(material_id) REFERENCES material (material_id)
);

-- Table: sales_order
CREATE TABLE sales_order (
	sales_order_id VARCHAR(20) NOT NULL, 
	quotation_id VARCHAR(20), 
	order_type VARCHAR(20) NOT NULL, 
	reference_type VARCHAR(1), 
	reference_document VARCHAR(20), 
	status VARCHAR(20), 
	customer_id VARCHAR(20) NOT NULL, 
	sold_to_party VARCHAR(20), 
	ship_to_party VARCHAR(20), 
	customer_reference VARCHAR(50), 
	customer_reference_date DATE, 
	sales_org VARCHAR(10), 
	distribution_channel VARCHAR(10), 
	division VARCHAR(10), 
	sales_office VARCHAR(10), 
	sales_group VARCHAR(10), 
	requested_delivery_date DATE, 
	pricing_date DATE, 
	currency VARCHAR(3), 
	payment_terms VARCHAR(10), 
	incoterms VARCHAR(5), 
	delivering_plant VARCHAR(20), 
	shipping_condition VARCHAR(10), 
	delivery_priority VARCHAR(2), 
	billing_block VARCHAR(20), 
	delivery_block VARCHAR(20), 
	max_partial_deliveries INTEGER, 
	net_value DECIMAL(15, 2), 
	remark TEXT, 
	search_term VARCHAR(20), 
	created_time DATETIME, 
	created_by VARCHAR(20), 
	PRIMARY KEY (sales_order_id), 
	FOREIGN KEY(quotation_id) REFERENCES quotation (quotation_id), 
	FOREIGN KEY(customer_id) REFERENCES business_partner (bp_id)
);

-- Table: delivery
CREATE TABLE delivery (
	delivery_id VARCHAR(20) NOT NULL, 
	sales_order_id VARCHAR(20), 
	delivery_type VARCHAR(20) NOT NULL, 
	delivery_status VARCHAR(20) NOT NULL COMMENT 'OPEN/PICKING/SHIPPED/IN_TRANSIT/PGI_DONE/CANCELLED', 
	ship_to_party VARCHAR(20) NOT NULL, 
	planned_delivery_date DATE, 
	planned_gi_date DATE, 
	actual_gi_date DATETIME, 
	picking_date DATE, 
	shipping_point VARCHAR(20), 
	carrier VARCHAR(100), 
	driver_name VARCHAR(50), 
	route VARCHAR(100), 
	tracking_no VARCHAR(50), 
	created_time DATETIME, 
	PRIMARY KEY (delivery_id), 
	FOREIGN KEY(sales_order_id) REFERENCES sales_order (sales_order_id), 
	FOREIGN KEY(ship_to_party) REFERENCES business_partner (bp_id)
);

-- Table: sales_order_item
CREATE TABLE sales_order_item (
	so_item_id VARCHAR(20) NOT NULL, 
	sales_order_id VARCHAR(20) NOT NULL, 
	item_no INTEGER NOT NULL, 
	material_id VARCHAR(20) NOT NULL, 
	item_description VARCHAR(255), 
	item_category VARCHAR(10), 
	order_quantity DECIMAL(15, 3), 
	confirmed_quantity DECIMAL(15, 3), 
	sales_unit VARCHAR(10), 
	plant VARCHAR(20), 
	storage_location VARCHAR(10), 
	shipping_point VARCHAR(10), 
	unit_price DECIMAL(15, 2), 
	discount DECIMAL(15, 2), 
	net_price DECIMAL(15, 2), 
	availability_status VARCHAR(20), 
	remark TEXT, 
	search_term VARCHAR(20), 
	PRIMARY KEY (so_item_id), 
	CONSTRAINT uk_sales_order_item UNIQUE (sales_order_id, item_no), 
	FOREIGN KEY(sales_order_id) REFERENCES sales_order (sales_order_id), 
	FOREIGN KEY(material_id) REFERENCES material (material_id)
);

-- Table: delivery_item
CREATE TABLE delivery_item (
	delivery_item_id VARCHAR(20) NOT NULL, 
	delivery_id VARCHAR(20) NOT NULL, 
	item_no INTEGER NOT NULL, 
	so_item_id VARCHAR(20), 
	material_id VARCHAR(20) NOT NULL, 
	order_quantity DECIMAL(15, 3), 
	delivery_quantity DECIMAL(15, 3), 
	picked_quantity DECIMAL(15, 3), 
	sales_unit VARCHAR(10), 
	plant VARCHAR(20), 
	storage_location VARCHAR(10), 
	item_description VARCHAR(255), 
	item_status VARCHAR(20), 
	PRIMARY KEY (delivery_item_id), 
	CONSTRAINT uk_delivery_item UNIQUE (delivery_id, item_no), 
	FOREIGN KEY(delivery_id) REFERENCES delivery (delivery_id), 
	FOREIGN KEY(so_item_id) REFERENCES sales_order_item (so_item_id), 
	FOREIGN KEY(material_id) REFERENCES material (material_id)
);

-- Table: invoice
CREATE TABLE invoice (
	invoice_id VARCHAR(20) NOT NULL, 
	delivery_id VARCHAR(20), 
	sales_order_id VARCHAR(20), 
	billing_type VARCHAR(20) NOT NULL, 
	invoice_date DATE NOT NULL, 
	billing_date DATE NOT NULL, 
	sales_org VARCHAR(4) COMMENT '销售组织代码', 
	distribution_channel VARCHAR(2) COMMENT '分销渠道代码', 
	division VARCHAR(2) COMMENT '产品组/事业部代码', 
	shipping_point VARCHAR(20) COMMENT '装运点/发货点', 
	sold_to_party VARCHAR(20), 
	payer VARCHAR(20), 
	destination_country VARCHAR(3) COMMENT '货物目的国家', 
	currency VARCHAR(3), 
	total_amount DECIMAL(15, 2), 
	status VARCHAR(20) NOT NULL COMMENT 'OPEN/PARTIAL/CLEARED/VOID', 
	remark TEXT COMMENT '其他补充说明', 
	search_term VARCHAR(50) COMMENT '辅助检索用关键词', 
	PRIMARY KEY (invoice_id), 
	FOREIGN KEY(delivery_id) REFERENCES delivery (delivery_id), 
	FOREIGN KEY(sales_order_id) REFERENCES sales_order (sales_order_id), 
	FOREIGN KEY(payer) REFERENCES business_partner (bp_id)
);

-- Table: closed_account_receivable
CREATE TABLE closed_account_receivable (
	closed_ar_id VARCHAR(20) NOT NULL, 
	invoice_id VARCHAR(20) NOT NULL, 
	receivable_amount DECIMAL(15, 2) NOT NULL, 
	received_amount DECIMAL(15, 2) NOT NULL, 
	created_time DATETIME, 
	closed_time DATETIME NOT NULL, 
	remark TEXT COMMENT '其他补充说明', 
	search_term VARCHAR(50) COMMENT '辅助检索用关键词', 
	PRIMARY KEY (closed_ar_id), 
	FOREIGN KEY(invoice_id) REFERENCES invoice (invoice_id)
);

-- Table: goods_issue
CREATE TABLE goods_issue (
	goods_issue_id VARCHAR(20) NOT NULL, 
	delivery_item_id VARCHAR(20) NOT NULL, 
	actual_quantity DECIMAL(15, 3) NOT NULL, 
	posting_date DATE NOT NULL, 
	goods_issue_time DATETIME NOT NULL, 
	warehouse VARCHAR(20), 
	batch_no INTEGER, 
	PRIMARY KEY (goods_issue_id), 
	FOREIGN KEY(delivery_item_id) REFERENCES delivery_item (delivery_item_id)
);

-- Table: invoice_item
CREATE TABLE invoice_item (
	invoice_item_id VARCHAR(20) NOT NULL, 
	invoice_id VARCHAR(20) NOT NULL, 
	item_no INTEGER NOT NULL, 
	material_id VARCHAR(20) NOT NULL, 
	quantity DECIMAL(15, 3), 
	sales_unit VARCHAR(10) COMMENT '销售计量单位', 
	unit_price DECIMAL(15, 2), 
	discount DECIMAL(5, 2) COMMENT '折扣百分比或金额', 
	tax_amount DECIMAL(15, 2), 
	net_price DECIMAL(15, 2), 
	item_description VARCHAR(500) COMMENT '行项目补充说明', 
	remark TEXT COMMENT '其他补充说明', 
	PRIMARY KEY (invoice_item_id), 
	CONSTRAINT uk_invoice_item UNIQUE (invoice_id, item_no), 
	FOREIGN KEY(invoice_id) REFERENCES invoice (invoice_id), 
	FOREIGN KEY(material_id) REFERENCES material (material_id)
);

-- Table: open_account_receivable
CREATE TABLE open_account_receivable (
	open_ar_id VARCHAR(20) NOT NULL, 
	invoice_id VARCHAR(20) NOT NULL, 
	receivable_amount DECIMAL(15, 2) NOT NULL, 
	received_amount DECIMAL(15, 2), 
	due_date DATE, 
	status VARCHAR(20) COMMENT 'UNPAID/PARTIAL/OVERDUE', 
	remark TEXT COMMENT '其他补充说明', 
	search_term VARCHAR(50) COMMENT '辅助检索用关键词', 
	created_time DATETIME, 
	PRIMARY KEY (open_ar_id), 
	UNIQUE (invoice_id), 
	FOREIGN KEY(invoice_id) REFERENCES invoice (invoice_id)
);

-- Table: pick_record
CREATE TABLE pick_record (
	pick_id VARCHAR(20) NOT NULL, 
	delivery_item_id VARCHAR(20) NOT NULL, 
	batch_no INTEGER NOT NULL, 
	pick_quantity DECIMAL(15, 3) NOT NULL, 
	storage_location VARCHAR(10), 
	pick_date DATETIME NOT NULL, 
	picked_by VARCHAR(50), 
	PRIMARY KEY (pick_id), 
	FOREIGN KEY(delivery_item_id) REFERENCES delivery_item (delivery_item_id)
);

-- Table: receipt
CREATE TABLE receipt (
	receipt_id VARCHAR(20) NOT NULL, 
	invoice_id VARCHAR(20) NOT NULL, 
	payer VARCHAR(20) NOT NULL, 
	receipt_amount DECIMAL(15, 2) NOT NULL, 
	receipt_date DATETIME NOT NULL, 
	payment_method VARCHAR(20), 
	currency VARCHAR(3), 
	reference_no VARCHAR(50), 
	remark TEXT COMMENT '其他补充说明', 
	search_term VARCHAR(50) COMMENT '辅助检索用关键词', 
	PRIMARY KEY (receipt_id), 
	FOREIGN KEY(invoice_id) REFERENCES invoice (invoice_id), 
	FOREIGN KEY(payer) REFERENCES business_partner (bp_id)
);

SET FOREIGN_KEY_CHECKS = 1;

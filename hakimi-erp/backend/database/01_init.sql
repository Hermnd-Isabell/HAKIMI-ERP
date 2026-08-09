-- HAKIMI ERP Database Initialization Script
-- Based on SAP SD Logic Model Design Report V1.0
-- MySQL 8.0+ 

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ---------------------------------------------------------
-- CREATE DATABASE
-- ---------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `hakimi_erp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `hakimi_erp`;

-- ---------------------------------------------------------
-- D1: CUSTOMER MASTER DATA (Business Partner)
-- ---------------------------------------------------------

-- 3.1 business_partner
CREATE TABLE IF NOT EXISTS `business_partner` (
    `bp_id` VARCHAR(20) NOT NULL COMMENT '业务伙伴唯一标识码',
    `bp_type` VARCHAR(10) NOT NULL COMMENT '伙伴类型: 组织/个人/公司',
    `bp_role` VARCHAR(20) NOT NULL COMMENT '角色: SOLD_TO/SHIP_TO/PAYER',
    `bp_name` VARCHAR(100) NOT NULL COMMENT '客户/公司/个人名称',
    `country` VARCHAR(3) DEFAULT 'CN' COMMENT '所属国家代码',
    `city` VARCHAR(50) COMMENT '所在城市',
    `district` VARCHAR(50) COMMENT '所在区县',
    `street` VARCHAR(100) COMMENT '街道地址',
    `house_number` VARCHAR(20) COMMENT '门牌号码',
    `postal_code` VARCHAR(20) COMMENT '邮政编码',
    `language` VARCHAR(3) DEFAULT 'ZH' COMMENT '通信语言',
    `time_zone` VARCHAR(10) DEFAULT 'UTC+8' COMMENT '所在时区',
    `transportation_zone` VARCHAR(20) COMMENT '运输区域代码',
    `telephone` VARCHAR(20) COMMENT '固定联系电话',
    `mobile_phone` VARCHAR(20) COMMENT '手机号码',
    `fax` VARCHAR(20) COMMENT '传真号码',
    `email` VARCHAR(100) COMMENT '电子邮箱地址',
    `status` VARCHAR(20) DEFAULT 'ACTIVE' COMMENT '交易状态: ACTIVE/BLOCK/ARCHIVED',
    `block_reason` VARCHAR(255) COMMENT '冻结或禁止交易时填写的原因',
    `data_source` VARCHAR(20) DEFAULT 'MANUAL' COMMENT '数据来源',
    `print_format` VARCHAR(50) COMMENT '单据默认打印格式',
    `search_term` VARCHAR(50) COMMENT '辅助检索用关键词',
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `last_changed_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
    PRIMARY KEY (`bp_id`)
) ENGINE=InnoDB COMMENT='业务伙伴（客户主记录）';

-- 3.2 customer_sales_data
CREATE TABLE IF NOT EXISTS `customer_sales_data` (
    `bp_id` VARCHAR(20) NOT NULL,
    `sales_org` VARCHAR(10) NOT NULL COMMENT '销售组织代码',
    `distribution_channel` VARCHAR(10) NOT NULL COMMENT '分销渠道代码',
    `division` VARCHAR(10) NOT NULL COMMENT '产品组/事业部代码',
    `sales_office` VARCHAR(10),
    `sales_group` VARCHAR(10),
    `sales_district` VARCHAR(10),
    `currency` CHAR(3) DEFAULT 'CNY' COMMENT '交易货币',
    `price_group` VARCHAR(10),
    `customer_pricing_procedure` VARCHAR(20),
    `delivery_priority` CHAR(2),
    `shipping_condition` VARCHAR(10),
    `delivering_plant` VARCHAR(20),
    `max_partial_deliveries` INT DEFAULT 9,
    `incoterms` VARCHAR(5),
    `account_assignment_group` VARCHAR(20),
    `tax_classification` VARCHAR(20),
    PRIMARY KEY (`bp_id`, `sales_org`, `distribution_channel`, `division`),
    FOREIGN KEY (`bp_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='客户销售区域数据';

-- 3.3 customer_finance_data
CREATE TABLE IF NOT EXISTS `customer_finance_data` (
    `bp_id` VARCHAR(20) NOT NULL,
    `company_code` VARCHAR(10) NOT NULL COMMENT '公司代码',
    `reconciliation_account` VARCHAR(20) COMMENT '统驭科目',
    `sort_key` VARCHAR(10),
    `payment_terms` VARCHAR(10) COMMENT '付款条件',
    `bank_account_name` VARCHAR(100),
    `bank_country` CHAR(2),
    `bank_key` VARCHAR(20),
    `bank_account` VARCHAR(50),
    `iban` VARCHAR(50),
    `bank_account_status` VARCHAR(20) DEFAULT 'ACTIVE',
    `card_type` VARCHAR(10),
    `card_number` VARCHAR(20),
    `preferred_card` TINYINT(1) DEFAULT 0,
    PRIMARY KEY (`bp_id`, `company_code`),
    FOREIGN KEY (`bp_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='客户公司代码财务数据';

-- 3.4 contact
CREATE TABLE IF NOT EXISTS `contact` (
    `contact_id` VARCHAR(20) NOT NULL,
    `bp_id` VARCHAR(20) NOT NULL,
    `contact_type` VARCHAR(20),
    `contact_role` VARCHAR(20),
    `first_name` VARCHAR(50),
    `last_name` VARCHAR(50),
    `department` VARCHAR(50),
    `position` VARCHAR(50),
    `personal_phone` VARCHAR(20),
    `email` VARCHAR(100),
    `status` VARCHAR(10) DEFAULT 'ACTIVE',
    PRIMARY KEY (`contact_id`),
    FOREIGN KEY (`bp_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='联系人';

-- 3.5 bp_relationship
CREATE TABLE IF NOT EXISTS `bp_relationship` (
    `relation_id` VARCHAR(20) NOT NULL,
    `relationship_type` VARCHAR(20) NOT NULL COMMENT '关系类型',
    `bp_from` VARCHAR(20) NOT NULL,
    `bp_to` VARCHAR(20) NOT NULL,
    `valid_from` DATE,
    `valid_to` DATE,
    PRIMARY KEY (`relation_id`),
    FOREIGN KEY (`bp_from`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`bp_to`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='业务伙伴关系';


-- 3.5 storage_location (warehouse storage location master)
CREATE TABLE IF NOT EXISTS `storage_location` (
    `sloc_id` VARCHAR(10) NOT NULL COMMENT 'Storage location ID',
    `sloc_name` VARCHAR(100) NOT NULL COMMENT 'Storage location name',
    `plant` VARCHAR(20) NOT NULL COMMENT 'Associated plant',
    `warehouse_no` VARCHAR(10) COMMENT 'Warehouse number',
    `storage_type` VARCHAR(20) COMMENT 'Storage type: RAW/SEMI/FERT/BULK/HAZ/COLD/PICK/STAG',
    `storage_bin` VARCHAR(20) COMMENT 'Shelf/bin coordinate',
    `description` VARCHAR(255) COMMENT 'Description',
    PRIMARY KEY (`sloc_id`)
) ENGINE=InnoDB COMMENT='Warehouse storage location master data';

-- ---------------------------------------------------------
-- D2: MATERIAL MASTER DATA
-- ---------------------------------------------------------

-- 4.1 material
CREATE TABLE IF NOT EXISTS `material` (
    `material_id` VARCHAR(20) NOT NULL,
    `material_name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `base_unit` VARCHAR(10) NOT NULL COMMENT '基本计量单位',
    `standard_price` DECIMAL(15,2) COMMENT '标准价格',
    `weight` DECIMAL(15,3) COMMENT '重量',
    `volume` DECIMAL(15,3) COMMENT '体积',
    `search_term` VARCHAR(50),
    `category` VARCHAR(50) DEFAULT NULL,
    `stock_quantity` DECIMAL(15,3) DEFAULT 0.000,
    `item_group` VARCHAR(20) DEFAULT NULL,
    `status` VARCHAR(10) DEFAULT 'ACTIVE',
    PRIMARY KEY (`material_id`)
) ENGINE=InnoDB COMMENT='物料主记录';

-- 4.2 sales_organization
CREATE TABLE IF NOT EXISTS `sales_organization` (
  `sales_org_id` varchar(10) NOT NULL COMMENT '销售组织代码',
  `description` varchar(100) NOT NULL COMMENT '描述',
  `distribution_channel` varchar(10) NOT NULL COMMENT '分销渠道',
  `division` varchar(10) NOT NULL COMMENT '产品组/事业部',
  `currency` varchar(3) DEFAULT 'CNY' COMMENT '本位币',
  `country` varchar(3) DEFAULT 'CN' COMMENT '所属国家',
  `status` varchar(10) DEFAULT 'ACTIVE' COMMENT '状态',
  PRIMARY KEY (`sales_org_id`,`distribution_channel`,`division`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4.3 pricing_condition
CREATE TABLE IF NOT EXISTS `pricing_condition` (
  `condition_id` varchar(20) NOT NULL,
  `condition_type` varchar(10) NOT NULL,
  `condition_name` varchar(50) NOT NULL,
  `material_id` varchar(20) DEFAULT NULL,
  `bp_id` varchar(20) DEFAULT NULL,
  `amount` decimal(15,2) DEFAULT NULL,
  `rate` decimal(5,2) DEFAULT NULL,
  `currency` varchar(3) DEFAULT 'CNY',
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `status` varchar(10) DEFAULT 'ACTIVE',
  PRIMARY KEY (`condition_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- D3: BUSINESS DOCUMENTS
-- ---------------------------------------------------------

-- 5.1 inquiry
CREATE TABLE IF NOT EXISTS `inquiry` (
    `inquiry_id` VARCHAR(20) NOT NULL,
    `inquiry_type` VARCHAR(20) NOT NULL,
    `status` VARCHAR(20) DEFAULT 'OPEN' COMMENT 'OPEN/CLOSED/CANCELLED',
    `customer_id` VARCHAR(20) NOT NULL,
    `sold_to_party` VARCHAR(20),
    `ship_to_party` VARCHAR(20),
    `customer_reference` VARCHAR(50),
    `sales_org` VARCHAR(10),
    `distribution_channel` VARCHAR(10),
    `division` VARCHAR(10),
    `requested_delivery_date` DATE,
    `valid_from` DATE,
    `valid_to` DATE,
    `pricing_date` DATE,
    `currency` CHAR(3) DEFAULT 'CNY',
    `delivering_plant` VARCHAR(20),
    `incoterms` VARCHAR(5),
    `payment_terms` VARCHAR(10),
    `net_value` DECIMAL(15,2),
    `inquiry_address` VARCHAR(255),
    `delivery_location` VARCHAR(100),
    `max_partial_deliveries` INT DEFAULT 9,
    `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `created_by` VARCHAR(20),
    PRIMARY KEY (`inquiry_id`),
    FOREIGN KEY (`customer_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='询价单抬头';

-- 5.2 inquiry_item
CREATE TABLE IF NOT EXISTS `inquiry_item` (
    `inquiry_item_id` VARCHAR(20) NOT NULL,
    `inquiry_id` VARCHAR(20) NOT NULL,
    `item_no` INT NOT NULL COMMENT '行号: 10, 20, 30...',
    `material_id` VARCHAR(20) NOT NULL,
    `item_description` VARCHAR(255),
    `order_quantity` DECIMAL(15,3),
    `sales_unit` VARCHAR(10),
    `expected_order_value` DECIMAL(15,2),
    `unit_price` DECIMAL(15,2),
    `discount` DECIMAL(15,2),
    `net_price` DECIMAL(15,2),
    PRIMARY KEY (`inquiry_item_id`),
    UNIQUE KEY `uk_inquiry_item` (`inquiry_id`, `item_no`),
    FOREIGN KEY (`inquiry_id`) REFERENCES `inquiry` (`inquiry_id`) ON DELETE CASCADE,
    FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='询价单行项目';

-- 5.3 quotation
CREATE TABLE IF NOT EXISTS `quotation` (
    `quotation_id` VARCHAR(20) NOT NULL,
    `inquiry_id` VARCHAR(20),
    `quotation_type` VARCHAR(20) NOT NULL,
    `status` VARCHAR(20) DEFAULT 'OPEN',
    `customer_id` VARCHAR(20) NOT NULL,
    `sold_to_party` VARCHAR(20),
    `ship_to_party` VARCHAR(20),
    `valid_from` DATE,
    `valid_to` DATE,
    `payment_terms` VARCHAR(10),
    `incoterms` VARCHAR(5),
    `net_value` DECIMAL(15,2),
    `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`quotation_id`),
    FOREIGN KEY (`customer_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`inquiry_id`) REFERENCES `inquiry` (`inquiry_id`) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='报价单抬头';

-- 5.4 quotation_item
CREATE TABLE IF NOT EXISTS `quotation_item` (
    `quotation_item_id` VARCHAR(20) NOT NULL,
    `quotation_id` VARCHAR(20) NOT NULL,
    `item_no` INT NOT NULL,
    `material_id` VARCHAR(20) NOT NULL,
    `order_quantity` DECIMAL(15,3),
    `sales_unit` VARCHAR(10),
    `unit_price` DECIMAL(15,2),
    `discount` DECIMAL(15,2),
    `net_price` DECIMAL(15,2),
    PRIMARY KEY (`quotation_item_id`),
    UNIQUE KEY `uk_quotation_item` (`quotation_id`, `item_no`),
    FOREIGN KEY (`quotation_id`) REFERENCES `quotation` (`quotation_id`) ON DELETE CASCADE,
    FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='报价单行项目';

-- 5.5 sales_order
CREATE TABLE IF NOT EXISTS `sales_order` (
    `sales_order_id` VARCHAR(20) NOT NULL,
    `quotation_id` VARCHAR(20),
    `order_type` VARCHAR(20) NOT NULL,
    `status` VARCHAR(20) DEFAULT 'OPEN',
    `customer_id` VARCHAR(20) NOT NULL,
    `sold_to_party` VARCHAR(20),
    `ship_to_party` VARCHAR(20),
    `customer_reference` VARCHAR(50),
    `requested_delivery_date` DATE,
    `pricing_date` DATE,
    `payment_terms` VARCHAR(10),
    `incoterms` VARCHAR(5),
    `delivering_plant` VARCHAR(20),
    `shipping_condition` VARCHAR(10),
    `delivery_priority` CHAR(2),
    `billing_block` VARCHAR(20),
    `delivery_block` VARCHAR(20),
    `net_value` DECIMAL(15,2),
    `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`sales_order_id`),
    FOREIGN KEY (`customer_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`quotation_id`) REFERENCES `quotation` (`quotation_id`) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='销售订单抬头';

-- 5.6 sales_order_item
CREATE TABLE IF NOT EXISTS `sales_order_item` (
    `so_item_id` VARCHAR(20) NOT NULL,
    `sales_order_id` VARCHAR(20) NOT NULL,
    `item_no` INT NOT NULL,
    `material_id` VARCHAR(20) NOT NULL,
    `item_category` VARCHAR(10),
    `order_quantity` DECIMAL(15,3),
    `confirmed_quantity` DECIMAL(15,3),
    `sales_unit` VARCHAR(10),
    `plant` VARCHAR(20),
    `storage_location` VARCHAR(10),
    `shipping_point` VARCHAR(10),
    `unit_price` DECIMAL(15,2),
    `discount` DECIMAL(15,2),
    `net_price` DECIMAL(15,2),
    `availability_status` VARCHAR(20),
    PRIMARY KEY (`so_item_id`),
    UNIQUE KEY `uk_sales_order_item` (`sales_order_id`, `item_no`),
    FOREIGN KEY (`sales_order_id`) REFERENCES `sales_order` (`sales_order_id`) ON DELETE CASCADE,
    FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='销售订单行项目';

-- ---------------------------------------------------------
-- D4: LOGISTICS
-- ---------------------------------------------------------

-- 6.1 delivery
CREATE TABLE IF NOT EXISTS `delivery` (
    `delivery_id` VARCHAR(20) NOT NULL,
    `sales_order_id` VARCHAR(20),
    `delivery_type` VARCHAR(20) NOT NULL,
    `delivery_status` VARCHAR(20) NOT NULL COMMENT 'OPEN/PGI_DONE/CANCELLED',
    `ship_to_party` VARCHAR(20) NOT NULL,
    `planned_delivery_date` DATE,
    `planned_gi_date` DATE,
    `actual_gi_date` DATETIME,
    `picking_date` DATE,
    `shipping_point` VARCHAR(20),
    `carrier` VARCHAR(100) COMMENT 'Carrier',
    `driver_name` VARCHAR(50) COMMENT 'Driver name',
    `route` VARCHAR(100) COMMENT 'Route',
    `tracking_no` VARCHAR(50) COMMENT 'Tracking No',
    PRIMARY KEY (`delivery_id`),
    FOREIGN KEY (`ship_to_party`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`sales_order_id`) REFERENCES `sales_order` (`sales_order_id`) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='交货单抬头';

-- 6.2 delivery_item
CREATE TABLE IF NOT EXISTS `delivery_item` (
    `delivery_item_id` VARCHAR(20) NOT NULL,
    `delivery_id` VARCHAR(20) NOT NULL,
    `item_no` INT NOT NULL,
    `so_item_id` VARCHAR(20),
    `material_id` VARCHAR(20) NOT NULL,
    `delivery_quantity` DECIMAL(15,3),
    `sales_unit` VARCHAR(10),
    `item_description` VARCHAR(255),
    `picked_quantity` DECIMAL(15,3) DEFAULT 0,
    `plant` VARCHAR(20),
    `storage_location` VARCHAR(10),
    `item_status` VARCHAR(20) DEFAULT 'OPEN',
    `order_quantity` DECIMAL(15,3) DEFAULT 0,
    PRIMARY KEY (`delivery_item_id`),
    UNIQUE KEY `uk_delivery_item` (`delivery_id`, `item_no`),
    FOREIGN KEY (`delivery_id`) REFERENCES `delivery` (`delivery_id`) ON DELETE CASCADE,
    FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`so_item_id`) REFERENCES `sales_order_item` (`so_item_id`) ON DELETE SET NULL
) ENGINE=InnoDB COMMENT='交货单行项目';

-- 6.3 goods_issue
CREATE TABLE IF NOT EXISTS `goods_issue` (
    `goods_issue_id` VARCHAR(20) NOT NULL,
    `delivery_item_id` VARCHAR(20) NOT NULL,
    `actual_quantity` DECIMAL(15,3) NOT NULL,
    `posting_date` DATE NOT NULL,
    `goods_issue_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `warehouse` VARCHAR(20),
    `batch_no` INT DEFAULT 1,
    PRIMARY KEY (`goods_issue_id`),
    FOREIGN KEY (`delivery_item_id`) REFERENCES `delivery_item` (`delivery_item_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='发货过账';


-- 6.4 pick_record (batch picking history)
CREATE TABLE IF NOT EXISTS `pick_record` (
    `pick_id` VARCHAR(20) NOT NULL,
    `delivery_item_id` VARCHAR(20) NOT NULL,
    `batch_no` INT NOT NULL COMMENT 'Pick batch number within the delivery',
    `pick_quantity` DECIMAL(15,3) NOT NULL DEFAULT 0,
    `storage_location` VARCHAR(10) COMMENT 'Storage location where pick occurred',
    `pick_date` DATETIME NOT NULL COMMENT 'Pick date and time',
    `picked_by` VARCHAR(50) COMMENT 'Operator who performed the pick',
    PRIMARY KEY (`pick_id`),
    FOREIGN KEY (`delivery_item_id`) REFERENCES delivery_item (delivery_item_id) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='Pick record for batch picking operations';

-- ---------------------------------------------------------
-- D5: FINANCIAL
-- ---------------------------------------------------------

-- 7.1 invoice
CREATE TABLE IF NOT EXISTS `invoice` (
    `invoice_id` VARCHAR(20) NOT NULL,
    `delivery_id` VARCHAR(20),
    `sales_order_id` VARCHAR(20),
    `billing_type` VARCHAR(20) NOT NULL,
    `invoice_date` DATE NOT NULL,
    `billing_date` DATE NOT NULL,
    `sales_org` VARCHAR(4) COMMENT '销售组织代码',
    `distribution_channel` VARCHAR(2) COMMENT '分销渠道代码',
    `division` VARCHAR(2) COMMENT '产品组/事业部代码',
    `shipping_point` VARCHAR(20) COMMENT '装运点/发货点',
    `sold_to_party` VARCHAR(20),
    `payer` VARCHAR(20),
    `destination_country` VARCHAR(3) COMMENT '货物目的国家',
    `currency` CHAR(3) DEFAULT 'CNY',
    `total_amount` DECIMAL(15,2),
    `status` VARCHAR(20) NOT NULL DEFAULT 'OPEN' COMMENT 'OPEN/PARTIAL/CLEARED/VOID',
    `remark` TEXT COMMENT '其他补充说明',
    `search_term` VARCHAR(50) COMMENT '辅助检索用关键词',
    PRIMARY KEY (`invoice_id`),
    FOREIGN KEY (`delivery_id`) REFERENCES `delivery` (`delivery_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`sales_order_id`) REFERENCES `sales_order` (`sales_order_id`) ON DELETE SET NULL,
    FOREIGN KEY (`payer`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='发票抬头';

-- 7.2 invoice_item
CREATE TABLE IF NOT EXISTS `invoice_item` (
    `invoice_item_id` VARCHAR(20) NOT NULL,
    `invoice_id` VARCHAR(20) NOT NULL,
    `item_no` INT NOT NULL,
    `material_id` VARCHAR(20) NOT NULL,
    `quantity` DECIMAL(15,3),
    `sales_unit` VARCHAR(10) COMMENT '销售计量单位',
    `unit_price` DECIMAL(15,2),
    `discount` DECIMAL(5,2) COMMENT '折扣百分比或金额',
    `tax_amount` DECIMAL(15,2),
    `net_price` DECIMAL(15,2),
    `item_description` VARCHAR(500) COMMENT '行项目补充说明',
    `remark` TEXT COMMENT '其他补充说明',
    PRIMARY KEY (`invoice_item_id`),
    UNIQUE KEY `uk_invoice_item` (`invoice_id`, `item_no`),
    FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE CASCADE,
    FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='发票行项目';

-- 7.3 open_account_receivable
CREATE TABLE IF NOT EXISTS `open_account_receivable` (
    `open_ar_id` VARCHAR(20) NOT NULL,
    `invoice_id` VARCHAR(20) NOT NULL,
    `receivable_amount` DECIMAL(15,2) NOT NULL,
    `received_amount` DECIMAL(15,2) DEFAULT 0.00,
    `due_date` DATE,
    `status` VARCHAR(20) DEFAULT 'UNPAID' COMMENT 'UNPAID/PARTIAL/OVERDUE',
    `remark` TEXT COMMENT '其他补充说明',
    `search_term` VARCHAR(50) COMMENT '辅助检索用关键词',
    `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`open_ar_id`),
    UNIQUE KEY `uk_ar_invoice` (`invoice_id`),
    FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='未清应收账款';

-- 7.4 closed_account_receivable
CREATE TABLE IF NOT EXISTS `closed_account_receivable` (
    `closed_ar_id` VARCHAR(20) NOT NULL,
    `invoice_id` VARCHAR(20) NOT NULL,
    `receivable_amount` DECIMAL(15,2) NOT NULL,
    `received_amount` DECIMAL(15,2) NOT NULL,
    `created_time` DATETIME,
    `closed_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `remark` TEXT COMMENT '其他补充说明',
    `search_term` VARCHAR(50) COMMENT '辅助检索用关键词',
    PRIMARY KEY (`closed_ar_id`),
    FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='已清应收账款';

-- 7.5 receipt
CREATE TABLE IF NOT EXISTS `receipt` (
    `receipt_id` VARCHAR(20) NOT NULL,
    `invoice_id` VARCHAR(20) NOT NULL,
    `payer` VARCHAR(20) NOT NULL,
    `receipt_amount` DECIMAL(15,2) NOT NULL,
    `receipt_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `payment_method` VARCHAR(20),
    `currency` CHAR(3) DEFAULT 'CNY',
    `reference_no` VARCHAR(50),
    `remark` TEXT COMMENT '其他补充说明',
    `search_term` VARCHAR(50) COMMENT '辅助检索用关键词',
    PRIMARY KEY (`receipt_id`),
    FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`payer`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB COMMENT='收款单';

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- HAKIMI ERP Database Schema (DDL)
-- Usage: mysql -u root -p < schema.sql
-- ============================================

CREATE DATABASE IF NOT EXISTS hakimi_erp DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hakimi_erp;

-- Table: business_partner
CREATE TABLE `business_partner` (
  `bp_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '业务伙伴唯一标识码',
  `bp_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '伙伴类型: 组织/个人/公司',
  `bp_role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色: SOLD_TO/SHIP_TO/PAYER',
  `bp_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '客户/公司/个人名称',
  `country` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT 'CN' COMMENT '所属国家代码',
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所在城市',
  `district` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所在区县',
  `street` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '街道地址',
  `house_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '门牌号码',
  `postal_code` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮政编码',
  `language` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT 'ZH' COMMENT '通信语言',
  `time_zone` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT 'UTC+8' COMMENT '所在时区',
  `transportation_zone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '运输区域代码',
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '固定联系电话',
  `mobile_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号码',
  `fax` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '传真号码',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电子邮箱地址',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'ACTIVE' COMMENT '交易状态: ACTIVE/BLOCK/ARCHIVED',
  `block_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '冻结或禁止交易时填写的原因',
  `data_source` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'MANUAL' COMMENT '数据来源',
  `print_format` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '单据默认打印格式',
  `search_term` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '辅助检索用关键词',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `last_changed_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`bp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='业务伙伴（客户主记录）';

-- Table: material
CREATE TABLE `material` (
  `material_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `material_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `base_unit` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '基本计量单位',
  `standard_price` decimal(15,2) DEFAULT NULL COMMENT '标准价格',
  `weight` decimal(15,3) DEFAULT NULL COMMENT '重量',
  `volume` decimal(15,3) DEFAULT NULL COMMENT '体积',
  `search_term` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stock_quantity` decimal(15,3) DEFAULT '0.000',
  `item_group` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT 'ACTIVE',
  PRIMARY KEY (`material_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='物料主记录';

-- Table: sales_organization
CREATE TABLE `sales_organization` (
  `sales_org_id` varchar(10) NOT NULL COMMENT '销售组织代码',
  `description` varchar(100) NOT NULL COMMENT '描述',
  `distribution_channel` varchar(10) NOT NULL COMMENT '分销渠道',
  `division` varchar(10) NOT NULL COMMENT '产品组/事业部',
  `currency` varchar(3) DEFAULT 'CNY' COMMENT '本位币',
  `country` varchar(3) DEFAULT 'CN' COMMENT '所属国家',
  `status` varchar(10) DEFAULT 'ACTIVE' COMMENT '状态',
  PRIMARY KEY (`sales_org_id`,`distribution_channel`,`division`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: pricing_condition
CREATE TABLE `pricing_condition` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: customer_sales_data
CREATE TABLE `customer_sales_data` (
  `bp_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sales_org` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '销售组织代码',
  `distribution_channel` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分销渠道代码',
  `division` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品组/事业部代码',
  `sales_office` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sales_group` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sales_district` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency` char(3) COLLATE utf8mb4_unicode_ci DEFAULT 'CNY' COMMENT '交易货币',
  `price_group` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_pricing_procedure` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_priority` char(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shipping_condition` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivering_plant` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `max_partial_deliveries` int DEFAULT '9',
  `incoterms` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `account_assignment_group` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tax_classification` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`bp_id`,`sales_org`,`distribution_channel`,`division`),
  CONSTRAINT `customer_sales_data_ibfk_1` FOREIGN KEY (`bp_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户销售区域数据';

-- Table: customer_finance_data
CREATE TABLE `customer_finance_data` (
  `bp_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公司代码',
  `reconciliation_account` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '统驭科目',
  `sort_key` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment_terms` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '付款条件',
  `bank_account_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_country` char(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_key` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_account` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `iban` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_account_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'ACTIVE',
  `card_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `card_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `preferred_card` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`bp_id`,`company_code`),
  CONSTRAINT `customer_finance_data_ibfk_1` FOREIGN KEY (`bp_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户公司代码财务数据';

-- Table: contact
CREATE TABLE `contact` (
  `contact_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bp_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `department` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `position` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `personal_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT 'ACTIVE',
  PRIMARY KEY (`contact_id`),
  KEY `bp_id` (`bp_id`),
  CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`bp_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='联系人';

-- Table: bp_relationship
CREATE TABLE `bp_relationship` (
  `relation_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `relationship_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关系类型',
  `bp_from` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bp_to` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  PRIMARY KEY (`relation_id`),
  KEY `bp_from` (`bp_from`),
  KEY `bp_to` (`bp_to`),
  CONSTRAINT `bp_relationship_ibfk_1` FOREIGN KEY (`bp_from`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
  CONSTRAINT `bp_relationship_ibfk_2` FOREIGN KEY (`bp_to`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='业务伙伴关系';

-- Table: inquiry
CREATE TABLE `inquiry` (
  `inquiry_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inquiry_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'OPEN' COMMENT 'OPEN/CLOSED/CANCELLED',
  `customer_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sold_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_reference` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sales_org` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `distribution_channel` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `division` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `requested_delivery_date` date DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `pricing_date` date DEFAULT NULL,
  `currency` char(3) COLLATE utf8mb4_unicode_ci DEFAULT 'CNY',
  `delivering_plant` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `incoterms` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment_terms` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `net_value` decimal(15,2) DEFAULT NULL,
  `inquiry_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_location` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `max_partial_deliveries` int DEFAULT '9',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`inquiry_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `inquiry_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='询价单抬头';

-- Table: inquiry_item
CREATE TABLE `inquiry_item` (
  `inquiry_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inquiry_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_no` int NOT NULL COMMENT '行号: 10, 20, 30...',
  `material_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_quantity` decimal(15,3) DEFAULT NULL,
  `sales_unit` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `expected_order_value` decimal(15,2) DEFAULT NULL,
  `unit_price` decimal(15,2) DEFAULT NULL,
  `discount` decimal(15,2) DEFAULT NULL,
  `net_price` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`inquiry_item_id`),
  UNIQUE KEY `uk_inquiry_item` (`inquiry_id`,`item_no`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `inquiry_item_ibfk_1` FOREIGN KEY (`inquiry_id`) REFERENCES `inquiry` (`inquiry_id`) ON DELETE CASCADE,
  CONSTRAINT `inquiry_item_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='询价单行项目';

-- Table: quotation
CREATE TABLE `quotation` (
  `quotation_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inquiry_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quotation_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'OPEN',
  `customer_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sold_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `payment_terms` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `incoterms` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `net_value` decimal(15,2) DEFAULT NULL,
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`quotation_id`),
  KEY `customer_id` (`customer_id`),
  KEY `inquiry_id` (`inquiry_id`),
  CONSTRAINT `quotation_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
  CONSTRAINT `quotation_ibfk_2` FOREIGN KEY (`inquiry_id`) REFERENCES `inquiry` (`inquiry_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='报价单抬头';

-- Table: quotation_item
CREATE TABLE `quotation_item` (
  `quotation_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quotation_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_no` int NOT NULL,
  `material_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_quantity` decimal(15,3) DEFAULT NULL,
  `sales_unit` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_price` decimal(15,2) DEFAULT NULL,
  `discount` decimal(15,2) DEFAULT NULL,
  `net_price` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`quotation_item_id`),
  UNIQUE KEY `uk_quotation_item` (`quotation_id`,`item_no`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `quotation_item_ibfk_1` FOREIGN KEY (`quotation_id`) REFERENCES `quotation` (`quotation_id`) ON DELETE CASCADE,
  CONSTRAINT `quotation_item_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='报价单行项目';

-- Table: sales_order
CREATE TABLE `sales_order` (
  `sales_order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quotation_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'OPEN',
  `customer_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sold_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_reference` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `requested_delivery_date` date DEFAULT NULL,
  `pricing_date` date DEFAULT NULL,
  `payment_terms` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `incoterms` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivering_plant` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shipping_condition` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_priority` char(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `billing_block` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_block` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `net_value` decimal(15,2) DEFAULT NULL,
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sales_order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `quotation_id` (`quotation_id`),
  CONSTRAINT `sales_order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
  CONSTRAINT `sales_order_ibfk_2` FOREIGN KEY (`quotation_id`) REFERENCES `quotation` (`quotation_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='销售订单抬头';

-- Table: sales_order_item
CREATE TABLE `sales_order_item` (
  `so_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sales_order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_no` int NOT NULL,
  `material_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_category` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_quantity` decimal(15,3) DEFAULT NULL,
  `confirmed_quantity` decimal(15,3) DEFAULT NULL,
  `sales_unit` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `plant` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `storage_location` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shipping_point` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_price` decimal(15,2) DEFAULT NULL,
  `discount` decimal(15,2) DEFAULT NULL,
  `net_price` decimal(15,2) DEFAULT NULL,
  `availability_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`so_item_id`),
  UNIQUE KEY `uk_sales_order_item` (`sales_order_id`,`item_no`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `sales_order_item_ibfk_1` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_order` (`sales_order_id`) ON DELETE CASCADE,
  CONSTRAINT `sales_order_item_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='销售订单行项目';

-- Table: delivery
CREATE TABLE `delivery` (
  `delivery_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sales_order_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'OPEN/PGI_DONE/CANCELLED',
  `ship_to_party` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `planned_delivery_date` date DEFAULT NULL,
  `planned_gi_date` date DEFAULT NULL,
  `actual_gi_date` datetime DEFAULT NULL,
  `picking_date` date DEFAULT NULL,
  `shipping_point` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`delivery_id`),
  KEY `ship_to_party` (`ship_to_party`),
  KEY `sales_order_id` (`sales_order_id`),
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`ship_to_party`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT,
  CONSTRAINT `delivery_ibfk_2` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_order` (`sales_order_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='交货单抬头';

-- Table: delivery_item
CREATE TABLE `delivery_item` (
  `delivery_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_no` int NOT NULL,
  `so_item_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `material_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_quantity` decimal(15,3) DEFAULT NULL,
  `sales_unit` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `item_description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`delivery_item_id`),
  UNIQUE KEY `uk_delivery_item` (`delivery_id`,`item_no`),
  KEY `material_id` (`material_id`),
  KEY `so_item_id` (`so_item_id`),
  CONSTRAINT `delivery_item_ibfk_1` FOREIGN KEY (`delivery_id`) REFERENCES `delivery` (`delivery_id`) ON DELETE CASCADE,
  CONSTRAINT `delivery_item_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT,
  CONSTRAINT `delivery_item_ibfk_3` FOREIGN KEY (`so_item_id`) REFERENCES `sales_order_item` (`so_item_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='交货单行项目';

-- Table: goods_issue
CREATE TABLE `goods_issue` (
  `goods_issue_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `actual_quantity` decimal(15,3) NOT NULL,
  `posting_date` date NOT NULL,
  `goods_issue_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `warehouse` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`goods_issue_id`),
  KEY `delivery_item_id` (`delivery_item_id`),
  CONSTRAINT `goods_issue_ibfk_1` FOREIGN KEY (`delivery_item_id`) REFERENCES `delivery_item` (`delivery_item_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='发货过账';

-- Table: invoice
CREATE TABLE `invoice` (
  `invoice_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sales_order_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `billing_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invoice_date` date NOT NULL,
  `billing_date` date NOT NULL,
  `sold_to_party` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payer` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency` char(3) COLLATE utf8mb4_unicode_ci DEFAULT 'CNY',
  `total_amount` decimal(15,2) DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'OPEN' COMMENT 'OPEN/PARTIAL/CLEARED/VOID',
  PRIMARY KEY (`invoice_id`),
  KEY `delivery_id` (`delivery_id`),
  KEY `sales_order_id` (`sales_order_id`),
  KEY `payer` (`payer`),
  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`delivery_id`) REFERENCES `delivery` (`delivery_id`) ON DELETE RESTRICT,
  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_order` (`sales_order_id`) ON DELETE SET NULL,
  CONSTRAINT `invoice_ibfk_3` FOREIGN KEY (`payer`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='发票抬头';

-- Table: invoice_item
CREATE TABLE `invoice_item` (
  `invoice_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invoice_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_no` int NOT NULL,
  `material_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(15,3) DEFAULT NULL,
  `unit_price` decimal(15,2) DEFAULT NULL,
  `tax_amount` decimal(15,2) DEFAULT NULL,
  `net_price` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`invoice_item_id`),
  UNIQUE KEY `uk_invoice_item` (`invoice_id`,`item_no`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `invoice_item_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE CASCADE,
  CONSTRAINT `invoice_item_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `material` (`material_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='发票行项目';

-- Table: open_account_receivable
CREATE TABLE `open_account_receivable` (
  `open_ar_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invoice_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receivable_amount` decimal(15,2) NOT NULL,
  `received_amount` decimal(15,2) DEFAULT '0.00',
  `due_date` date DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'UNPAID' COMMENT 'UNPAID/PARTIAL/OVERDUE',
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`open_ar_id`),
  UNIQUE KEY `uk_ar_invoice` (`invoice_id`),
  CONSTRAINT `open_account_receivable_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='未清应收账款';

-- Table: closed_account_receivable
CREATE TABLE `closed_account_receivable` (
  `closed_ar_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invoice_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receivable_amount` decimal(15,2) NOT NULL,
  `received_amount` decimal(15,2) NOT NULL,
  `created_time` datetime DEFAULT NULL,
  `closed_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`closed_ar_id`),
  KEY `invoice_id` (`invoice_id`),
  CONSTRAINT `closed_account_receivable_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='已清应收账款';

-- Table: receipt
CREATE TABLE `receipt` (
  `receipt_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invoice_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payer` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receipt_amount` decimal(15,2) NOT NULL,
  `receipt_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency` char(3) COLLATE utf8mb4_unicode_ci DEFAULT 'CNY',
  `reference_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`receipt_id`),
  KEY `invoice_id` (`invoice_id`),
  KEY `payer` (`payer`),
  CONSTRAINT `receipt_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`) ON DELETE RESTRICT,
  CONSTRAINT `receipt_ibfk_2` FOREIGN KEY (`payer`) REFERENCES `business_partner` (`bp_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收款单';

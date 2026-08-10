-- =====================================================
-- ERP Schema Migration: ORM vs DB alignment
-- =====================================================

USE hakimi_erp;

-- 1. inquiry: add 6 missing columns
ALTER TABLE inquiry
  ADD COLUMN sales_area VARCHAR(100) NULL AFTER ship_to_party,
  ADD COLUMN customer_reference_date DATE NULL AFTER customer_reference,
  ADD COLUMN sales_office VARCHAR(10) NULL AFTER division,
  ADD COLUMN sales_group VARCHAR(10) NULL AFTER sales_office,
  ADD COLUMN remark TEXT NULL,
  ADD COLUMN search_term VARCHAR(20) NULL;

-- 2. inquiry_item: add 2 missing columns
ALTER TABLE inquiry_item
  ADD COLUMN remark TEXT NULL,
  ADD COLUMN search_term VARCHAR(20) NULL;

-- 3. quotation: add 17 missing columns
ALTER TABLE quotation
  ADD COLUMN sales_area VARCHAR(100) NULL AFTER ship_to_party,
  ADD COLUMN customer_reference VARCHAR(50) NULL AFTER sales_area,
  ADD COLUMN customer_reference_date DATE NULL AFTER customer_reference,
  ADD COLUMN sales_org VARCHAR(10) NULL AFTER customer_reference_date,
  ADD COLUMN distribution_channel VARCHAR(10) NULL AFTER sales_org,
  ADD COLUMN division VARCHAR(10) NULL AFTER distribution_channel,
  ADD COLUMN sales_office VARCHAR(10) NULL AFTER division,
  ADD COLUMN sales_group VARCHAR(10) NULL AFTER sales_office,
  ADD COLUMN requested_delivery_date DATE NULL AFTER sales_group,
  ADD COLUMN pricing_date DATE NULL AFTER valid_to,
  ADD COLUMN currency VARCHAR(3) DEFAULT 'CNY' NULL AFTER pricing_date,
  ADD COLUMN delivering_plant VARCHAR(20) NULL AFTER incoterms,
  ADD COLUMN max_partial_deliveries INT DEFAULT 9 NULL,
  ADD COLUMN quotation_address VARCHAR(255) NULL,
  ADD COLUMN remark TEXT NULL,
  ADD COLUMN search_term VARCHAR(20) NULL,
  ADD COLUMN created_by VARCHAR(20) NULL;

-- 4. quotation_item: add 4 missing columns
ALTER TABLE quotation_item
  ADD COLUMN item_description VARCHAR(255) NULL AFTER material_id,
  ADD COLUMN expected_order_value DECIMAL(15,2) NULL AFTER order_quantity,
  ADD COLUMN remark TEXT NULL,
  ADD COLUMN search_term VARCHAR(20) NULL;

-- 5. sales_order: add 13 missing columns
ALTER TABLE sales_order
  ADD COLUMN reference_type VARCHAR(1) NULL AFTER order_type,
  ADD COLUMN reference_document VARCHAR(20) NULL AFTER reference_type,
  ADD COLUMN customer_reference_date DATE NULL AFTER customer_reference,
  ADD COLUMN sales_org VARCHAR(10) NULL AFTER customer_reference_date,
  ADD COLUMN distribution_channel VARCHAR(10) NULL AFTER sales_org,
  ADD COLUMN division VARCHAR(10) NULL AFTER distribution_channel,
  ADD COLUMN sales_office VARCHAR(10) NULL AFTER division,
  ADD COLUMN sales_group VARCHAR(10) NULL AFTER sales_office,
  ADD COLUMN currency VARCHAR(3) DEFAULT 'CNY' NULL AFTER pricing_date,
  ADD COLUMN max_partial_deliveries INT DEFAULT 9 NULL AFTER delivery_block,
  ADD COLUMN remark TEXT NULL,
  ADD COLUMN search_term VARCHAR(20) NULL,
  ADD COLUMN created_by VARCHAR(20) NULL;

-- 6. sales_order_item: add 3 missing columns
ALTER TABLE sales_order_item
  ADD COLUMN item_description VARCHAR(255) NULL AFTER material_id,
  ADD COLUMN remark TEXT NULL,
  ADD COLUMN search_term VARCHAR(20) NULL;

-- 7. delivery: add 1 missing column
ALTER TABLE delivery
  ADD COLUMN created_time DATETIME DEFAULT CURRENT_TIMESTAMP NULL;

-- 8. delivery_item: add 5 missing columns
ALTER TABLE delivery_item
  ADD COLUMN order_quantity DECIMAL(15,3) DEFAULT 0 NULL AFTER material_id,
  ADD COLUMN picked_quantity DECIMAL(15,3) DEFAULT 0 NULL AFTER delivery_quantity,
  ADD COLUMN plant VARCHAR(20) NULL NULL,
  ADD COLUMN storage_location VARCHAR(10) NULL NULL,
  ADD COLUMN item_status VARCHAR(20) DEFAULT 'OPEN' NULL;

-- 9. goods_issue: add 1 missing column
ALTER TABLE goods_issue
  ADD COLUMN batch_no INT DEFAULT 1 NULL;

-- 10. Create pick_record table (missing entirely)
CREATE TABLE IF NOT EXISTS pick_record (
  pick_id VARCHAR(20) NOT NULL PRIMARY KEY,
  delivery_item_id VARCHAR(20) NOT NULL,
  batch_no INT NOT NULL,
  pick_quantity DECIMAL(15,3) NOT NULL DEFAULT 0,
  storage_location VARCHAR(10) NULL,
  pick_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  picked_by VARCHAR(50) NULL,
  CONSTRAINT fk_pick_record_item FOREIGN KEY (delivery_item_id) REFERENCES delivery_item(delivery_item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. Create storage_location table (missing entirely)
CREATE TABLE IF NOT EXISTS storage_location (
  sloc_id VARCHAR(10) NOT NULL PRIMARY KEY,
  sloc_name VARCHAR(100) NOT NULL,
  plant VARCHAR(20) NOT NULL,
  warehouse_no VARCHAR(10) NULL,
  storage_type VARCHAR(20) NULL,
  storage_bin VARCHAR(20) NULL,
  description VARCHAR(255) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. Insert a few storage locations
INSERT INTO storage_location (sloc_id, sloc_name, plant, warehouse_no, storage_type, description) VALUES
  ('SL01', 'Finished Goods A', 'PL01', 'WH01', 'RACK', 'Finished goods storage rack A'),
  ('SL02', 'Finished Goods B', 'PL01', 'WH01', 'RACK', 'Finished goods storage rack B'),
  ('SL03', 'Raw Materials', 'PL01', 'WH02', 'BULK', 'Raw material bulk storage');

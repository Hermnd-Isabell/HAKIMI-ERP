-- HAKIMI ERP: Sync database schema with SQLAlchemy models
-- Date: 2026-08-16
-- Scope: delivery / sales_order / sales_order_item missing columns.
-- IMPORTANT: Run once on databases created before this migration.
-- New installs should use updated schema.sql / 01_init.sql instead.

USE `hakimi_erp`;

ALTER TABLE `delivery`
  ADD COLUMN `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP AFTER `tracking_no`;

ALTER TABLE `sales_order`
  ADD COLUMN `reference_type` VARCHAR(1) DEFAULT NULL AFTER `order_type`,
  ADD COLUMN `reference_document` VARCHAR(20) DEFAULT NULL AFTER `reference_type`,
  ADD COLUMN `customer_reference_date` DATE DEFAULT NULL AFTER `customer_reference`,
  ADD COLUMN `sales_org` VARCHAR(10) DEFAULT NULL AFTER `customer_reference_date`,
  ADD COLUMN `distribution_channel` VARCHAR(10) DEFAULT NULL AFTER `sales_org`,
  ADD COLUMN `division` VARCHAR(10) DEFAULT NULL AFTER `distribution_channel`,
  ADD COLUMN `sales_office` VARCHAR(10) DEFAULT NULL AFTER `division`,
  ADD COLUMN `sales_group` VARCHAR(10) DEFAULT NULL AFTER `sales_office`,
  ADD COLUMN `currency` VARCHAR(3) DEFAULT 'CNY' AFTER `pricing_date`,
  ADD COLUMN `max_partial_deliveries` INT DEFAULT 9 AFTER `delivery_block`,
  ADD COLUMN `remark` TEXT DEFAULT NULL AFTER `max_partial_deliveries`,
  ADD COLUMN `search_term` VARCHAR(20) DEFAULT NULL AFTER `remark`,
  ADD COLUMN `created_by` VARCHAR(20) DEFAULT NULL AFTER `created_time`;

ALTER TABLE `sales_order_item`
  ADD COLUMN `item_description` VARCHAR(255) DEFAULT NULL AFTER `material_id`,
  ADD COLUMN `remark` TEXT DEFAULT NULL AFTER `availability_status`,
  ADD COLUMN `search_term` VARCHAR(20) DEFAULT NULL AFTER `remark`;

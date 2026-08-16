-- HAKIMI ERP: Sync remaining ORM columns with existing databases
-- Date: 2026-08-16
-- Scope: inquiry / quotation / invoice / receivable / receipt missing columns.
-- Run once on databases created before this migration.
-- New installs should use regenerated schema.sql / 01_init.sql instead.

USE `hakimi_erp`;

ALTER TABLE `inquiry`
  ADD COLUMN `sales_area` VARCHAR(100) NULL AFTER `ship_to_party`,
  ADD COLUMN `customer_reference_date` DATE NULL AFTER `customer_reference`,
  ADD COLUMN `sales_office` VARCHAR(10) NULL AFTER `division`,
  ADD COLUMN `sales_group` VARCHAR(10) NULL AFTER `sales_office`,
  ADD COLUMN `remark` TEXT NULL AFTER `inquiry_address`,
  ADD COLUMN `search_term` VARCHAR(20) NULL AFTER `remark`;

ALTER TABLE `inquiry_item`
  ADD COLUMN `remark` TEXT NULL AFTER `net_price`,
  ADD COLUMN `search_term` VARCHAR(20) NULL AFTER `remark`;

ALTER TABLE `quotation`
  ADD COLUMN `sales_area` VARCHAR(100) NULL AFTER `ship_to_party`,
  ADD COLUMN `customer_reference` VARCHAR(50) NULL AFTER `sales_area`,
  ADD COLUMN `customer_reference_date` DATE NULL AFTER `customer_reference`,
  ADD COLUMN `sales_org` VARCHAR(10) NULL AFTER `customer_reference_date`,
  ADD COLUMN `distribution_channel` VARCHAR(10) NULL AFTER `sales_org`,
  ADD COLUMN `division` VARCHAR(10) NULL AFTER `distribution_channel`,
  ADD COLUMN `sales_office` VARCHAR(10) NULL AFTER `division`,
  ADD COLUMN `sales_group` VARCHAR(10) NULL AFTER `sales_office`,
  ADD COLUMN `requested_delivery_date` DATE NULL AFTER `sales_group`,
  ADD COLUMN `pricing_date` DATE NULL AFTER `valid_to`,
  ADD COLUMN `currency` VARCHAR(3) NULL DEFAULT 'CNY' AFTER `pricing_date`,
  ADD COLUMN `delivering_plant` VARCHAR(20) NULL AFTER `incoterms`,
  ADD COLUMN `max_partial_deliveries` INT NULL DEFAULT 9 AFTER `delivering_plant`,
  ADD COLUMN `quotation_address` VARCHAR(255) NULL AFTER `net_value`,
  ADD COLUMN `remark` TEXT NULL AFTER `quotation_address`,
  ADD COLUMN `search_term` VARCHAR(20) NULL AFTER `remark`,
  ADD COLUMN `created_by` VARCHAR(20) NULL AFTER `created_time`;

ALTER TABLE `quotation_item`
  ADD COLUMN `item_description` VARCHAR(255) NULL AFTER `material_id`,
  ADD COLUMN `expected_order_value` DECIMAL(15,2) NULL AFTER `sales_unit`,
  ADD COLUMN `remark` TEXT NULL AFTER `net_price`,
  ADD COLUMN `search_term` VARCHAR(20) NULL AFTER `remark`;

ALTER TABLE `invoice`
  ADD COLUMN `sales_org` VARCHAR(4) NULL AFTER `billing_date`,
  ADD COLUMN `distribution_channel` VARCHAR(2) NULL AFTER `sales_org`,
  ADD COLUMN `division` VARCHAR(2) NULL AFTER `distribution_channel`,
  ADD COLUMN `shipping_point` VARCHAR(20) NULL AFTER `division`,
  ADD COLUMN `destination_country` VARCHAR(3) NULL AFTER `payer`,
  ADD COLUMN `remark` TEXT NULL AFTER `status`,
  ADD COLUMN `search_term` VARCHAR(50) NULL AFTER `remark`;

ALTER TABLE `invoice_item`
  ADD COLUMN `sales_unit` VARCHAR(10) NULL AFTER `quantity`,
  ADD COLUMN `discount` DECIMAL(5,2) NULL AFTER `unit_price`,
  ADD COLUMN `item_description` VARCHAR(500) NULL AFTER `net_price`,
  ADD COLUMN `remark` TEXT NULL AFTER `item_description`;

ALTER TABLE `open_account_receivable`
  ADD COLUMN `remark` TEXT NULL AFTER `status`,
  ADD COLUMN `search_term` VARCHAR(50) NULL AFTER `remark`;

ALTER TABLE `closed_account_receivable`
  ADD COLUMN `remark` TEXT NULL AFTER `closed_time`,
  ADD COLUMN `search_term` VARCHAR(50) NULL AFTER `remark`;

ALTER TABLE `receipt`
  ADD COLUMN `remark` TEXT NULL AFTER `reference_no`,
  ADD COLUMN `search_term` VARCHAR(50) NULL AFTER `remark`;

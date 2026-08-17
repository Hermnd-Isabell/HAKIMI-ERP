-- =====================================================
-- O2C Test Data: Materials + Inquiries + Quotations + Orders + Deliveries
-- =====================================================

USE hakimi_erp;

-- === STEP 1: Fix material table missing columns ===
ALTER TABLE material
  ADD COLUMN category VARCHAR(50) NULL COMMENT '产品类别',
  ADD COLUMN stock_quantity DECIMAL(15,3) DEFAULT 999999 NULL COMMENT '库存数量',
  ADD COLUMN item_group VARCHAR(20) NULL COMMENT '产品组',
  ADD COLUMN status VARCHAR(10) DEFAULT 'ACTIVE' NULL COMMENT '状态';

-- === STEP 2: Update existing materials with real data ===
UPDATE material SET 
  material_name = 'Precision Bearing 6201-ZZ',
  description = 'Deep groove ball bearing, 12mm ID, sealed',
  standard_price = 45.00,
  weight = 0.080,
  volume = 0.000040,
  category = 'Bearings',
  item_group = 'BG01',
  stock_quantity = 5000
WHERE material_id = 'M994';

UPDATE material SET 
  material_name = 'Industrial Seal Ring DN50',
  description = 'O-ring seal, NBR, 50mm diameter',
  standard_price = 12.50,
  weight = 0.020,
  volume = 0.000010,
  category = 'Seals',
  item_group = 'SG01',
  stock_quantity = 10000
WHERE material_id = 'M995';

-- Add 2 more materials for richer test data
INSERT INTO material (material_id, material_name, description, base_unit, standard_price, weight, volume, search_term, category, item_group, stock_quantity, status) VALUES
  ('M996', 'Hydraulic Pump HP-25', 'Hydraulic gear pump, 25 L/min, 250 bar', 'EA', 1280.00, 5.500, 0.008, 'PUMP', 'Pumps', 'PG01', 200, 'ACTIVE'),
  ('M997', 'Steel Shaft D20x500', 'Precision steel shaft, 20mm dia, 500mm length', 'EA', 85.00, 1.230, 0.000157, 'SHAFT', 'Shafts', 'SG02', 800, 'ACTIVE');

-- === STEP 3: Insert Inquiries ===
INSERT INTO inquiry (inquiry_id, inquiry_type, status, customer_id, sold_to_party, ship_to_party, sales_area, customer_reference, customer_reference_date, sales_org, distribution_channel, division, sales_office, sales_group, requested_delivery_date, valid_from, valid_to, pricing_date, currency, delivering_plant, incoterms, payment_terms, max_partial_deliveries, net_value, inquiry_address, remark, search_term, created_time, created_by) VALUES
  ('INQ00001', 'ZINQ', 'CLOSED', 'BP00001', 'BP00001', 'BP00001', 'North China', 'PO-2026-001', '2026-07-15', 'OR01', '10', '10', 'BJ01', 'G01', '2026-08-01', '2026-07-15', '2026-08-31', '2026-07-15', 'CNY', 'PL01', 'EXW', 'NET30', 9, 45500.00, 'Beijing Huaxin Industries, Chaoyang District, Beijing', 'Customer inquiry for precision bearings', 'HUAXIN', '2026-07-15 09:30:00', 'USER01'),
  ('INQ00002', 'ZINQ', 'CLOSED', 'BP00003', 'BP00003', 'BP00003', 'Southwest China', 'PO-2026-077', '2026-07-20', 'OR01', '10', '10', 'CD01', 'G02', '2026-08-05', '2026-07-20', '2026-09-15', '2026-07-20', 'CNY', 'PL01', 'FOB', 'NET45', 9, 12750.00, 'Chengdu Tianyu Machinery, Wuhou District, Chengdu', 'Inquiry for seal rings and shafts', 'TIANYU', '2026-07-20 14:15:00', 'USER01'),
  ('INQ00003', 'ZINQ', 'OPEN', 'BP00005', 'BP00005', 'BP00005', 'Central China', 'PO-2026-103', '2026-08-01', 'OR01', '10', '10', 'WH01', 'G01', '2026-09-15', '2026-08-01', '2026-09-30', '2026-08-01', 'CNY', 'PL01', 'EXW', 'NET30', 9, 12800.00, 'Wuhan Zhengda Hardware, East Lake High-Tech Zone, Wuhan', 'New inquiry for hydraulic pumps', 'ZHENGDA', '2026-08-01 10:00:00', 'USER01');

-- === STEP 4: Insert Inquiry Items ===
INSERT INTO inquiry_item (inquiry_item_id, inquiry_id, item_no, material_id, item_description, order_quantity, sales_unit, expected_order_value, unit_price, discount, net_price, remark, search_term) VALUES
  -- Inquiry 1 items (2 line items)
  ('INQI0001', 'INQ00001', 10, 'M994', 'Precision Bearing 6201-ZZ', 1000.000, 'EA', 45000.00, 45.00, 0.00, 45.00, 'Standard pricing', 'BEARING'),
  ('INQI0002', 'INQ00001', 20, 'M995', 'Industrial Seal Ring DN50', 40.000, 'EA', 500.00, 12.50, 0.00, 12.50, NULL, 'SEAL'),
  -- Inquiry 2 items (2 line items)
  ('INQI0003', 'INQ00002', 10, 'M995', 'Industrial Seal Ring DN50', 1000.000, 'EA', 12500.00, 12.50, 0.00, 12.50, NULL, 'SEAL'),
  ('INQI0004', 'INQ00002', 20, 'M997', 'Steel Shaft D20x500', 3.000, 'EA', 255.00, 85.00, 0.00, 85.00, NULL, 'SHAFT'),
  -- Inquiry 3 items (1 line item)
  ('INQI0005', 'INQ00003', 10, 'M996', 'Hydraulic Pump HP-25', 10.000, 'EA', 12800.00, 1280.00, 0.00, 1280.00, NULL, 'PUMP');

-- === STEP 5: Insert Quotations ===
INSERT INTO quotation (quotation_id, inquiry_id, quotation_type, status, customer_id, sold_to_party, ship_to_party, sales_area, customer_reference, customer_reference_date, sales_org, distribution_channel, division, sales_office, sales_group, requested_delivery_date, valid_from, valid_to, pricing_date, currency, payment_terms, incoterms, delivering_plant, max_partial_deliveries, net_value, quotation_address, remark, search_term, created_time, created_by) VALUES
  ('QT00001', 'INQ00001', 'ZQT', 'CLOSED', 'BP00001', 'BP00001', 'BP00001', 'North China', 'PO-2026-001', '2026-07-15', 'OR01', '10', '10', 'BJ01', 'G01', '2026-08-01', '2026-07-16', '2026-08-31', '2026-07-16', 'CNY', 'NET30', 'EXW', 'PL01', 9, 45500.00, 'Beijing Huaxin Industries, Chaoyang District, Beijing', 'Quotation based on inquiry INQ00001', 'HUAXIN', '2026-07-16 10:00:00', 'USER01'),
  ('QT00002', 'INQ00002', 'ZQT', 'CLOSED', 'BP00003', 'BP00003', 'BP00003', 'Southwest China', 'PO-2026-077', '2026-07-20', 'OR01', '10', '10', 'CD01', 'G02', '2026-08-05', '2026-07-21', '2026-09-15', '2026-07-21', 'CNY', 'NET45', 'FOB', 'PL01', 9, 12775.00, 'Chengdu Tianyu Machinery, Wuhou District, Chengdu', 'Quotation with slight price adjustment on shafts', 'TIANYU', '2026-07-21 11:00:00', 'USER01'),
  ('QT00003', 'INQ00003', 'ZQT', 'OPEN', 'BP00005', 'BP00005', 'BP00005', 'Central China', 'PO-2026-103', '2026-08-01', 'OR01', '10', '10', 'WH01', 'G01', '2026-09-15', '2026-08-02', '2026-09-30', '2026-08-02', 'CNY', 'NET30', 'EXW', 'PL01', 9, 12800.00, 'Wuhan Zhengda Hardware, East Lake High-Tech Zone, Wuhan', 'Quotation pending customer confirmation', 'ZHENGDA', '2026-08-02 09:00:00', 'USER01');

-- === STEP 6: Insert Quotation Items ===
INSERT INTO quotation_item (quotation_item_id, quotation_id, item_no, material_id, item_description, order_quantity, sales_unit, expected_order_value, unit_price, discount, net_price, remark, search_term) VALUES
  -- Quotation 1 items
  ('QTI0001', 'QT00001', 10, 'M994', 'Precision Bearing 6201-ZZ', 1000.000, 'EA', 45000.00, 45.00, 0.00, 45.00, NULL, 'BEARING'),
  ('QTI0002', 'QT00001', 20, 'M995', 'Industrial Seal Ring DN50', 40.000, 'EA', 500.00, 12.50, 0.00, 12.50, NULL, 'SEAL'),
  -- Quotation 2 items (shaft price adjusted slightly)
  ('QTI0003', 'QT00002', 10, 'M995', 'Industrial Seal Ring DN50', 1000.000, 'EA', 12500.00, 12.50, 0.00, 12.50, NULL, 'SEAL'),
  ('QTI0004', 'QT00002', 20, 'M997', 'Steel Shaft D20x500', 3.000, 'EA', 255.00, 85.00, 0.00, 85.00, NULL, 'SHAFT'),
  -- Quotation 3 items
  ('QTI0005', 'QT00003', 10, 'M996', 'Hydraulic Pump HP-25', 10.000, 'EA', 12800.00, 1280.00, 0.00, 1280.00, NULL, 'PUMP');

-- === STEP 7: Insert Sales Orders ===
INSERT INTO sales_order (sales_order_id, quotation_id, order_type, reference_type, reference_document, status, customer_id, sold_to_party, ship_to_party, customer_reference, customer_reference_date, sales_org, distribution_channel, division, sales_office, sales_group, requested_delivery_date, pricing_date, currency, payment_terms, incoterms, delivering_plant, shipping_condition, delivery_priority, billing_block, delivery_block, max_partial_deliveries, net_value, remark, search_term, created_time, created_by) VALUES
  ('SO00001', 'QT00001', 'ZOR', 'B', 'QT00001', 'COMPLETED', 'BP00001', 'BP00001', 'BP00001', 'PO-2026-001', '2026-07-15', 'OR01', '10', '10', 'BJ01', 'G01', '2026-08-01', '2026-07-17', 'CNY', 'NET30', 'EXW', 'PL01', '01', '02', NULL, NULL, 9, 45500.00, 'Order from quotation QT00001', 'HUAXIN', '2026-07-17 14:00:00', 'USER01'),
  ('SO00002', 'QT00002', 'ZOR', 'B', 'QT00002', 'IN_PROCESS', 'BP00003', 'BP00003', 'BP00003', 'PO-2026-077', '2026-07-20', 'OR01', '10', '10', 'CD01', 'G02', '2026-08-05', '2026-07-22', 'CNY', 'NET45', 'FOB', 'PL01', '02', '03', NULL, NULL, 9, 12775.00, 'Order from quotation QT00002', 'TIANYU', '2026-07-22 09:30:00', 'USER01'),
  ('SO00003', NULL, 'ZOR', NULL, NULL, 'OPEN', 'BP00007', 'BP00007', 'BP00007', 'PO-2026-200', '2026-08-03', 'OR01', '10', '10', 'SZ01', 'G01', '2026-08-20', '2026-08-03', 'CNY', 'NET30', 'EXW', 'PL01', '01', '02', NULL, NULL, 9, 6400.00, 'Direct order, no quotation reference', 'HENGLI', '2026-08-03 15:00:00', 'USER01');

-- === STEP 8: Insert Sales Order Items ===
INSERT INTO sales_order_item (so_item_id, sales_order_id, item_no, material_id, item_description, item_category, order_quantity, confirmed_quantity, sales_unit, plant, storage_location, shipping_point, unit_price, discount, net_price, availability_status, remark, search_term) VALUES
  -- SO1 items (from Quotation 1)
  ('SOI0001', 'SO00001', 10, 'M994', 'Precision Bearing 6201-ZZ', 'TAN', 1000.000, 1000.000, 'EA', 'PL01', 'SL01', 'SP01', 45.00, 0.00, 45.00, 'AVAILABLE', NULL, 'BEARING'),
  ('SOI0002', 'SO00001', 20, 'M995', 'Industrial Seal Ring DN50', 'TAN', 40.000, 40.000, 'EA', 'PL01', 'SL01', 'SP01', 12.50, 0.00, 12.50, 'AVAILABLE', NULL, 'SEAL'),
  -- SO2 items (from Quotation 2)
  ('SOI0003', 'SO00002', 10, 'M995', 'Industrial Seal Ring DN50', 'TAN', 1000.000, 1000.000, 'EA', 'PL01', 'SL01', 'SP01', 12.50, 0.00, 12.50, 'AVAILABLE', NULL, 'SEAL'),
  ('SOI0004', 'SO00002', 20, 'M997', 'Steel Shaft D20x500', 'TAN', 3.000, 3.000, 'EA', 'PL01', 'SL03', 'SP01', 85.00, 0.00, 85.00, 'AVAILABLE', NULL, 'SHAFT'),
  -- SO3 items (direct order)
  ('SOI0005', 'SO00003', 10, 'M994', 'Precision Bearing 6201-ZZ', 'TAN', 100.000, 100.000, 'EA', 'PL01', 'SL01', 'SP01', 45.00, 5.00, 40.00, 'AVAILABLE', '5% discount for direct order', 'BEARING'),
  ('SOI0006', 'SO00003', 20, 'M996', 'Hydraulic Pump HP-25', 'TAN', 3.000, 2.000, 'EA', 'PL01', 'SL02', 'SP01', 1280.00, 200.00, 1080.00, 'PARTIAL', 'Only 2 available, 1 backordered', 'PUMP');

-- === STEP 9: Insert Deliveries ===
INSERT INTO delivery (delivery_id, sales_order_id, delivery_type, delivery_status, ship_to_party, planned_delivery_date, planned_gi_date, actual_gi_date, picking_date, shipping_point, carrier, driver_name, route, tracking_no, created_time) VALUES
  -- Delivery for SO1 (completed PGI)
  ('DLV00001', 'SO00001', 'LF', 'COMPLETED', 'BP00001', '2026-07-28', '2026-07-28', '2026-07-28 16:00:00', '2026-07-27', 'SP01', 'SF Express', 'Zhang Wei', 'Beijing-Line-A', 'SF1234567890', '2026-07-27 08:00:00'),
  -- Delivery for SO2 (in transit)
  ('DLV00002', 'SO00002', 'LF', 'IN_TRANSIT', 'BP00003', '2026-08-03', '2026-08-03', '2026-08-03 14:30:00', '2026-08-02', 'SP01', 'JD Logistics', 'Li Ming', 'Chengdu-Line-B', 'JD9876543210', '2026-08-02 09:00:00');

-- === STEP 10: Insert Delivery Items ===
INSERT INTO delivery_item (delivery_item_id, delivery_id, item_no, so_item_id, material_id, order_quantity, delivery_quantity, picked_quantity, sales_unit, plant, storage_location, item_description, item_status) VALUES
  -- Delivery 1 items (matching SO1 items, fully delivered)
  ('DLVI0001', 'DLV00001', 10, 'SOI0001', 'M994', 1000.000, 1000.000, 1000.000, 'EA', 'PL01', 'SL01', 'Precision Bearing 6201-ZZ', 'COMPLETED'),
  ('DLVI0002', 'DLV00001', 20, 'SOI0002', 'M995', 40.000, 40.000, 40.000, 'EA', 'PL01', 'SL01', 'Industrial Seal Ring DN50', 'COMPLETED'),
  -- Delivery 2 items (matching SO2 items, shipped)
  ('DLVI0003', 'DLV00002', 10, 'SOI0003', 'M995', 1000.000, 1000.000, 1000.000, 'EA', 'PL01', 'SL01', 'Industrial Seal Ring DN50', 'SHIPPED'),
  ('DLVI0004', 'DLV00002', 20, 'SOI0004', 'M997', 3.000, 3.000, 3.000, 'EA', 'PL01', 'SL03', 'Steel Shaft D20x500', 'SHIPPED');

-- === STEP 11: Insert Pick Records ===
INSERT INTO pick_record (pick_id, delivery_item_id, batch_no, pick_quantity, storage_location, pick_date, picked_by) VALUES
  ('PR00001', 'DLVI0001', 1, 1000.000, 'SL01', '2026-07-27 09:00:00', 'Wang Lei'),
  ('PR00002', 'DLVI0002', 1, 40.000, 'SL01', '2026-07-27 09:15:00', 'Wang Lei'),
  ('PR00003', 'DLVI0003', 1, 1000.000, 'SL01', '2026-08-02 10:00:00', 'Zhao Qiang'),
  ('PR00004', 'DLVI0004', 1, 3.000, 'SL03', '2026-08-02 10:30:00', 'Zhao Qiang');

-- === STEP 12: Insert Goods Issues ===
INSERT INTO goods_issue (goods_issue_id, delivery_item_id, actual_quantity, posting_date, goods_issue_time, warehouse, batch_no) VALUES
  ('GI00001', 'DLVI0001', 1000.000, '2026-07-28', '2026-07-28 16:00:00', 'WH01', 1),
  ('GI00002', 'DLVI0002', 40.000, '2026-07-28', '2026-07-28 16:00:00', 'WH01', 1),
  ('GI00003', 'DLVI0003', 1000.000, '2026-08-03', '2026-08-03 14:30:00', 'WH01', 1),
  ('GI00004', 'DLVI0004', 3.000, '2026-08-03', '2026-08-03 14:30:00', 'WH02', 1);

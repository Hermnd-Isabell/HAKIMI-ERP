path = r'D:\HAKIMI-ERP\hakimi-erp\backend\database\01_init.sql'
with open(path, 'r', encoding='utf-8') as f:
    sql = f.read()

checks = ['carrier', 'driver_name', 'route', 'tracking_no', 
          'picked_quantity', 'plant', 'storage_location', 'item_status', 'order_quantity',
          'batch_no', 'pick_record', 'sloc_id', 'sloc_name', 'storage_type']
for c in checks:
    print(c + ': ' + ('YES' if c in sql else 'MISSING'))

print("\n--- pick_record table ---")
idx = sql.find('pick_record')
if idx >= 0:
    print(sql[idx:idx+500])

print("\n--- storage_location table ---")
idx = sql.find('storage_location (warehouse')
if idx >= 0:
    print(sql[idx:idx+500])

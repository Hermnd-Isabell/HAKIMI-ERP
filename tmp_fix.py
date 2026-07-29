with open(r'D:\HAKIMI-ERP\hakimi-erp\frontend\src\views\Home.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# Increase assistant banner vertical padding from 26px to 40px
content = content.replace(
    'padding: 26px 30px;',
    'padding: 36px 32px;'
)

# Increase padding-top on assistant-section
content = content.replace(
    '.assistant-section { margin-top: auto; padding-top: 8px; }',
    '.assistant-section { margin-top: auto; padding-top: 12px; }'
)

# Make the icon and text bigger too
content = content.replace(
    '<svg viewBox="0 0 44 44" width="44" height="44">',
    '<svg viewBox="0 0 52 52" width="52" height="52">'
)

with open(r'D:\HAKIMI-ERP\hakimi-erp\frontend\src\views\Home.vue', 'w', encoding='utf-8') as f:
    f.write(content)
print('Home.vue fixed')

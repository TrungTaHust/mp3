import pandas as pd

df = pd.read_excel('final.xlsx')
if 'version' not in df.columns:
    raise ValueError("Cột 'version' không tồn tại trong file Excel!")

with pd.ExcelWriter('dls.xlsx', engine='xlsxwriter') as writer:
    for version, group in df.groupby('version'):
        sheet_name = str(version)
        group.to_excel(writer, sheet_name=sheet_name, index=False)

print("✅ Đã tách xong theo từng version vào file dls.xlsx")
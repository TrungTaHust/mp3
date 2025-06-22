import pandas as pd

file_path = "dls1.xlsx"

# Đọc dữ liệu
base_df = pd.read_excel(file_path, sheet_name="base")
max_df = pd.read_excel(file_path, sheet_name="max")

# Đổi tên cột trong base (trừ first_name, last_name)
base_rename = {col: f"{col}_base" for col in base_df.columns if col not in ['first_name', 'last_name']}
base_renamed = base_df.rename(columns=base_rename)

# Đổi tên cột trong max (trừ first_name, last_name)
max_rename = {col: f"{col}_max" for col in max_df.columns if col not in ['first_name', 'last_name']}
max_renamed = max_df.rename(columns=max_rename)

# Ghép 2 DataFrame theo first_name và last_name, giữ tất cả cầu thủ base
final_df = pd.merge(
    base_renamed,
    max_renamed,
    how='left',
    on=['first_name', 'last_name']
)

# Các cột _max nếu thiếu (NaN) thì điền 0
max_cols = [col for col in final_df.columns if col.endswith('_max')]
final_df[max_cols] = final_df[max_cols].fillna(0)

# Ghi lại vào sheet 'final' trong cùng file Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    final_df.to_excel(writer, sheet_name='final', index=False)

print("✅ Đã tạo sheet 'final' với dữ liệu ghép base và max, điền 0 cho _max khi không có.")

import pandas as pd
from sklearn.linear_model import LinearRegression

file_path = "dls1.xlsx"

stat_cols = ['spe', 'acc', 'sta', 'str', 'con', 'pas', 'sho', 'tac']

# Đọc dữ liệu
final_df = pd.read_excel(file_path, sheet_name="final")
upgrading_df = pd.read_excel(file_path, sheet_name="upgrading")

# Lọc bỏ các dòng có chỉ số max bằng 0
mask_nonzero = (final_df[[s + "_m" for s in stat_cols]] != 0).all(axis=1)
filtered_df = final_df[mask_nonzero].copy()

# Tính chênh lệch
for stat in stat_cols:
    filtered_df[f"diff_{stat}"] = filtered_df[f"{stat}_m"] - filtered_df[f"{stat}_b"]
filtered_df["diff_rat"] = filtered_df["rate_m"] - filtered_df["rate_b"]

# Học trọng số (LinearRegression positive)
X = filtered_df[[f"diff_{s}" for s in stat_cols]]
y = filtered_df["diff_rat"]
model = LinearRegression(positive=True)
model.fit(X, y)

weights = model.coef_
weights_rounded = [round(w, 4) for w in weights]

# Tạo dataframe trọng số
weight_df = pd.DataFrame({
    "stat": stat_cols,
    "weight": weights_rounded
})

# Dự đoán rating cho upgrading
def estimate_rating(row):
    return sum(row.get(f"{stat}_b", 0) * w for stat, w in zip(stat_cols, weights_rounded))

upgrading_df["estimated_rating"] = upgrading_df.apply(estimate_rating, axis=1)

# Ghi ra file
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    final_df.to_excel(writer, sheet_name="final", index=False)
    upgrading_df.to_excel(writer, sheet_name="upgrading", index=False)
    weight_df.to_excel(writer, sheet_name="weight", index=False)

print("✅ Hoàn tất: học trọng số, dự đoán rating upgrading, ghi ra file.")
print(weight_df)

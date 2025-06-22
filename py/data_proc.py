import pandas as pd
import json
import subprocess

sheet_names = ['20253']
id_sheet = 'ID'

df_id = pd.read_excel('dls.xlsx', sheet_name=id_sheet, engine='openpyxl')
df_id['full_name'] = (df_id['full_name'].astype(str).str.replace(' ', '').str.lower())
id_duplicates = df_id['full_name'][df_id['full_name'].duplicated(keep=False)]
if not id_duplicates.empty:
    print(f"⚠️ Trùng lặp full_name trong sheet '{id_sheet}':")
    print(df_id[df_id['full_name'].isin(id_duplicates)])
else:
    print(f"✅ Không có full_name bị trùng trong sheet '{id_sheet}'.")

full_name_to_id = dict(zip(df_id['full_name'], df_id['ID']))

price_map = {
    861: 2800, 862: 2600, 863: 0, 864: 0,
    851: 2625, 852: 2440, 853: 2165, 854: 1975,
    841: 2460, 842: 2285, 843: 2030, 844: 1850,
    831: 2300, 832: 2130, 833: 1900, 834: 1730,
    821: 2145, 822: 1985, 823: 1770, 824: 1615,
    811: 1995, 812: 1850, 813: 1650, 814: 1500,
    801: 1850, 802: 1715, 803: 1535, 804: 1395,
    791: 1715, 792: 1585, 793: 1420, 794: 1290,
    781: 1585, 782: 1465, 783: 1315, 784: 1195,
    771: 1460, 772: 1345, 773: 1215, 774: 1100,
    761: 1340, 762: 1235, 763: 1115, 764: 1010,
    751: 1225, 752: 1130, 753: 1020, 754: 925,
    741: 1115, 742: 1030, 743: 935, 744: 840,
    731: 1015, 732: 935, 733: 850, 734: 765,
    721: 920, 722: 845, 723: 770, 724: 690,
    711: 830, 712: 760, 713: 695, 714: 620,
    701: 745, 702: 680, 703: 625, 704: 555,
    691: 665, 692: 605, 693: 555, 694: 495,
    681: 590, 682: 535, 683: 495, 684: 435,
    671: 520, 672: 470, 673: 435, 674: 385,
    661: 455, 662: 410, 663: 380, 664: 335,
    651: 400, 652: 355, 653: 335, 654: 290,
    641: 345, 642: 310, 643: 285, 644: 245,
    631: 300, 632: 265, 633: 245, 634: 210,
    621: 255, 622: 220, 623: 210, 624: 175,
    611: 215, 612: 185, 613: 175, 614: 145,
    601: 185, 602: 155, 603: 145, 604: 115,
    591: 155, 592: 130, 593: 120, 594: 90,
    581: 130, 582: 105, 583: 95, 584: 70,
    571: 110, 572: 85, 573: 75, 574: 55,
    561: 95, 562: 75, 563: 60, 564: 40,
    551: 85, 552: 60, 553: 50, 554: 25,
    541: 75, 542: 55, 543: 40, 544: 20,
    531: 70, 532: 50, 533: 35, 534: 15,
    521: 0, 522: 50, 523: 0, 524: 10
}

for sheet in sheet_names:
    df = pd.read_excel('dls.xlsx', sheet_name=sheet, engine='openpyxl')
    df['first_name'] = df['first_name'].fillna("")
    df['last_name'] = df['last_name'].fillna("")

    df['full_name'] = (df['first_name'] + df['last_name']).str.replace(" ", "").str.lower()
    duplicated_full_names = df['full_name'][df['full_name'].duplicated(keep=False)]
    if not duplicated_full_names.empty:
        print(f"⚠️ Sheet '{sheet}' có full_name bị trùng lặp:")
        print(df[df['full_name'].isin(duplicated_full_names)].sort_values(by='full_name'))
    else:
        print(f"✅ Sheet '{sheet}' không có full_name bị trùng.")

    df['last_name'] = df.apply(lambda row: f"{row['last_name']} (old)" if row['updated'] == 0 else row['last_name'],
                               axis=1)
    df['price'] = df['price_id'].map(price_map)
    df['id'] = df['full_name'].map(full_name_to_id)

    df = df.drop(columns=['updated', 'pos_id', 'price_id'])

    data_list = df.to_dict(orient='records')
    file_path = f'{sheet}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    with open('C:/Users/Admin/my-express-app/data.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    # Báo cáo null
    null_summary = df.isnull().sum()
    total_null = null_summary.sum()
    if total_null > 0:
        print(f"Sheet {sheet} chứa {total_null} giá trị null.")
        print("Thống kê số lượng null theo cột:")
        print(null_summary)
        print("Các bản ghi có giá trị null:")
        print(df[df.isnull().any(axis=1)])

    print(f"✅ Đã xử lý xong sheet {sheet} và ghi file JSON/result.")

# Deploy qua Vercel
project_dir = r"C:\Users\Admin\my-express-app"
vercel_path = r"C:\Users\Admin\AppData\Roaming\npm\vercel.cmd"
result = subprocess.run([vercel_path, "--prod"], cwd=project_dir, capture_output=True, text=True, shell=True)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
if result.returncode != 0:
    print("Deploy failed!")
else:
    print("Deploy successful!")
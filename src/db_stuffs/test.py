DATA_DIR = "D:\Projectlads\Face-Mask-Detection\src\db_stuffs\data.csv"
info = []
with open(DATA_DIR) as data:
    for row in data:
        info.append(row.split(',')[1:6])
    info = info[1:]
    print(info)
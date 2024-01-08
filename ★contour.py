
# 注意：本コードは、一日データが作成された前提で、コンター図を作成するものである。
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import japanize_matplotlib  # 日本語文字化け防止
from scipy import interpolate
import os
from scipy.ndimage import zoom

pd.set_option('display.max_columns', 1000)


def get_temp(a, b, df_temp_m):  # 配列
    df = df_temp_m.loc[:, df_temp_m.columns.str.contains(a) & df_temp_m.columns.str.contains(b) & df_temp_m.columns.str.contains(fix)]
    if df.empty == False:
        return df.iat[0, 0]
    elif df.empty == True:
        return 0


date = "2023-07-02"
# 上下温度を出力したい場合は、軸を入力"①","②"...
# fix_list = ["床表面温度","天井表面温度","東壁表面温度","西壁表面温度","床室内側","天井室内側"]
# fix = "③"
fix = "天井表面温度" # ここに床表面温度か天井表面温度を入力
# fix = input("図の種類を入力してください<窓断面,床表面温度,天井表面温度,東壁表面温度,西壁表面温度,床室内側,天井室内側..>:")

book = pd.ExcelFile(r"G:\共有ドライブ\屋上Cadac2021\day\\" + str(date.split("-")[0] + date.split("-")[1] + date.split("-")[2]) + ".xlsx")
df_air = pd.read_excel(book, sheet_name="上下温度", index_col=0)
df_flooring = pd.read_excel(book, sheet_name="床表面温度", index_col=0)
df_ceiling = pd.read_excel(book, sheet_name="天井表面温度", index_col=0)
df_wall = pd.read_excel(book, sheet_name="壁表面温度", index_col=0)
df_screen = pd.read_excel(book, sheet_name="ｽｸﾘｰﾝ", index_col=0)
# df_PCM_f = pd.read_excel(book, sheet_name = "床PCM熱電対", index_col=0)
# df_PCM_c = pd.read_excel(book, sheet_name = "天井PCM熱電対", index_col=0)
df_temp = pd.concat([df_air, df_flooring, df_ceiling, df_wall], axis=1)  # ,df_PCM_f,df_PCM_c, df_screen
df_temp = df_temp.T.drop_duplicates().T  # 重複カラム削除
# 時刻指定
time = "08:00"
     #  "08:30,09:00,09:30,10:00,10:30,11:00,11:30,12:00,12:30,13:00,13:30,14:00,14:30,15:00,15:30,16:00,16:30,17:00"
# time = input("グラフ化したい時刻を入力<hh:mm,hh:mm,hh:mm,...>:")
time_list = time.split(",")
print("time list :", time_list)
print("df_temp", type(df_temp))
os.makedirs(r"G:\\共有ドライブ\\屋上Cadac2021\\contour\\" + str(date), exist_ok=True)

for time in time_list:
    plt.clf()
    hour = (int(time.split(":")[0])) * 60 + int(time.split(":")[1])
    df_temp_m = df_temp.iloc[[hour]]
    # temp = df_temp_m["上下温度_室温"][0]
    # 　床→0000 天井→2400
    new_list = []

    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③0100"] = df_temp_m["ｽｸﾘｰﾝ室内側空気温度c0100"]
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③0600"] = df_temp_m["ｽｸﾘｰﾝ室内側空気温度c0600"]
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③1100"] = df_temp_m["ｽｸﾘｰﾝ室内側空気温度c1100"]
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③1700"] = df_temp_m["ｽｸﾘｰﾝ室内側空気温度c1700"]
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③2200"] = df_temp_m["ｽｸﾘｰﾝ室内側空気温度c2200"]
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③0350"] = (df_temp_m["ｽｸﾘｰﾝ室内側空気温度c0100"] + df_temp_m["ｽｸﾘｰﾝ室内側空気温度c0600"])/2
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③0850"] = (df_temp_m["ｽｸﾘｰﾝ室内側空気温度c0600"] + df_temp_m["ｽｸﾘｰﾝ室内側空気温度c1100"])/2
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③1400"] = (df_temp_m["ｽｸﾘｰﾝ室内側空気温度c1100"] + df_temp_m["ｽｸﾘｰﾝ室内側空気温度c1700"])/2
    # df_temp_m["ｽｸﾘｰﾝ室内側空気温度③2000"] = (df_temp_m["ｽｸﾘｰﾝ室内側空気温度c1700"] + df_temp_m["ｽｸﾘｰﾝ室内側空気温度c2200"])/2

    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0100"] = df_temp_m["ｽｸﾘｰﾝ窓間空気温度c0100"]
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0600"] = df_temp_m["ｽｸﾘｰﾝ窓間空気温度c0600"]
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1100"] = df_temp_m["ｽｸﾘｰﾝ窓間空気温度c1100"]
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1700"] = df_temp_m["ｽｸﾘｰﾝ窓間空気温度c1700"]
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③2200"] = df_temp_m["ｽｸﾘｰﾝ窓間空気温度c2200"]
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0350"] = (df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0100"] + df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0600"])/2
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0800"] = (df_temp_m["ｽｸﾘｰﾝ窓間空気温度③0600"] + df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1100"]) / 2
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1400"] = (df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1100"] + df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1700"])/2
    # df_temp_m["ｽｸﾘｰﾝ窓間空気温度③2000"] = (df_temp_m["ｽｸﾘｰﾝ窓間空気温度③1700"] + df_temp_m["ｽｸﾘｰﾝ窓間空気温度③2200"]) / 2

    for key in df_temp_m.columns:
        if "床表面" in key:
            key = key + "0000"
        elif "天井表面" in key:
            key = key + "2400"
        elif "ｽｸﾘｰﾝ窓間空気温度" or "ｽｸﾘｰﾝ室内側空気温度" in key:
            key = key.replace("ｽｸﾘｰﾝ窓間空気温度", "上下温度O")
            key = key.replace("ｽｸﾘｰﾝ室内側空気温度", "上下温度A")
        new_list.append(key)
    df_temp_m.columns = new_list

    air_t = ["①", "②", "③", "④", "⑤"]
    x_list = []
    y_list = []

    if fix == "床表面温度" or fix == "天井表面温度":  # チェック済み
        x_list = ["①", "②", "③", "④", "⑤"]
        y_list = ["A", "B", "C", "D", "E", "F"]
    elif fix == "床室内側" or fix == "天井室内側":  # PCM温度表示用
        x_list = ["①", "③", "⑤"]
        y_list = ["B", "C", "D", "E"]
    elif "壁表面温度" in fix:
        x_list = ["A", "B", "C", "D", "E"]
        y_list = ["0100", "1100", "2200"]
    elif fix in air_t:   # 窓断面
        x_list = ["A", "AB", "B", "C", "D", "E"]  # ["O", "A", "B", "C", "D", "E"]
        y_list = ["100", "350", "600", "850", "1100", "1400", "1700", "2000", "2200"]

    # 表面温度
    x = np.arange(len(x_list))  # 横軸, 0 1 2 3 4 5,　補間分
    y = np.arange(len(y_list))  # 縦軸, 0 1 2 3 4 5 6 7 8
    # 空気温度分布
    # x = [100, 400, 900, 1800, 2700, 3600]  # 横軸, 長さ,　補間分
    # y = [100, 350, 600, 850, 1100, 1400, 1700, 2000, 2200]  # 縦軸,長さ

    xx, yy = np.meshgrid(x, y)  # 格子点座標の作成
    plt.scatter(xx, yy)
    print("x_list", x_list, "y_list", y_list)
    z_2d = np.zeros((len(y_list), len(x_list)))  # 格子点ごとのデータを初期化0
    print(z_2d)

    for i, a in enumerate(x_list):
        for j, b in enumerate(y_list):
            temp = get_temp(b, a, df_temp_m)
            if not np.isnan(temp):
                z_2d[j, i] = temp

    # 上下温度の350,850,1400等計測していない位置を上下の計測値平均値として補間
    for i, a in enumerate(x_list):
        for j, b in enumerate(y_list):
            if z_2d[j, i] == 0 and z_2d[j + 1, i] != 0 and z_2d[j - 1, i] != 0:
                z_2d[j, i] = (z_2d[j + 1, i] + z_2d[j - 1, i]) / 2
            elif z_2d[j, i] == 0 and z_2d[j, i + 1] != 0 and z_2d[j, i - 1] != 0:
                z_2d[j, i] = (z_2d[j, i + 1] + z_2d[j - 1, i - 1]) / 2
    print(z_2d)

    # 補間必要なし時。以下二行コメントアウト
    f = interpolate.interp2d(x, y, z_2d, kind="cubic")
    z_2d = f(x, y)

    v = np.linspace(20, 30, 21)  # 表面温度
    # v = np.linspace(20, 30, 21)  # PCM温度,室温,2x+1を三番目の数値として入力
    # v = np.linspace(10, 40, 31)  # PCM温度,室温

    plt.contourf(xx, yy, z_2d, v, cmap="jet", extend="both")
    plt.colorbar(ticks=v[::2])  # カラーバー飛ばし表示
    plt.xticks(x, x_list)
    plt.yticks(y, y_list)
    if fix == "床室内側" or fix == "天井室内側":
        fix = fix + "PCM表面温度"
    # plt.title(date + " " + time + " " + fix + " 平均室温" + '{:.1f}'.format(temp))
    time = time.replace(":", "-")

    plt.savefig(r"G:\\共有ドライブ\\屋上Cadac2021\\contour\\" + str(date) + "\\" + str(time) + str(fix) + ".png")
    # plt.show()
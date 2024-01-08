import re
import numpy as np
import sympy as sp
import math

df_lst = []


def func_wind(x):
    wind = round(float(x) / 22.5)
    if wind == 0:
        return 16
    else:
        return wind


hokui = float(35.712678)
toukei = float(139.761989)
hokui_rad = hokui / 180 * np.pi
toukei_rad = toukei / 180 * np.pi

for file in file_list:
    df = pd.read_csv(file, skiprows=13, encoding="cp932", index_col=[3]).iloc[3:, 3:]
    date_str = re.findall(r'[^\\/:*?"<>|\r\n]+$', str(file))
    date_str = re.split("-|_", date_str[0])
    date = date_str[0] + "-" + date_str[1] + "-" + date_str[2]
    df.rename(index=lambda s: date + " " + s, inplace=True)
    if len(df) < 360:
        print(str(file) + "データ欠損")
    df_lst.append(df)

df_10s = pd.concat(df_lst)
print(df_10s.columns)
df_10s.rename(columns={"外気温1": "外気温1", "外気温2": "外気温2"}, inplace=True)
df_10s = df_10s.loc[:,
         ["外気温1", "外気温2", "屋外湿度計", "直達日射計", "屋根上全天日射計", "鉛直面日射計", "IR上向き日射計", "IR下向き日射計", "IR上向き赤外線放射計", "IR下向き赤外線放射計",
          "風向", "風速"]]

df_10s = df_10s.astype("float64")
df_10s.index = pd.to_datetime(df_10s.index)
print(df_10s.index)
# 入力日の前日23時から,最終日の翌日1時まで

# マイナス時0にする
radiation_list = ["直達日射計", "屋根上全天日射計", "鉛直面日射計", "IR上向き日射計", "IR下向き日射計"]
for i in radiation_list:
    df_10s[i] = df_10s[i].mask(df_10s[i] < 0, 0)

# #HASP用計算
df_10s["外気温"] = df_10s["外気温2"]
df_10s["風向"] = df_10s["風向"].apply(func_wind)  # 風向16分位
df_10s["絶対湿度"] = 0.622 * (6.1078 * 10 ** (7.5 * df_10s["外気温"] / (237.3 + df_10s["外気温"])) * df_10s["屋外湿度計"] / 100) / (
            1013.25 - (6.1078 * 10 ** (7.5 * df_10s["外気温"] / (237.3 + df_10s["外気温"])) * df_10s["屋外湿度計"] / 100))

df_10s["通し日数"] = pd.to_datetime(df_10s.index, format="%Y-%m-%d %H:%M:%S").dayofyear.values
df_10s["通し時刻"] = pd.to_datetime(df_10s.index, format="%Y-%m-%d %H:%M:%S").hour.values + pd.to_datetime(df_10s.index,
                                                                                                       format="%Y-%m-%d %H:%M:%S").minute.values / 60

df_10s["shiita0"] = (df_10s["通し日数"] - 1) / 365 * 2 * np.pi
df_10s["太陽赤緯(rad)"] = 0.006918 - 0.399912 * np.cos(df_10s["shiita0"]) + 0.070257 * np.sin(
    df_10s["shiita0"]) - 0.006758 * np.cos(2 * df_10s["shiita0"]) + 0.000907 * np.sin(
    2 * df_10s["shiita0"]) - 0.002697 * np.cos(3 * df_10s["shiita0"]) + 0.00148 * np.sin(3 * df_10s["shiita0"])

df_10s["均時差(rad)"] = 0.000075 + 0.001868 * np.cos(df_10s["shiita0"]) - 0.032077 * np.sin(
    df_10s["shiita0"]) - 0.014615 * np.cos(2 * df_10s["shiita0"]) - 0.040849 * np.sin(2 * df_10s["shiita0"])
df_10s["均時差(度)"] = df_10s["均時差(rad)"] / np.pi * 180

df_10s["時角(rad)"] = (df_10s["通し時刻"] - 12) / 12 * np.pi + (toukei - 135) / 180 * np.pi + df_10s["均時差(rad)"]
df_10s["太陽高度(rad)"] = np.arcsin(
    np.sin(hokui_rad) * np.sin(df_10s["太陽赤緯(rad)"]) + np.cos(hokui_rad) * np.cos(df_10s["太陽赤緯(rad)"]) * np.cos(
        df_10s["時角(rad)"]))
df_10s["太陽方位(rad)"] = np.arctan((np.cos(hokui_rad) * np.cos(df_10s["太陽赤緯(rad)"]) * np.sin(df_10s["時角(rad)"])) / (
            np.sin(hokui_rad) * np.sin(df_10s["太陽高度(rad)"]) - np.sin(df_10s["太陽赤緯(rad)"])))
df_10s["太陽高度"] = df_10s["太陽高度(rad)"] / np.pi * 180

# 太陽方位(°)計算
df_10s["太陽方位"] = df_10s["太陽方位(rad)"] / np.pi * 180
df_10s["太陽方位"].where((df_10s["時角(rad)"] < 0) & (df_10s["太陽方位(rad)"] > 0), df_10s["太陽方位"] - 180, inplace=True)
df_10s["太陽方位"].where((df_10s["時角(rad)"] > 0) & (df_10s["太陽方位(rad)"] < 0), df_10s["太陽方位"] + 180, inplace=True)

# df_10s["水平面直達日射量"] = df_10s["法線面直達日射量"] * np.sin(df_10s["太陽高度(rad)"]) # Jdn * sinh
# df_10s["鉛直面直達日射量"] = df_10s["法線面直達日射量"] * np.cos(df_10s["太陽高度(rad)"]) * np.cos(df_10s["太陽方位(rad)"]) # Jdn*cosh*cosa
# df_10s["水平面天空日射量"] = df_10s["屋根上全天日射計"] - df_10s["水平面直達日射量"]
# df_10s["鉛直面天空日射量"] = df_10s["鉛直面日射計"] - df_10s["鉛直面直達日射量"]


df_10s["アルベド"] = 0.1  # 仮
# df_10s["アルベド"] = df_10s["IR下側日射計"] / df_10s["IR上側日射計"]　現状縦置き使えない

df_10s["夜間放射量"] = - 2 * df_10s["IR上向き赤外線放射計"]  # 夜間放射観測値[W/m2]
df_10s["夜間放射量"].mask(df_10s["夜間放射量"] < 0, 0, inplace=True)
# df_10s["error_法線面直達日射量"] = df_10s["直達日射計"] # 過少計測された法線面直達日射
df_10s["水平面全天日射"] = df_10s["屋根上全天日射計"]

# 直散分離 udagawa
df_10s["I0"] = 1370 * (1 + 0.033 * np.cos(2 * np.pi * df_10s["通し日数"] / 365))  # 大気圏外法線面日射量

df_10s["太陽高度"].mask(df_10s["太陽高度"] < 3, 3, inplace=True)
df_10s["太陽高度(rad)"] = df_10s["太陽高度"] * np.pi / 180

# KTt=Ihol/(Io*sinh)
df_10s["KTt"] = df_10s["水平面全天日射"] / (df_10s["I0"] * np.sin(df_10s["太陽高度(rad)"]))
# KTtc=0.5163+0.333sinh+0.00803sinh^2
df_10s["KTtc"] = 0.5163 + 0.333 * np.sin(df_10s["太陽高度(rad)"]) + 0.00803 * np.sin(df_10s["太陽高度(rad)"]) ** 2

# KTt<KTtc Idn=(2.277-1.258*sinh+0.2396sinh^2)Ktt^3Io
df_10s["直散分離_法線面直達日射"] = (2.277 - 1.258 * np.sin(df_10s["太陽高度(rad)"]) + 0.2396 * np.sin(df_10s["太陽高度(rad)"]) ** 2) * \
                         df_10s["KTt"] ** 3 * df_10s["I0"]
# Kt >= Kc Idn=(-0.43+1.43KTt)Io
df_10s["直散分離_法線面直達日射"].mask(df_10s["KTt"] > df_10s["KTtc"], df_10s["I0"] * (-0.43 + 1.43 * df_10s["KTt"]), inplace=True)

df_10s["直散分離_水平面天空日射"] = df_10s["水平面全天日射"] - df_10s["直散分離_法線面直達日射"] * np.sin(df_10s["太陽高度(rad)"])

# DN の計算値が 4.18MJ/(m2h) を超える場合，計算値を 4.18MJ/(m2h) に置き換え，計算値と 4.18MJ/(m2h)との差を水平面の値に換算し，SH に加算。
up_limit = 4.18 * 1000000 / 3600
df_10s["直散分離_水平面天空日射"].mask(df_10s["直散分離_法線面直達日射"] > up_limit,
                            df_10s["水平面全天日射"] - np.sin(df_10s["太陽高度(rad)"]) * up_limit,
                            inplace=True)
df_10s["直散分離_法線面直達日射"].mask(df_10s["直散分離_法線面直達日射"] > up_limit,
                            up_limit, inplace=True)

# 日射量がマイナス時、０に直す
df_10s["直散分離_水平面天空日射"].mask(df_10s["直散分離_水平面天空日射"] < 0, 0, inplace=True)
df_10s["直散分離_法線面直達日射"].mask(df_10s["直散分離_法線面直達日射"] < 0, 0, inplace=True)

df_10s["計算_鉛直面全天日射"] = 0.5 * df_10s["直散分離_水平面天空日射"] + df_10s["直散分離_法線面直達日射"] * np.cos(df_10s["太陽高度(rad)"]) * np.cos(
    df_10s["太陽方位(rad)"])
df_10s["計算_水平面全天日射"] = df_10s["直散分離_水平面天空日射"] + np.sin(df_10s["太陽高度(rad)"]) * df_10s["直散分離_法線面直達日射"]

df_10s["地物反射入り_計算_鉛直面全天日射"] = df_10s["計算_鉛直面全天日射"] + df_10s["アルベド"] * 0.5 * df_10s["計算_鉛直面全天日射"]

# 照度計算
# df_10s["Ces"] = 0.08302 + 0.5358 * math.exp(-17.394 * df_10s["太陽高度(rad)"]) + 0.3818 * math.exp(-3.2899 * df_10s["太陽高度(rad)"])
# df_10s["Ce"] = df_10s["直散分離_水平面天空日射"] / df_10s["計算_水平面全天日射"]
# df_10s["Cle"] = (1 - df_10s["Ce"]) / (1 - df_10s["Ces"])
df_10s["鉛直面直達日射"] = df_10s["直散分離_法線面直達日射"] * np.cos(df_10s["太陽高度(rad)"]) * np.cos(df_10s["太陽方位(rad)"])
df_10s["鉛直面天空日射"] = 0.5 * df_10s["直散分離_水平面天空日射"]
df_10s["鉛直面直達照度"] = 110 * df_10s["鉛直面直達日射"]
df_10s["鉛直面天空照度"] = 120 * df_10s["鉛直面天空日射"]

df_10s.to_csv("10s.csv", encoding="cp932")

df_10s["法線面直達日射量"] = df_10s["直散分離_法線面直達日射"]
df_10s["水平面天空日射量"] = df_10s["直散分離_水平面天空日射"]

# 毎時刻ステップの+-30min平均値
df_10s["外気温"] = df_10s["外気温"].rolling(window=360, center=True).mean()
df_10s["絶対湿度"] = df_10s["絶対湿度"].rolling(window=360, center=True).mean()

# 積算値
df_10s["法線面直達日射量"] = df_10s["直散分離_法線面直達日射"].rolling(window=360, center=True).sum() * 10  # 10s間隔のデータを360個集計,1時間のJ/m2
df_10s["水平面天空日射量"] = df_10s["直散分離_水平面天空日射"].rolling(window=360, center=True).sum() * 10
df_10s["夜間放射量"] = df_10s["夜間放射量"].rolling(window=360, center=True).sum() * 10

# 換算
df_10s["外気温"] = df_10s["外気温"] * 10 + 500  # 気温観測値[℃]*10+500
df_10s["絶対湿度"] = df_10s["絶対湿度"] * 10000  # 絶対湿度[kg/kg]*10000
df_10s["風速"] = df_10s["風速"] * 10
df_10s["法線面直達日射量"] = df_10s["法線面直達日射量"] * 0.000239  # kcal/m2*h
df_10s["水平面天空日射量"] = df_10s["水平面天空日射量"] * 0.000239  # kcal/m2*h
df_10s["夜間放射量"] = df_10s["夜間放射量"] * 0.000239  # kcal/m2*h

print(df_10s)

df_10s.to_csv("df_10s.csv", encoding="cp932")

df_hasp = df_10s.loc[:, ["外気温", "絶対湿度", "法線面直達日射量", "水平面天空日射量", "夜間放射量", "風向", "風速"]]
print(df_hasp)
df_hasp = df_hasp.asfreq("H")

df_hasp.to_csv("hasp.csv", encoding="cp932")
print(df_hasp.head(50))
print(df_hasp.tail(50))
for col in df_hasp.columns:
    df_hasp[col] = df_hasp[col].fillna(df_hasp[col].mean())
    df_hasp[col] = df_hasp[col].astype(int)

    df_hasp[col] = df_hasp[col].astype(str)
    df_hasp[col] = df_hasp[col].apply(lambda x: "{:>3}".format(x))

#     print(df_hasp[col][0])
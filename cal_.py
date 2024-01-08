import pandas as pd
import numpy as np
import datetime
import calendar
import math
import itertools


def cal_sheet(df_all):
    temp_col = [column for column in df_all.columns if "上下温度" in column]
    temp_part = [column for column in temp_col if "0100" or "0600" or "1100" or "1700" or "2200" in column]
    temp_part.remove("上下温度B⑤0100")
    temp_part.remove("上下温度E③1700")
    df_temp = df_all[temp_part]
    # df_all["上下温度_室温"] = df_temp.mean(axis=1)  # 上下温度の全平均を室温として計算
    df_all["上下温度_室温"] = df_temp.mean(axis=1)  # 上下温度の全平均を室温として計算
    df_all["床熱橋部熱流計D"] = -df_all["床熱橋部熱流計D"]
    df_all["床熱橋部熱流計E"] = -df_all["床熱橋部熱流計E"]

    df_all["天井室内側5cm角熱流計D③"] = -df_all["天井室内側5cm角熱流計D③"]
    df_all["天井室内側5cm角熱流計D①"] = -df_all["天井室内側5cm角熱流計D①"]
    df_all["天井室内側5cm角熱流計E①"] = -df_all["天井室内側5cm角熱流計E①"]
    df_all["天井室内側5cm角熱電対C③"] = df_all["天井室内側5㎝角熱電対C3"]

    df_all["keep"] = df_all["天井屋外側5cm角熱流計C⑤"]
    df_all["天井屋外側5cm角熱流計C⑤"] = df_all["天井室内側5cm角熱流計C⑤"]
    df_all["天井室内側5cm角熱流計C⑤"] = df_all["keep"]
    del df_all["keep"]

    # 2307
    df_all["天井10cm角熱流計D①"] = df_all["天井10cm角熱流計D⑤"]
    # 注意：ここは名前が間違っているため、転写
    df_all["ｽｸﾘｰﾝ室内側空気温度b1100"] = df_all["ｽｸﾘｰﾝ室内側空気温度b0100.1"]
    df_all = df_all.drop("ｽｸﾘｰﾝ室内側空気温度b0100.1", axis=1)

    df_all["室内側ｶﾞﾗｽ表面温度b0600"] = df_all["室内側ｶﾞﾗｽ表面温度b1700.1"]
    df_all = df_all.drop("室内側ｶﾞﾗｽ表面温度b1700.1", axis=1)

    df_all["室内側ｶﾞﾗｽ表面熱流計b1100"] = (df_all["室内側ｶﾞﾗｽ表面熱流計b0600"] + df_all["室内側ｶﾞﾗｽ表面熱流計b1700"])/2
    df_all["屋外窓ﾌﾚｰﾑ表面温度②"] = (df_all["屋外窓ﾌﾚｰﾑ表面温度①"] + df_all["屋外窓ﾌﾚｰﾑ表面温度⑤"])/2
    df_all["屋外窓ﾌﾚｰﾑ表面温度③"] = (df_all["屋外窓ﾌﾚｰﾑ表面温度①"] + df_all["屋外窓ﾌﾚｰﾑ表面温度⑤"]) / 2
    df_all["屋外窓ﾌﾚｰﾑ表面温度④"] = (df_all["屋外窓ﾌﾚｰﾑ表面温度①"] + df_all["屋外窓ﾌﾚｰﾑ表面温度⑤"]) / 2
    # df_all["天井屋外側5cm角熱流計A③"] = -df_all["天井屋外側5cm角熱流計A③"]
    # df_all["天井屋外側5cm角熱流計BC③"] = -df_all["天井屋外側5cm角熱流計BC③"]
    #
    # df_all["床室内側5cm角熱流計A③"] = -df_all["床室内側5cm角熱流計A③"]
    # df_all["床室内側5cm角熱流計BC③"] = -df_all["床室内側5cm角熱流計BC③"]
    # df_all["床屋外側5cm角熱流計A③"] = -df_all["床屋外側5cm角熱流計A③"]
    # df_all["床屋外側5cm角熱流計BC③"] = -df_all["床屋外側5cm角熱流計BC③"]
    #
    # df_all["keep"] = df_all["床屋外側5cm角熱流計B③"]
    # df_all["床屋外側5cm角熱流計B③"] = df_all["床室内側5cm角熱流計B③"]
    # df_all["床室内側5cm角熱流計B③"] = -df_all["keep"]
    # del df_all["keep"]
    #
    # df_all["IR下向き赤外線放射計"] += 5.67 * (10 ** (-8)) * (df_all["IR温度"] + 273.15) ** 4
    # df_all["IR上向き赤外線放射計"] += 5.67 * (10 ** (-8)) * (df_all["IR温度"] + 273.15) ** 4
    # df_all["IR推定天空温度ST"] = (df_all["IR上向き赤外線放射計"] / (5.67 * 10 ** -8)) ** (1 / 4) - 273.15
    # df_all["IR推定地表温度GT"] = (df_all["IR下向き赤外線放射計"] / (5.67 * 10 ** -8)) ** (1 / 4) - 273.15

    df_all["keep"] = df_all["床屋外側5cm角熱流計B③"]
    df_all["床屋外側5cm角熱流計B③"] = df_all["床室内側5cm角熱流計B③"]
    df_all["床室内側5cm角熱流計B③"] = -df_all["keep"]
    del df_all["keep"]



    df_all["床室内側5cm角熱流計A③"] = -df_all["床室内側5cm角熱流計A③"]
    df_all["床室内側5cm角熱流計BC③"] = -df_all["床室内側5cm角熱流計BC③"]

    df_all["床屋外側5cm角熱流計A③"] = -df_all["床屋外側5cm角熱流計A③"]
    df_all["床屋外側5cm角熱流計BC③"] = -df_all["床屋外側5cm角熱流計BC③"]

    df_all["keep"] = df_all["床屋外側5cm角熱電対B③"]
    df_all["床屋外側5cm角熱電対B③"] = df_all["床室内側5cm角熱電対B③"]
    df_all["床室内側5cm角熱電対B③"] = df_all["keep"]
    del df_all["keep"]

    return df_all


def d_to_r(degree):
    rad = degree / 180 * np.pi
    return rad


def r_to_d(rad):
    deg = rad / np.pi * 180
    return deg


def cal_solar(date_ymd, df_all):
    hk = 35.712678  # 北緯
    tk = 139.761989  # 東経
    hk_rad = d_to_r(hk)
    tk_rad = d_to_r(tk)
    df_solar = pd.DataFrame(index=df_all.index, columns=[])
    df_solar["通し日数"] = (df_all.index - datetime.datetime(int(date_ymd[0]), 1, 1)).days + 1
    df_solar["通し時刻"] = df_all.index.hour + df_all.index.minute / 60

    df_solar["shiita0"] = (df_solar["通し日数"] - 1) / 365 * 2 * np.pi
    df_solar["太陽赤緯(rad)"] = 0.006918 - 0.399912 * np.cos(df_solar["shiita0"]) + 0.070257 * np.sin(
        df_solar["shiita0"]) - 0.006758 * np.cos(2 * df_solar["shiita0"]) + 0.000907 * np.sin(
        2 * df_solar["shiita0"]) - 0.002697 * np.cos(3 * df_solar["shiita0"]) + 0.00148 * np.sin(
        3 * df_solar["shiita0"])
    df_solar["太陽赤緯(度)"] = r_to_d(df_solar["太陽赤緯(rad)"])
    df_solar["均時差(rad)"] = 0.000075 + 0.001868 * np.cos(df_solar["shiita0"]) - 0.032077 * np.sin(
        df_solar["shiita0"]) - 0.014615 * np.cos(2 * df_solar["shiita0"]) - 0.040849 * np.sin(2 * df_solar["shiita0"])
    df_solar["均時差(度)"] = r_to_d(df_solar["均時差(rad)"])
    df_solar["時角(rad)"] = (df_solar["通し時刻"] - 12) / 12 * np.pi + (tk - 135) / 180 * np.pi + df_solar["均時差(rad)"]
    df_solar["太陽高度(rad)"] = np.arcsin(np.sin(hk_rad) * np.sin(df_solar["太陽赤緯(rad)"]) + np.cos(hk_rad) * np.cos(
            df_solar["太陽赤緯(rad)"]) * np.cos(df_solar["時角(rad)"]))
    df_solar["太陽高度(度)"] = r_to_d(df_solar["太陽高度(rad)"])

    # 真南として計算 窓方位角0　gamma =太陽方位角 220619岸本　西面対応90追記 123行目
    wallr = 0 # 壁面方位角
    direc = 90
    df_solar["太陽方位(rad)"] = np.arccos(
        (np.sin(df_solar["太陽高度(rad)"]) * np.sin(hk_rad) - np.sin(df_solar["太陽赤緯(rad)"])) /
        (np.cos(df_solar["太陽高度(rad)"]) * np.cos(hk_rad)))
    df_solar["太陽方位(度)"] = - r_to_d(df_solar["太陽方位(rad)"])
    df_solar["太陽方位(度)"].where(df_solar["時角(rad)"] < 0, - df_solar["太陽方位(度)"], inplace=True)

    df_solar["壁面太陽入射角(rad)"] = 0

    df_solar["壁面太陽入射角(度)"] = df_solar.apply(lambda row: math.degrees(math.acos(
        math.sin(math.radians(row["太陽高度(度)"])) * math.cos(math.radians(direc)) +
        math.cos(math.radians(row["太陽高度(度)"])) * math.sin(math.radians(direc)) *
        math.cos(math.radians(row["太陽方位(度)"] - wallr)))), axis=1)

    df_solar["壁面太陽入射角(rad)"] = d_to_r(df_solar["壁面太陽入射角(度)"])
    return df_solar
# sc : 太陽定数 (日射量の単位と同じ単位で与える)
# nyear, nday : 計算対象年（西暦年）,年間通し日数(1～365,西暦年が閏年なら1～366)
# sh,sA,Aw,beta,albedo : 太陽高度(°),太陽方位角(°),斜面方位角(°),斜面傾斜角（°）地物反射率（0～1）
# Ig,Ib,Id : 水平面全天日射量,法線面直達日射量,水平面天空日射量


def cal_Perez(date_ymd, solar_check, df_all, df_solar):
    def_ = 1  # 熱負荷計算や建物の熱環境評価ではdef=1,dff_ =0は一様天空
    nyear = int(date_ymd[0])
    if calendar.isleap(nyear):
        nday = 366
    else:
        nday = 365
    Aw = 0
    beta = 90
    albedo = 0.1
    dr = np.pi / 180
    k0 = 1.041
    sc = 1370

    # 直達日射計計測値使用時
    if solar_check == 0:
        df_solar["水平面全天日射量"] = df_all["屋根上全天日射計"]
        df_solar["法線面直達日射量"] = df_all["直達日射計"]
    df_solar["水平面全天日射量"].mask(df_solar["水平面全天日射量"] < 10, 0, inplace=True)
    df_solar["法線面直達日射量"].mask(df_solar["法線面直達日射量"] < 10, 0, inplace=True)
    df_solar["水平面天空日射量"] = df_solar["水平面全天日射量"] - df_solar["法線面直達日射量"] * np.sin(df_solar["太陽高度(rad)"])


    # ----------- 入射角の余弦incosの計算----------------------------------------------------
    df_solar["incos"] = np.cos(dr * beta) * np.sin(dr * df_solar["太陽高度(度)"]) + np.sin(dr * beta) * np.cos(
        dr * df_solar["太陽高度(度)"]) * np.cos(dr * (df_solar["太陽方位(度)"] - Aw))
    df_solar["incos"].mask(df_solar["incos"] < 0, 0, inplace=True)

    # ----------非一様分布モデル(Perezモデル）-----------------------------------------------
    # ----------準直達成分,一様成分の係数F1--------------------------------------------------
    F1km = [[-0.008, 0.588, -0.062],
            [0.130, 0.683, -0.151],
            [0.330, 0.487, -0.221],
            [0.568, 0.187, -0.295],
            [0.873, -0.392, -0.362],
            [1.132, -1.237, -0.412],
            [1.062, -1.600, -0.359],
            [0.678, -0.327, -0.250]]
    # ----------地平成分の係数F2-------------------------------------------------------------
    F2km = [[-0.060, 0.072, -0.022],
            [-0.019, 0.066, -0.029],
            [0.055, -0.064, -0.026],
            [0.109, -0.152, -0.014],
            [0.226, -0.462, 0.001],
            [0.288, -0.823, 0.056],
            [0.264, -1.127, 0.131],
            [0.156, -1.377, 0.251]]
    # ----------非一様分布モデルの斜面準直達日射量circum,斜面天空一様日射量backs,-------------
    # ----------地平天空日射量horiz,及び斜面直達日射tiltIb,斜面天空日射tiltIdの計算-----------
    n0 = nyear - 1968
    d0 = 3.71 + 0.2596 * n0 - int((n0 + 3.0) / 4.0)
    m0 = dr * 0.9856 * (nday - d0)
    nyu = m0 + dr * (1.914 * np.sin(m0) + 0.02 * np.sin(2.0 * m0))
    r = 1 + 0.033 * np.cos(nyu)
    extIb = r * sc
    df_solar["Zd"] = 90 - df_solar["太陽高度(度)"]
    df_solar["Z"] = d_to_r(df_solar["Zd"])

    df_solar["a"] = df_solar["incos"]
    df_solar["b"] = np.cos(df_solar["Z"])
    df_solar["b"].mask(df_solar["b"] < 0.087, 0.087, inplace=True)
    df_solar["ep"] = ((df_solar["水平面天空日射量"] + df_solar["法線面直達日射量"]) / df_solar["水平面天空日射量"] + k0 * df_solar[
        "Z"] ** 3.0) / (1.0 + k0 * df_solar["Z"] ** 3.0)

    # print(df_solar["Zd"])
    df_solar["Zd_cal"] = 1 / (93.885 - df_solar["Zd"])  # マイナスあり
    df_solar["Zd_cal"].mask(df_solar["Zd_cal"] < 0, 0, inplace=True)
    df_solar["am"] = 1 / (np.sin(d_to_r(df_solar["太陽高度(度)"])) + 0.15 * df_solar["Zd_cal"].pow(1.253))
    df_solar["de"] = df_solar["水平面天空日射量"] * df_solar["am"] / extIb

    df_solar["m"] = 0
    df_solar["m"].mask(df_solar["ep"] < 1.065, 0, inplace=True)
    df_solar["m"].mask((df_solar["ep"] >= 1.065) & (df_solar["ep"] < 1.23), 1, inplace=True)
    df_solar["m"].mask((df_solar["ep"] >= 1.23) & (df_solar["ep"] < 1.5), 2, inplace=True)
    df_solar["m"].mask((df_solar["ep"] >= 1.5) & (df_solar["ep"] < 1.95), 3, inplace=True)
    df_solar["m"].mask((df_solar["ep"] >= 1.95) & (df_solar["ep"] < 2.8), 4, inplace=True)
    df_solar["m"].mask((df_solar["ep"] >= 2.8) & (df_solar["ep"] < 4.5), 5, inplace=True)
    df_solar["m"].mask((df_solar["ep"] >= 4.5) & (df_solar["ep"] < 6.2), 6, inplace=True)
    df_solar["m"].mask(df_solar["ep"] >= 6.2, 7, inplace=True)

    df_solar["F1k0"] = df_solar["m"].apply(lambda x: F1km[x][0])
    df_solar["F1k1"] = df_solar["m"].apply(lambda x: F1km[x][1])
    df_solar["F1k2"] = df_solar["m"].apply(lambda x: F1km[x][2])
    df_solar["F1"] = df_solar["F1k0"] + df_solar["F1k1"] * df_solar["de"] + df_solar["F1k2"] * df_solar["Z"]
    df_solar["circum"] = df_solar["水平面天空日射量"] * df_solar["F1"] * df_solar["a"] / df_solar["b"]
    df_solar["circum"].mask(df_solar["circum"] < 0, 0, inplace=True)

    df_solar["F2k0"] = df_solar["m"].apply(lambda x: F2km[x][0])
    df_solar["F2k1"] = df_solar["m"].apply(lambda x: F2km[x][1])
    df_solar["F2k2"] = df_solar["m"].apply(lambda x: F2km[x][2])
    df_solar["backs"] = df_solar["水平面天空日射量"] * (1 - df_solar["F1"]) * ((1 + np.cos(dr * beta)) / 2)
    df_solar["F2"] = df_solar["F2k0"] + df_solar["F2k1"] * df_solar["de"] + df_solar["F2k2"] * df_solar["Z"]
    df_solar["horiz"] = df_solar["水平面天空日射量"] * df_solar["F2"] * np.sin(dr * beta)
    df_solar["horiz"].mask(df_solar["horiz"] < 0, 0, inplace=True)

    # ----------- 一様分布モデルの斜面直達日射tiltIb,斜面天空日射tiltIdの計算----------------
    if def_ == 0:  # 一様分布モデル
        df_solar["鉛直面直達日射量"] = df_solar["法線面直達日射量"] * df_solar["incos"]
        df_solar["鉛直面天空日射量"] = df_solar["水平面天空日射量"] * (1 + np.cos(dr * beta))/2
    elif def_ == 1:  # 天空非一様分布(準直達日射を直達日射とする)
        df_solar["鉛直面直達日射量"] = df_solar["法線面直達日射量"] * df_solar["incos"] + df_solar["circum"]
        df_solar["鉛直面天空日射量"] = df_solar["backs"] + df_solar["horiz"]
    else:  # 天空非一様分布(準直達日射を天空日射とする)
        df_solar["鉛直面直達日射量"] = df_solar["法線面直達日射量"] * df_solar["incos"]
        df_solar["鉛直面天空日射量"] = df_solar["circum"] + df_solar["backs"] + df_solar["horiz"]
    # -----------def値による準直達日射circumのtiltIbまたはtiltIdへの組み込み------------------
    # -----------地物による反射日射量の計算（一様分布モデル、非一様分布モデル共通）------------
    df_solar["鉛直面地物反射日射量"] = df_solar["水平面全天日射量"] * albedo * (1 - np.cos(dr * beta))/2
    df_solar["鉛直面全日射量"] = df_solar["鉛直面直達日射量"] + df_solar["鉛直面天空日射量"] + df_solar["鉛直面地物反射日射量"]

    # df_solar.drop(
    #     ["incos", "Zd", "Z", "a", "b", "ep", "am", "de", "m", "F1k0", "F1k1", "F1k2", "F1", "circum", "F2k0", "F2k1",
    #      "F2k2", "backs", "F2", "horiz"], axis=1)
    return df_solar

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 水平面全天日射量,法線面直達日射量,水平面天空日射量から,
    # 任意斜面の直達日射量,天空日射量,地物反射日射量,及び全日射量を計算するプログラム。
    # 天空日射の分布を一様(isotropic)とするか,非一様(anisotropic, Perez et.alによる)とするかをdefにより切り替える。
    # 一様分布モデルを選択する場合は,def=0とする。非一様分布を選択する場合は,準直達日射(circumsolar radiation)を
    # 直達日射に含めるならdef=1,天空日射に含めるならdef=2とする。本プログラムでは,熱負荷計算や建物の熱環境評価では
    # def=1,直達光の制御や太陽光発電のシミュレーションではdef=2を推奨するが,これらの選択はユーザーが決める。
    # 本プログラムを修正すれば,上記以外の組み換えも可能である。
    # -----------合成計算に必要な入力データ（defのみ整数、それ以外は実数）----------------------------------------
    # def_ : def_=0 のとき、天空一様分布
    # def_=1 のとき、天空非一様分布(準直達日射を直達日射とする)
    # def_=2 のとき、天空非一様分布(準直達日射を天空日射とする)

    # ----------プログラムにより得られる計算結果（すべて実数）----------------------------------------------------
    # tiltIb,tiltId,tiltRef,tiltIt : 斜面直達日射量,斜面天空日射量,斜面地物反射日射量,斜面全日射量
    # ---------プログラム内部で定義して使用している主な変数（すべて実数）-----------------------------------------
    # r : 太陽定数から大気外法線面日射量を求める補正係数
    # extIb,Zd, Z, incos : 大気外法線面日射量,天頂角（度), 天頂角(ラジアン）,斜面への日射入射角の余弦
    # circum, horiz, backs : 斜面準直達日射量,斜面地平日射量,斜面一様天空日射量
    # ep,am,de,k1,F1km,F1k,f1,F2km,F2k,F2 : 非一様分布モデルに使用する係数y
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 202005 by H.Akasaka ++++++++++++++++++++++++++
import numpy as np
# 窓枠の袖壁、庇寸法


def cal_shading(df_solar):
    DH = 0.1725
    HR = 2.055
    WR = 1.658
    W1 = 0.067
    W2 = 0.067
    H1 = 0.01
    DVE = 0.1775
    DVW = 0.1775

    # DP、DA計算 220619岸本 西面対応-90追記 16、17行目
    da = np.tan((df_solar["太陽方位(度)"] - 90) * np.pi / 180)
    dp = np.tan((df_solar["太陽高度(度)"]) * np.pi / 180) / np.cos((df_solar["太陽方位(度)"] - 90) * np.pi / 180)
    df_solar["庇DA"] = DH * da
    df_solar["庇DP"] = DH * dp
    df_solar["袖壁東DA"] = - DVE * da
    df_solar["袖壁東DP"] = DVE * dp
    df_solar["袖壁西DA"] = DVW * da
    df_solar["袖壁西DP"] = DVW * dp

    df_solar["庇DHA"] = D_calc("庇", "DHA", df_solar)
    df_solar["庇DHB"] = D_calc("庇", "DHB", df_solar)
    df_solar["庇DWA"] = D_calc("庇", "DWA", df_solar)
    df_solar["庇DWB"] = D_calc("庇", "DWB", df_solar)

    df_solar["袖壁東DHA"] = D_calc("袖壁東", "DHA", df_solar)
    df_solar["袖壁東DHB"] = D_calc("袖壁東", "DHB", df_solar)
    df_solar["袖壁東DWA"] = D_calc("袖壁東", "DWA", df_solar)
    df_solar["袖壁東DWB"] = D_calc("袖壁東", "DWB", df_solar)

    df_solar["袖壁西DHA"] = D_calc("袖壁西", "DHA", df_solar)
    df_solar["袖壁西DHB"] = D_calc("袖壁西", "DHB", df_solar)
    df_solar["袖壁西DWA"] = D_calc("袖壁西", "DWA", df_solar)
    df_solar["袖壁西DWB"] = D_calc("袖壁西", "DWB", df_solar)

    df_solar["庇ASDW"] = ASDW(df_solar["庇DWA"], df_solar["庇DWB"], df_solar["庇DHA"], df_solar["庇DHB"], "庇")
    df_solar["袖壁東ASDW"] = ASDW(df_solar["袖壁東DWA"], df_solar["袖壁東DWB"], df_solar["袖壁東DHA"], df_solar["袖壁東DHB"],
                                 "袖壁東")
    df_solar["袖壁西ASDW"] = ASDW(df_solar["袖壁西DWA"], df_solar["袖壁西DWB"], df_solar["袖壁西DHA"], df_solar["袖壁西DHB"],
                                 "袖壁西")
    return df_solar


def D_calc(situation, cond, df_solar):   # DW計算
    DH = 0.1725
    HR = 2.055
    WR = 1.658
    W1 = 0.067
    W2 = 0.067
    H1 = 0.01
    DVE = 0.1775
    DVW = 0.1775
    DA = df_solar[situation + "DA"]
    DP = df_solar[situation + "DP"]
    if situation == "庇":
        DA = abs(DA)
    #       DA<0時, W1 = W2　解決策まだ。
    cond_dict = {"DHA": [W1 >= DA, W1 < DA],
                 "DHB": [W1 + WR >= DA, W1 + WR < DA],
                 "DWA": [H1 >= DP, H1 < DP],
                 "DWB": [H1 + HR >= DP, H1 + HR < DP]}
    cond_value_hisashi = {"DHA": [DP - H1, W1 * DP / DA - H1],
                          "DHB": [DP - H1, (W1 + WR) * DP / DA - H1],
                          "DWA": [0, (W1 + WR) - H1 * DA / DP],
                          "DWB": [W1 + WR - DA, W1 + WR - (H1 + HR) * DA / DP]}
    cond_value_sodekabe = {"DHA": [0, (H1 + HR) - W1 * DP / DA],
                           "DHB": [H1 + HR - DP, H1 + HR - (W1 + WR) * DP / DA],
                           "DWA": [DA - W1, H1 * DA / DP - W1],
                           "DWB": [DA - W1, (H1 + HR) * DA / DP - W1]}
    condition = cond_dict[cond]
    if situation == "庇":
        value = cond_value_hisashi[cond]
    else:
        value = cond_value_sodekabe[cond]
    if "H" in cond:
        length = HR
    else:
        length = WR
    df_solar[situation + cond] = np.select(condition, value)
    return df_solar[situation + cond].apply(
        lambda x: length if x >= length else (0 if x < 0 else x))  # min max 処理


def ASDW(DWA, DWB, DHA, DHB, situation):
    if situation == "庇":
        return DWA * DHA + 0.5 * (DWA + DWB) * (DHB - DHA)
    else:
        return DHA * DWA + 0.5 * (DHA + DHB) * (DWB - DWA)

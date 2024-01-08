#         if sheetname == "ｽｸﾘｰﾝ":
#             column_index_list = df_sheet.columns.str.contains("ｽｸﾘｰﾝ窓間空気温度")
#             df_sheet["ｽｸﾘｰﾝ窓間空気温度d0600"] = df_sheet["ｽｸﾘｰﾝ窓間空気温度b0600"]
#             df_sheet["ｽｸﾘｰﾝ窓間空気温度d1100"] = df_sheet["ｽｸﾘｰﾝ窓間空気温度b1100"]
# #             column_index_list_icyo1 = [not i1 for i1 in df_sheet.columns.str.contains("ｽｸﾘｰﾝ窓間空気温度d0600")]
# #             column_index_list_icyo2 = [not i2 for i2 in df_sheet.columns.str.contains("ｽｸﾘｰﾝ窓間空気温度d1100")]
# #             column_index_list = column_index_list & column_index_list_icyo1 & column_index_list_icyo2
#             df_sheet["スクリーン窓間空気温度"] = df_sheet.iloc[:, column_index_list].mean(axis=1)

#             #　スクリーン窓間計算
#             s = 0.1115 #　スクリーンと窓間の距離
#             s2 = s * s
#             H = 2.18 # 窓ガラスの高さ
#             W = 1.82
#             kaikouritsu = 0.1
#             Atop = 0.001 * W
#             Abot = 0.001 * W
#             fai = 90 * np.pi / 180
#             Al = 0.001 * H
#             Ar = 0.001 * H
#             Ah = kaikouritsu * H * W

#             df_temp = df_sheet.iloc[:, df_sheet.columns.str.contains("上下温度")]
#             df_sheet["室温"] = df_sheet.drop("上下温度D④0100",axis=1).mean(axis=1) # 断線対応
#             df_sheet["To"] = 283 - 273.15
#             df_sheet["rho"] = 1.293 /( 1 + df_sheet["To"]/ 273.15)
#             df_sheet["粘性係数"] = 1.458 * (10 ** (-6)) * ((df_sheet["スクリーン窓間空気温度"] + 273.15) ** (1.5)) / (df_sheet["スクリーン窓間空気温度"] + 383.55)
#             df_sheet["rho_out"] = 1.293 /( 1 + df_sheet["スクリーン窓間空気温度"]/ 273.15)
#             df_temp = df_sheet.iloc[:, df_sheet.columns.str.contains("上下温度")]

#             Aeqin = Abot + Atop * (Al + Ar + Ah)/(2*(Abot +Atop))
#             Aeqout = Atop + Abot * (Al + Ar + Ah)/(2*(Abot +Atop))
#             Zin = (s * W /(0.66 * Aeqin) - 1) ** (2)
#             Zout = (s * W /(0.60 * Aeqout) - 1) ** (2)
#             df_sheet["Aeqin"] = Aeqin
#             df_sheet["Aeqout"] = Aeqout
#             df_sheet["Zin"] = Zin
#             df_sheet["Zout"] = Zout
#             g = 9.8

#             df_sheet["スクリーン窓間風速v"] = (((((12 * df_sheet["粘性係数"] * H/s2) ** (2)) +
#                                         (2* ((df_sheet["rho_out"])**(2)) *(1+Zin +Zout)* (df_sheet["To"]+273.15) *df_sheet["rho"] *g * H * np.sin(fai) *
#                                          abs(df_sheet["室温"]-df_sheet["スクリーン窓間空気温度"]))/((df_sheet["室温"]+273)*
#                                                                                        (df_sheet["スクリーン窓間空気温度"]+273)))) ** (0.5) -
#                                        12 * df_sheet["粘性係数"] * H/s2)/(df_sheet["rho_out"] * (1 + Zin + Zout))

#             df_sheet["Gr使えない"] = 9.81 * s ** 3 * abs(df_sheet["ガラス室内側表面温度"] - df_sheet["スクリーン表面温度"]) * df_sheet["rho_out"]**2/(df_sheet["スクリーン窓間空気温度"] * df_sheet["粘性係数"] ** 2)
#             df_sheet["Pr使えない"] = df_sheet["粘性係数"] * 1008 / 0.027 # 要修正
#             df_sheet["Nu使えない"] = 0.035 * (df_sheet["Gr"] * df_sheet["Pr"])**0.38
#             df_sheet["hg(hc)使えない"] = df_sheet["Nu"] * ((2.3340 * 0.001 * (df_sheet["スクリーン窓間空気温度"]+273) **(1.5))/ (164.54 + 273 + df_sheet["スクリーン窓間空気温度"]))/s
#             #  コンダクタンス
#             df_sheet["hcv"] = 2 * df_sheet["hg(hc)"] + 4 * df_sheet["スクリーン窓間風速v"]
#             print(df_sheet)
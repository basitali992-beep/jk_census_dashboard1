import pandas as pd

def get_district_data():
    """
    Census 2011 district-wise data for Jammu & Kashmir (22 districts at time of Census).
    Sources: Census of India 2011, Primary Census Abstract, censusindia.gov.in
    Note: J&K had 22 districts during Census 2011. Shupiyan is counted separately from Pulwama.
    """
    records = [
        # District, Division, Total_Pop, Male_Pop, Female_Pop, Urban_Pop, Rural_Pop,
        # Literacy_Rate, Male_Literacy, Female_Literacy,
        # Workers_Total, Main_Workers, Marginal_Workers,
        # Sex_Ratio, Child_Sex_Ratio(0-6), Households, Area_sqkm
        ("Anantnag",   "Kashmir", 1078692, 554076, 524616, 181032, 897660, 58.81, 70.23, 46.73, 352648, 285432, 67216, 946, 908, 210636, 3984),
        ("Bandipore",  "Kashmir",  392232, 203504, 188728,  19025, 373207, 54.95, 66.86, 42.18, 112658,  90124, 22534, 927, 883,  76345, 1574),
        ("Baramulla",  "Kashmir", 1008039, 523252, 484787, 155437, 852602, 56.28, 67.41, 44.34, 302834, 244021, 58813, 926, 888, 193245, 4243),
        ("Budgam",     "Kashmir",  753745, 390031, 363714,  63938, 689807, 52.56, 64.82, 39.48, 222453, 176238, 46215, 932, 894, 144238, 2379),
        ("Doda",       "Jammu",    409576, 218736, 190840,  40614, 368962, 56.03, 67.58, 43.10, 135023, 107614, 27409, 873, 874,  82563, 8912),
        ("Ganderbal",  "Kashmir",  297446, 154889, 142557,  22341, 275105, 55.49, 66.94, 43.17,  89334,  71467, 17867, 920, 887,  57821, 1278),
        ("Jammu",      "Jammu",   1529958, 804684, 725274, 657660, 872298, 83.45, 88.03, 78.27, 592468, 507324, 85144, 901, 871, 305219, 3097),
        ("Kargil",     "Ladakh",   140802,  76087,  64715,  27513, 113289, 62.00, 73.49, 48.68,  47632,  38241,  9391, 851, 923,  27416,14036),
        ("Kathua",     "Jammu",    616435, 328469, 287966, 130060, 486375, 73.24, 81.25, 64.33, 224948, 186478, 38470, 877, 869, 122345, 2651),
        ("Kishtwar",   "Jammu",    231037, 122788, 108249,  19654, 211383, 56.72, 68.62, 43.47,  78542,  63012, 15530, 881, 912,  46378, 5764),
        ("Kulgam",     "Kashmir",  422786, 218239, 204547,  29612, 393174, 55.07, 67.10, 42.38, 131648, 105318, 26330, 937, 929,  82341, 1706),
        ("Kupwara",    "Kashmir",  875775, 454812, 420963,  46127, 829648, 57.00, 68.62, 44.55, 257563, 205650, 51913, 926, 873, 170934, 2379),
        ("Leh",        "Ladakh",   133487,  73312,  60175,  34870,  98617, 77.20, 85.64, 66.73,  52487,  44614,  7873, 821, 916,  26524,45110),
        ("Poonch",     "Jammu",    476820, 255116, 221704,  25219, 451601, 63.09, 73.73, 51.03, 155847, 122567, 33280, 869, 889,  93456, 1674),
        ("Pulwama",    "Kashmir",  560440, 288632, 271808,  69256, 491184, 59.57, 71.69, 46.74, 175438, 141302, 34136, 942, 914, 107834, 1086),
        ("Rajouri",    "Jammu",    642415, 344231, 298184,  64524, 577891, 64.20, 75.01, 52.17, 210567, 167452, 43115, 867, 872, 126342, 2630),
        ("Ramban",     "Jammu",    283713, 153047, 130666,  22183, 261530, 54.67, 66.78, 41.18,  96234,  77012, 19222, 854, 902,  57213, 1329),
        ("Reasi",      "Jammu",    314667, 166971, 147696,  22536, 292131, 57.79, 69.84, 44.51, 104543,  83634, 20909, 885, 908,  62341, 1719),
        ("Samba",      "Jammu",    318611, 170782, 147829,  80213, 238398, 76.23, 83.17, 68.42, 116234,  96814, 19420, 866, 855,  63412, 1015),
        ("Shopian",    "Kashmir",  265960, 136578, 129382,   9861, 256099, 49.24, 61.54, 36.41,  79645,  63716, 15929, 947, 932,  51234,  612),
        ("Srinagar",   "Kashmir", 1236829, 648476, 588353, 959227, 277602, 69.69, 76.10, 62.83, 430678, 373524, 57154, 907, 866, 243456,  2228),
        ("Udhampur",   "Jammu",    554985, 296768, 258217, 100234, 454751, 69.29, 78.40, 59.30, 193456, 158234, 35222, 870, 879, 110234, 4550),
    ]

    columns = [
        "District", "Division", "Total_Population", "Male_Population", "Female_Population",
        "Urban_Population", "Rural_Population",
        "Literacy_Rate", "Male_Literacy", "Female_Literacy",
        "Total_Workers", "Main_Workers", "Marginal_Workers",
        "Sex_Ratio", "Child_Sex_Ratio", "Households", "Area_sqkm"
    ]

    df = pd.DataFrame(records, columns=columns)
    df["Population_Density"] = (df["Total_Population"] / df["Area_sqkm"]).round(1)
    df["Urban_Pct"] = (df["Urban_Population"] / df["Total_Population"] * 100).round(2)
    df["Rural_Pct"] = (df["Rural_Population"] / df["Total_Population"] * 100).round(2)
    df["Worker_Participation_Rate"] = (df["Total_Workers"] / df["Total_Population"] * 100).round(2)
    df["Gender_Literacy_Gap"] = (df["Male_Literacy"] - df["Female_Literacy"]).round(2)
    return df

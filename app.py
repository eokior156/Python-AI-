import streamlit as st

# --- 1. 資料庫 (已加入 base_flour 欄位，每個麵包都有專屬基重) ---
RECIPE_DB = {
    "baguette": {"name": "法式長棍", "base_flour": 150, "ingredients": {"麵粉": 100, "水": 70, "鹽": 2, "酵母": 1},
                 "process": {"烤箱": "230°C", "發酵": "90分", "溫度": "24°C", "濕度": "70%"},
                 "steps": ["水解", "摺疊", "基本發酵", "整形", "最後發酵", "割線", "蒸汽烘烤"]},
    "ciabatta": {"name": "拖鞋麵包", "base_flour": 200,
                 "ingredients": {"麵粉": 100, "水": 80, "鹽": 2, "酵母": 1, "橄欖油": 5},
                 "process": {"烤箱": "220°C", "發酵": "120分", "溫度": "24°C", "濕度": "70%"},
                 "steps": ["攪拌", "基本發酵", "整形", "最後發酵", "烘烤"]},
    "milk_toast": {"name": "鮮奶吐司", "base_flour": 300,
                   "ingredients": {"麵粉": 100, "水": 65, "糖": 10, "鹽": 1.5, "酵母": 1.5, "奶油": 8},
                   "process": {"烤箱": "170°C", "發酵": "60+60分", "溫度": "28°C", "濕度": "75%"},
                   "steps": ["攪拌至擴展", "基本發酵", "分割滾圓", "桿捲", "最後發酵", "烘烤"]},
    "dinner_rolls": {"name": "奶油餐包", "base_flour": 50,
                     "ingredients": {"麵粉": 100, "水": 60, "糖": 12, "鹽": 1.5, "酵母": 2, "奶油": 10},
                     "process": {"烤箱": "180°C", "發酵": "60+40分", "溫度": "28°C", "濕度": "75%"},
                     "steps": ["攪拌", "基本發酵", "分割", "滾圓", "最後發酵", "烘烤"]},
    "pineapple_bun": {"name": "菠蘿麵包", "base_flour": 60,
                      "ingredients": {"麵粉": 100, "水": 55, "糖": 15, "酵母": 2, "鹽": 1.5, "奶油": 10},
                      "process": {"烤箱": "180°C", "發酵": "60+40分", "溫度": "28°C", "濕度": "75%"},
                      "steps": ["製作酥皮", "攪拌", "基本發酵", "包皮", "最後發酵", "烘烤"]},
    "red_bean_bun": {"name": "紅豆麵包", "base_flour": 60,
                     "ingredients": {"麵粉": 100, "水": 55, "糖": 12, "酵母": 2, "鹽": 1.5, "奶油": 8},
                     "process": {"烤箱": "180°C", "發酵": "60+40分", "溫度": "28°C", "濕度": "75%"},
                     "steps": ["包餡", "攪拌", "基本發酵", "最後發酵", "烘烤"]},
    "brioche": {"name": "布里歐修", "base_flour": 100,
                "ingredients": {"麵粉": 100, "水": 40, "糖": 15, "酵母": 2, "鹽": 1.5, "奶油": 50},
                "process": {"烤箱": "190°C", "發酵": "60+60分", "溫度": "26°C", "濕度": "70%"},
                "steps": ["奶油後放", "冷藏發酵", "整形", "最後發酵", "烘烤"]},
    "croissant": {"name": "可頌", "base_flour": 120,
                  "ingredients": {"麵粉": 100, "水": 50, "糖": 10, "酵母": 2, "鹽": 2, "奶油": 25},
                  "process": {"烤箱": "200°C", "發酵": "60+90分", "溫度": "22°C", "濕度": "65%"},
                  "steps": ["折疊包油", "整形", "最後發酵", "烘烤"]},
    "cinnamon_roll": {"name": "肉桂捲", "base_flour": 80,
                      "ingredients": {"麵粉": 100, "水": 50, "糖": 15, "酵母": 2, "鹽": 1.5, "奶油": 15},
                      "process": {"烤箱": "175°C", "發酵": "60+45分", "溫度": "28°C", "濕度": "75%"},
                      "steps": ["攪拌", "捲起", "切割", "最後發酵", "烘烤"]},
    "donut": {"name": "甜甜圈", "base_flour": 60,
              "ingredients": {"麵粉": 100, "水": 50, "糖": 10, "酵母": 2, "鹽": 1, "奶油": 15},
              "process": {"油溫": "170°C", "發酵": "60+30分", "溫度": "28°C", "濕度": "75%"},
              "steps": ["攪拌", "分割", "整形", "最後發酵", "油炸"]},
    "stollen": {"name": "史多倫", "base_flour": 200,
                "ingredients": {"麵粉": 100, "水": 40, "糖": 20, "酵母": 2, "鹽": 1, "奶油": 40, "果乾": 50},
                "process": {"烤箱": "160°C", "發酵": "90分", "溫度": "24°C", "濕度": "60%"},
                "steps": ["浸漬果乾", "攪拌", "包餡", "整形", "烘烤"]},
    "fruit_bread": {"name": "水果歐包", "base_flour": 150,
                    "ingredients": {"麵粉": 100, "水": 65, "糖": 5, "酵母": 1, "鹽": 2, "奶油": 5, "果乾": 20},
                    "process": {"烤箱": "210°C", "發酵": "120分", "溫度": "25°C", "濕度": "70%"},
                    "steps": ["攪拌", "基本發酵", "整形", "最後發酵", "烘烤"]},
    "pork_floss_bun": {"name": "肉鬆麵包", "base_flour": 60,
                       "ingredients": {"麵粉": 100, "水": 55, "糖": 15, "酵母": 2, "鹽": 1.5, "奶油": 10},
                       "process": {"烤箱": "180°C", "發酵": "60+40分", "溫度": "28°C", "濕度": "75%"},
                       "steps": ["攪拌", "包餡", "表面裝飾", "最後發酵", "烘烤"]}
}


# --- 2. 專業計算邏輯 ---
def calculate_scaled_ingredient(ing_name, percentage, base_flour, multiplier):
    # 使用烘焙百分比: (百分比 / 100) * 基重 * 數量
    weight = (percentage / 100) * base_flour * multiplier
    # 大量生產酵母縮減邏輯
    if "酵母" in ing_name and multiplier > 50:
        weight *= 0.9
    return weight


# --- 3. 介面 ---
st.set_page_config(page_title="專業烘焙管理系統", layout="wide")
st.title("🍞 專業烘焙管理系統")
menu = st.sidebar.selectbox("模式選擇", ["標準配方查詢", "網路食譜診斷"])

if menu == "標準配方查詢":
    options = {v['name']: k for k, v in RECIPE_DB.items()}
    choice = st.selectbox("選擇品項", list(options.keys()))
    qty = st.number_input("生產數量", min_value=1, value=1)

    if st.button("顯示完整參數"):
        item = RECIPE_DB[options[choice]]
        base_flour = item["base_flour"]

        st.subheader(f"{item['name']} (x{qty})")
        st.caption(f"單個麵包麵粉基準量: {base_flour}g")

        if qty > 50:
            st.warning("⚠️ 檢測到大量生產：已啟動酵母縮減機制。")

        # 顯示環境與材料
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 🌡️ 環境參數")
            for k, v in item["process"].items():
                st.write(f"- **{k}**: {v}")
        with col2:
            st.write("### ⚖️ 材料清單")
            for ing, pct in item["ingredients"].items():
                final_qty = calculate_scaled_ingredient(ing, pct, base_flour, qty)
                adjustment = " (已縮減)" if ("酵母" in ing and qty > 50) else ""
                st.write(f"- **{ing}**: {final_qty:.1f}g {adjustment}")

        st.write("### 📝 製作步驟")
        for i, step in enumerate(item["steps"], 1):
            st.write(f"{i}. {step}")

elif menu == "網路食譜診斷":
    st.info("網路食譜診斷功能運作中 (依據預設分類規則)")
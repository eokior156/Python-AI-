# 定義丙級檢定食譜的檢查標準 (Constraints)
def check_recipe_feasibility(flour, water, sugar, salt, yeast):
    # 以麵粉為 100% 計算
    hydration = (water / flour) * 100

    # 定義合格範圍 (這就是你的 AI 判斷標準)
    # 假設丙級標準：水份 60-70%, 糖 0-10%, 鹽 1-2%, 酵母 1-2%
    if 60 <= hydration <= 70 and 1 <= salt <= 2 and 1 <= yeast <= 2:
        return True, "配方符合標準！"
    else:
        return False, "配方不合格，調整比例後再試。"


# 測試一個配方
# 輸入: 麵粉=500g, 水=325g, 糖=20g, 鹽=10g, 酵母=5g
is_good, message = check_recipe_feasibility(500, 325, 20, 10, 5)
print(message)


def check_recipe_feasibility(flour, water, sugar, salt, yeast):
    # 計算烘焙百分比 (Baker's Percentage)
    h_pct = (water / flour) * 100
    s_pct = (sugar / flour) * 100
    salt_pct = (salt / flour) * 100
    y_pct = (yeast / flour) * 100

    print(f"--- 目前配方分析 ---")
    print(f"吸水率: {h_pct:.1f}% (標準: 60-70%)")
    print(f"糖佔比: {s_pct:.1f}%")
    print(f"鹽佔比: {salt_pct:.1f}% (標準: 1-2%)")
    print(f"酵母佔比: {y_pct:.1f}% (標準: 1-2%)")
    print("-" * 20)

    # 檢查標準
    if 60 <= h_pct <= 70 and 1 <= salt_pct <= 2 and 1 <= y_pct <= 2:
        return True, "結果：恭喜！此配方符合丙級標準。"
    else:
        return False, "結果：不合格，請調整比例。"


# 這裡是你的輸入區域 (試著調整這些數字看看)
# 例如：麵粉500g, 水325g, 糖20g, 鹽10g, 酵母5g
result, message = check_recipe_feasibility(flour=500, water=325, sugar=20, salt=10, yeast=5)
print(message)


def optimize_recipe(flour, water, sugar, salt, yeast):
    # 計算當前比例
    h_pct = (water / flour) * 100
    salt_pct = (salt / flour) * 100
    y_pct = (yeast / flour) * 100

    # 修正邏輯：如果比例不對，將其強制調整為標準範圍的「中位數」
    # 目標：吸水率 65%, 鹽 1.5%, 酵母 1.5%
    new_water = water
    new_salt = salt
    new_yeast = yeast

    if not (60 <= h_pct <= 70):
        new_water = flour * 0.65  # 強制修正為 65%
        print(f"-> 修正吸水率: {h_pct:.1f}% -> 65.0%")

    if not (1 <= salt_pct <= 2):
        new_salt = flour * 0.015  # 強制修正為 1.5%
        print(f"-> 修正鹽佔比: {salt_pct:.1f}% -> 1.5%")

    if not (1 <= y_pct <= 2):
        new_yeast = flour * 0.015  # 強制修正為 1.5%
        print(f"-> 修正酵母佔比: {y_pct:.1f}% -> 1.5%")

    return new_water, new_salt, new_yeast


# 測試：故意輸入一個不合格的配方
# 假設鹽放太多 (4%)，水太少 (50%)
flour, water, sugar, salt, yeast = 500, 250, 20, 20, 5
print("原配方不合格，執行 AI 修正中...")
new_water, new_salt, new_yeast = optimize_recipe(flour, water, sugar, salt, yeast)

print(f"\n修正後的建議配方:")
print(f"麵粉: {flour}g, 水: {new_water:.1f}g, 鹽: {new_salt:.1f}g, 酵母: {new_yeast:.1f}g")
import math

# --- 1. 完整烘焙資料庫 ---
RECIPE_DB = {
    "pineapple_bun": {"name": "菠蘿麵包", "dough_weight": 60, "proof": (30, 75), "bake": (180, 15),
                      "ingredients": {"flour": 100, "water": 55, "sugar": 15, "yeast": 2, "salt": 1.5, "butter": 10},
                      "steps": ["製作菠蘿皮", "攪拌麵團", "基本發酵", "分割滾圓", "貼皮整形", "最後發酵", "烘烤"]},
    "milk_powder_bun": {"name": "奶酥麵包", "dough_weight": 60, "proof": (28, 80), "bake": (170, 15),
                        "ingredients": {"flour": 100, "water": 55, "sugar": 12, "yeast": 2, "salt": 1.5, "butter": 10},
                        "steps": ["製作奶酥餡", "攪拌麵團", "基本發酵", "包餡", "整形", "最後發酵", "烘烤"]},
    "red_bean_bun": {"name": "紅豆麵包", "dough_weight": 60, "proof": (28, 80), "bake": (170, 15),
                     "ingredients": {"flour": 100, "water": 55, "sugar": 12, "yeast": 2, "salt": 1.5, "butter": 8},
                     "steps": ["準備紅豆餡", "攪拌麵團", "基本發酵", "包餡", "整形", "最後發酵", "烘烤"]},
    "custard_bun": {"name": "卡士達麵包", "dough_weight": 60, "proof": (28, 80), "bake": (170, 15),
                    "ingredients": {"flour": 100, "water": 55, "sugar": 15, "yeast": 2, "salt": 1.5, "butter": 10},
                    "steps": ["製作卡士達餡", "攪拌麵團", "基本發酵", "包餡", "整形", "最後發酵", "烘烤"]},
    "pork_floss_bun": {"name": "肉鬆甜麵包", "dough_weight": 65, "proof": (28, 75), "bake": (175, 15),
                       "ingredients": {"flour": 100, "water": 55, "sugar": 15, "yeast": 2, "salt": 1.5, "butter": 10},
                       "steps": ["處理肉鬆", "攪拌麵團", "基本發酵", "包餡", "表面裝飾", "最後發酵", "烘烤"]},
    "brioche": {"name": "布里歐修", "dough_weight": 50, "proof": (26, 75), "bake": (190, 12),
                "ingredients": {"flour": 100, "water": 40, "sugar": 15, "yeast": 2, "salt": 1.5, "butter": 50},
                "steps": ["攪拌麵團(高油量)", "基本發酵", "冷藏發酵", "整形", "最後發酵", "烘烤"]},
    "croissant": {"name": "可頌", "dough_weight": 70, "proof": (24, 70), "bake": (200, 20),
                  "ingredients": {"flour": 100, "water": 50, "sugar": 10, "yeast": 2, "salt": 2, "butter": 25},
                  "steps": ["攪拌麵團", "包裹奶油", "摺疊擀壓", "整形", "最後發酵", "烘烤"]},
    "danish": {"name": "丹麥麵包", "dough_weight": 70, "proof": (24, 70), "bake": (190, 18),
               "ingredients": {"flour": 100, "water": 45, "sugar": 15, "yeast": 2, "salt": 2, "butter": 30},
               "steps": ["攪拌麵團", "包裹奶油", "摺疊", "包餡", "最後發酵", "烘烤"]},
    "chocolate_bun": {"name": "巧克力麵包", "dough_weight": 60, "proof": (28, 75), "bake": (180, 15),
                      "ingredients": {"flour": 100, "water": 55, "sugar": 15, "cocoa": 5, "yeast": 2, "salt": 1.5,
                                      "butter": 10},
                      "steps": ["攪拌巧克力麵團", "基本發酵", "包入巧克力", "整形", "最後發酵", "烘烤"]},
    "fruit_bread": {"name": "水果麵包", "dough_weight": 150, "proof": (28, 75), "bake": (180, 25),
                    "ingredients": {"flour": 100, "water": 60, "sugar": 10, "yeast": 2, "salt": 1.5, "butter": 15,
                                    "fruit": 30},
                    "steps": ["攪拌麵團", "拌入果乾", "基本發酵", "整形", "最後發酵", "烘烤"]},
    "donut": {"name": "甜甜圈", "dough_weight": 50, "proof": (30, 80), "bake": (180, 3),
              "ingredients": {"flour": 100, "water": 50, "sugar": 10, "yeast": 2, "salt": 1, "butter": 15},
              "steps": ["攪拌麵團", "基本發酵", "分割整形", "最後發酵", "油炸"]},
    "cinnamon_roll": {"name": "肉桂捲", "dough_weight": 80, "proof": (30, 75), "bake": (175, 20),
                      "ingredients": {"flour": 100, "water": 50, "sugar": 15, "yeast": 2, "salt": 1.5, "butter": 15},
                      "steps": ["攪拌麵團", "基本發酵", "抹肉桂餡", "捲起切割", "最後發酵", "烘烤"]},
    "stollen": {"name": "史多倫", "dough_weight": 400, "proof": (26, 70), "bake": (160, 45),
                "ingredients": {"flour": 100, "water": 40, "sugar": 20, "yeast": 2, "salt": 1, "butter": 40,
                                "fruit": 50},
                "steps": ["果乾浸漬", "攪拌麵團", "基本發酵", "包入杏仁膏與果乾", "最後發酵", "烘烤"]}
}


def calculate_ingredients(total_dough, recipe):
    total_pct = sum(recipe["ingredients"].values())
    flour_total = (total_dough / total_pct) * 100
    return {item: round((flour_total * pct) / 100, 1) for item, pct in recipe["ingredients"].items()}


def run_system():
    print(f"目前系統支援品項: {list(RECIPE_DB.keys())}")
    code = input("\n請輸入麵包代碼: ").strip().lower()

    if code not in RECIPE_DB:
        print("查無此品項。")
        return

    item = RECIPE_DB[code]
    qty = int(input(f"請輸入預計生產數量: "))

    # 運算
    total_dough_required = qty * item["dough_weight"]
    material_list = calculate_ingredients(total_dough_required, item)

    print(f"\n--- {item['name']} 生產規格 ---")
    print(f"總麵團需求: {total_dough_required}g")
    print("-" * 30)
    print("【材料清單】:")
    for ing, weight in material_list.items():
        print(f"{ing:8}: {weight}g")

    print("-" * 30)
    print(f"發酵建議: {item['proof'][0]}°C / 濕度 {item['proof'][1]}%")
    print(f"烘烤建議: {item['bake'][0]}°C / {item['bake'][1]} 分鐘")

    print("\n【製作步驟】:")
    for i, step in enumerate(item['steps'], 1):
        print(f"{i}. {step}")

    # 品質檢查
    try:
        actual_temp = float(input("\n請輸入您實測的發酵溫度 (數字): "))
        if abs(actual_temp - item['proof'][0]) > 2:
            print("【警告】: 溫度異常，請檢查環境。")
        else:
            print("【狀態】: 溫度理想。")
    except:
        pass


if __name__ == "__main__":
    run_system()

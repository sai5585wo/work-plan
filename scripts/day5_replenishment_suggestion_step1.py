"""Day 5: replenishment report learning script.

This script grows step by step during learning.
Current covered business questions:
1. Can Python read the replenishment table?
2. Is the existing gap quantity reliable?
3. Which replenishment tasks still need follow-up?
4. Which supplier and cost should be used for replenishment?
"""

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("outputs")
GAP_CHECK_OUTPUT = OUTPUT_DIR / "day5_replenishment_gap_check.csv"
FOLLOWUP_OUTPUT = OUTPUT_DIR / "day5_replenishment_followup.csv"
SUGGESTION_OUTPUT = OUTPUT_DIR / "day5_replenishment_suggestion.csv"

# 业务意思：读取补货采购表，把 CSV 变成 Python 能处理的表格。
replenishment = pd.read_csv("data/replenishment.csv")

# 业务意思：读取商品资料表，后面用来带出供应商和成本。
products = pd.read_csv("data/products.csv")

# 业务意思：确认补货表里哪些列代表关键业务字段。
# 这里用列的位置，是为了避免 Windows 终端偶尔把中文字段名传成乱码。
sku_column = replenishment.columns[0]
product_name_column = replenishment.columns[1]
current_stock_column = replenishment.columns[2]
safety_stock_column = replenishment.columns[3]
inventory_status_column = replenishment.columns[4]
original_gap_column = replenishment.columns[5]
system_suggestion_column = replenishment.columns[7]
replenishment_status_column = replenishment.columns[8]
owner_column = replenishment.columns[9]
arrival_date_column = replenishment.columns[10]

# 业务意思：确认商品资料表里哪些列代表 SKU、供应商和成本。
product_sku_column = products.columns[0]
supplier_column = products.columns[4]
cost_column = products.columns[5]

# 业务意思：用规则重新计算缺口数量。
# 如果安全库存 - 当前库存小于 0，就按 0 处理，因为库存充足时不需要补货。
replenishment["计算缺口数量"] = (
    replenishment[safety_stock_column] - replenishment[current_stock_column]
).clip(lower=0)

# 业务意思：判断原来的缺口数量，是否等于 Python 重新计算出来的缺口数量。
replenishment["缺口是否一致"] = (
    replenishment[original_gap_column] == replenishment["计算缺口数量"]
)

# 业务意思：只显示缺口校验最关心的字段，方便检查。
gap_check_result = replenishment[
    [
        sku_column,
        product_name_column,
        current_stock_column,
        safety_stock_column,
        original_gap_column,
        "计算缺口数量",
        "缺口是否一致",
    ]
]

# 业务意思：筛选真正需要继续跟进的补货任务。
# 条件 1：计算缺口数量大于 0，说明确实还缺货。
# 条件 2：系统建议不是“暂不补货”，说明系统认为需要补。
# 条件 3：补货状态不是“已取消”，说明人工没有取消这个补货任务。
need_follow_up = replenishment[
    (replenishment["计算缺口数量"] > 0)
    & (replenishment[system_suggestion_column] != "暂不补货")
    & (replenishment[replenishment_status_column] != "已取消")
]

# 业务意思：只保留采购/运营当前最需要看的字段。
followup_result = need_follow_up[
    [
        sku_column,
        product_name_column,
        current_stock_column,
        safety_stock_column,
        "计算缺口数量",
        inventory_status_column,
        system_suggestion_column,
        replenishment_status_column,
        owner_column,
        arrival_date_column,
    ]
]

# 业务意思：用 SKU 把补货任务和商品资料连起来，带出供应商和成本。
replenishment_suggestion = need_follow_up.merge(
    products[[product_sku_column, supplier_column, cost_column]],
    left_on=sku_column,
    right_on=product_sku_column,
    how="left",
)

# 业务意思：计算预计补货成本，帮助采购/运营知道这批补货大概要花多少钱。
replenishment_suggestion["预计补货成本"] = (
    replenishment_suggestion["计算缺口数量"] * replenishment_suggestion[cost_column]
)

# 业务意思：整理成采购/运营可直接查看的补货建议表。
suggestion_result = replenishment_suggestion[
    [
        sku_column,
        product_name_column,
        current_stock_column,
        safety_stock_column,
        "计算缺口数量",
        inventory_status_column,
        system_suggestion_column,
        replenishment_status_column,
        supplier_column,
        cost_column,
        "预计补货成本",
        owner_column,
        arrival_date_column,
    ]
]

print("=== 待跟进补货任务 ===")
print(followup_result.to_string(index=False))

print("\n=== 补货建议表 ===")
print(suggestion_result.to_string(index=False))

# 业务意思：同时导出当前已经学过的两个结果，方便后续查看或导入飞书。
OUTPUT_DIR.mkdir(exist_ok=True)
gap_check_result.to_csv(GAP_CHECK_OUTPUT, index=False, encoding="utf-8-sig")
followup_result.to_csv(FOLLOWUP_OUTPUT, index=False, encoding="utf-8-sig")
suggestion_result.to_csv(SUGGESTION_OUTPUT, index=False, encoding="utf-8-sig")

print(f"\n已导出缺口数量校验报表：{GAP_CHECK_OUTPUT}")
print(f"已导出待跟进补货任务：{FOLLOWUP_OUTPUT}")
print(f"已导出补货建议表：{SUGGESTION_OUTPUT}")

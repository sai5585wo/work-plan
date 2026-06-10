"""Day 5 step 1: find SKUs that still need replenishment follow-up.

This small script answers one business question:
which replenishment rows should procurement or operations continue to follow.
"""

import pandas as pd


# 业务意思：读取补货采购表，准备判断哪些 SKU 需要继续跟进补货。
replenishment = pd.read_csv("data/replenishment.csv")

# 业务意思：确认补货表里哪些列代表关键业务字段。
# 这里用列的位置，是为了避免 Windows 终端偶尔把中文字段名传成乱码。
sku_column = replenishment.columns[0]
product_name_column = replenishment.columns[1]
current_stock_column = replenishment.columns[2]
safety_stock_column = replenishment.columns[3]
inventory_status_column = replenishment.columns[4]
system_suggestion_column = replenishment.columns[7]
replenishment_status_column = replenishment.columns[8]
owner_column = replenishment.columns[9]

# 业务意思：重新计算缺口数量，确认“安全库存 - 当前库存”还差多少。
replenishment["计算缺口数量"] = (
    replenishment[safety_stock_column] - replenishment[current_stock_column]
).clip(lower=0)

# 业务意思：只保留有缺口、系统建议补货、并且没有被人工取消的补货任务。
need_follow_up = replenishment[
    (replenishment["计算缺口数量"] > 0)
    & (replenishment[system_suggestion_column] != "暂不补货")
    & (replenishment[replenishment_status_column] != "已取消")
]

# 业务意思：只显示采购/运营最关心的字段。
result = need_follow_up[
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
    ]
]

# 业务意思：把需要继续跟进的补货 SKU 显示在终端里，先不导出文件。
print(result.to_string(index=False))

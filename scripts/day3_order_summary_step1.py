"""Day 3 step 1: read orders.csv and summarize sales by SKU.

This small script is intentionally limited to one learning goal:
turn order rows into a SKU-level sales summary.
"""

import pandas as pd


# 业务意思：读取订单记录表，把 CSV 变成 Python 能处理的表格。
orders = pd.read_csv("data/orders.csv")

# 业务意思：确认订单表里哪些列代表订单号、SKU、数量和销售额。
# 这里用列的位置，是为了避免 Windows 终端偶尔把中文字段名传成乱码。
order_id_column = orders.columns[0]
sku_column = orders.columns[1]
quantity_column = orders.columns[4]
sales_column = orders.columns[5]

# 业务意思：把相同 SKU 的订单放到一起，统计总销量、总销售额和订单笔数。
summary = orders.groupby(sku_column).agg(
    总销量=(quantity_column, "sum"),
    总销售额=(sales_column, "sum"),
    订单笔数=(order_id_column, "count"),
)

# 业务意思：把 SKU 汇总结果显示在终端里，先不导出文件。
print(summary)

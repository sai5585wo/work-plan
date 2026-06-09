"""Day 3 step 2: read orders.csv and summarize sales by platform.

This small script answers one business question:
which sales platform/channel has more orders and sales amount.
"""

import pandas as pd


# 业务意思：读取订单记录表，准备按平台渠道统计。
orders = pd.read_csv("data/orders.csv")

# 业务意思：确认订单表里哪些列代表订单号、数量、销售额和平台。
# 这里用列的位置，是为了避免 Windows 终端偶尔把中文字段名传成乱码。
order_id_column = orders.columns[0]
quantity_column = orders.columns[4]
sales_column = orders.columns[5]
platform_column = orders.columns[6]

# 业务意思：把同一个平台的订单放到一起，统计订单笔数、总销量和总销售额。
summary = orders.groupby(platform_column).agg(
    订单笔数=(order_id_column, "count"),
    总销量=(quantity_column, "sum"),
    总销售额=(sales_column, "sum"),
)

# 业务意思：把平台渠道汇总结果显示在终端里，先不导出文件。
print(summary)

"""Day 3 step 3: filter pending or exception orders.

This small script answers one business question:
which orders still need human follow-up.
"""

import pandas as pd


# 业务意思：读取订单记录表，准备找出需要跟进的订单。
orders = pd.read_csv("data/orders.csv")

# 业务意思：确认订单表里哪一列代表订单状态。
# 这里用列的位置，是为了避免 Windows 终端偶尔把中文字段名传成乱码。
order_status_column = orders.columns[7]

# 业务意思：只保留订单状态为“待处理”或“异常”的订单。
need_follow_up_orders = orders[
    orders[order_status_column].isin(["待处理", "异常"])
]

# 业务意思：把需要运营继续跟进的订单清单显示在终端里。
print(need_follow_up_orders)

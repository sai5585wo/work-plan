"""Day 6: exception summary report.

This script answers two business questions:
1. What types and statuses of exceptions do we currently have?
2. Which exceptions are not closed yet, and which orders do they affect?
3. What should the responsible person do next?
"""

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("outputs")
SUMMARY_OUTPUT = OUTPUT_DIR / "day6_exception_summary.csv"
OPEN_EXCEPTIONS_OUTPUT = OUTPUT_DIR / "day6_open_exceptions.csv"
ACTION_SUGGESTION_OUTPUT = OUTPUT_DIR / "day6_exception_action_suggestion.csv"

# 业务意思：读取异常记录表，查看当前有哪些异常需要统计和跟进。
exceptions = pd.read_csv("data/exceptions.csv")

# 业务意思：读取订单表，用影响订单号关联订单信息。
orders = pd.read_csv("data/orders.csv")

# 业务意思：清理字段名和文本值两边的空格，避免“ORD006”和“ ORD006 ”匹配不上。
exceptions.columns = exceptions.columns.str.strip()
orders.columns = orders.columns.str.strip()

for column in exceptions.columns:
    if pd.api.types.is_string_dtype(exceptions[column]):
        exceptions[column] = exceptions[column].str.strip()

for column in orders.columns:
    if pd.api.types.is_string_dtype(orders[column]):
        orders[column] = orders[column].str.strip()

# 业务意思：确认异常表里的关键字段。
exception_id_column = exceptions.columns[0]
sku_column = exceptions.columns[1]
product_name_column = exceptions.columns[2]
exception_type_column = exceptions.columns[3]
exception_description_column = exceptions.columns[4]
affected_order_column = exceptions.columns[5]
process_status_column = exceptions.columns[6]
owner_column = exceptions.columns[7]
created_date_column = exceptions.columns[8]

# 业务意思：确认订单表里的关键字段。
order_id_column = orders.columns[0]
platform_column = orders.columns[6]
order_status_column = orders.columns[7]
order_date_column = orders.columns[8]

# 业务意思：按异常类型统计数量，回答“哪类异常最多”。
type_summary = (
    exceptions.groupby(exception_type_column)
    .size()
    .reset_index(name="数量")
    .rename(columns={exception_type_column: "项目"})
)
type_summary.insert(0, "维度", "异常类型")

# 业务意思：按处理状态统计数量，回答“还有多少异常没闭环”。
status_summary = (
    exceptions.groupby(process_status_column)
    .size()
    .reset_index(name="数量")
    .rename(columns={process_status_column: "项目"})
)
status_summary.insert(0, "维度", "处理状态")

# 业务意思：把异常类型汇总和处理状态汇总放到同一张汇总表里。
exception_summary = pd.concat([type_summary, status_summary], ignore_index=True)

# 业务意思：筛选未关闭异常，已关闭的异常不再进入待处理清单。
open_exceptions = exceptions[exceptions[process_status_column] != "已关闭"]

# 业务意思：用“影响订单号 = 订单号”关联订单表，带出平台、订单状态和订单日期。
open_exception_detail = open_exceptions.merge(
    orders[[order_id_column, platform_column, order_status_column, order_date_column]],
    left_on=affected_order_column,
    right_on=order_id_column,
    how="left",
)

# 业务意思：整理成运营/客服/采购可以直接查看的未关闭异常清单。
open_exception_detail = open_exception_detail[
    [
        exception_id_column,
        sku_column,
        product_name_column,
        exception_type_column,
        exception_description_column,
        affected_order_column,
        platform_column,
        order_status_column,
        process_status_column,
        owner_column,
        created_date_column,
        order_date_column,
    ]
]

action_rules = {
    "缺货异常": "联系采购确认补货计划或预计到货时间",
    "订单异常": "核对平台订单状态和发货记录",
    "商品资料缺失": "补全商品资料、供应商和上架信息",
}

# 业务意思：根据异常类型生成处理建议，告诉负责人下一步该做什么。
open_exception_detail["处理建议"] = open_exception_detail[exception_type_column].map(
    action_rules
).fillna("人工判断处理方式")

print("=== 异常汇总表 ===")
print(exception_summary.to_string(index=False))

print("\n=== 未关闭异常清单 ===")
print(open_exception_detail.to_string(index=False))

print("\n=== 异常处理建议表 ===")
print(open_exception_detail.to_string(index=False))

# 业务意思：导出异常汇总表和未关闭异常清单，方便后续查看或导入飞书。
OUTPUT_DIR.mkdir(exist_ok=True)
exception_summary.to_csv(SUMMARY_OUTPUT, index=False, encoding="utf-8-sig")
open_exception_detail.to_csv(OPEN_EXCEPTIONS_OUTPUT, index=False, encoding="utf-8-sig")
open_exception_detail.to_csv(
    ACTION_SUGGESTION_OUTPUT, index=False, encoding="utf-8-sig"
)

print(f"\n已导出异常汇总表：{SUMMARY_OUTPUT}")
print(f"已导出未关闭异常清单：{OPEN_EXCEPTIONS_OUTPUT}")
print(f"已导出异常处理建议表：{ACTION_SUGGESTION_OUTPUT}")

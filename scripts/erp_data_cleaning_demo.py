from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def write_csv(df: pd.DataFrame, name: str) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_DIR / name, index=False)


def print_table_preview(name: str, df: pd.DataFrame) -> None:
    print(f"\n=== {name} ===")
    print(f"行数: {len(df)}")
    print(f"字段: {', '.join(df.columns)}")
    print(df.head())


def build_sku_check_report(products: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    product_skus = set(products["SKU"])
    rows = []

    for table_name, df in tables.items():
        current_skus = set(df["SKU"])
        missing_skus = sorted(current_skus - product_skus)
        rows.append(
            {
                "数据表": table_name,
                "SKU总数": len(current_skus),
                "缺失SKU数量": len(missing_skus),
                "缺失SKU": "、".join(missing_skus) if missing_skus else "",
                "检查结果": "异常" if missing_skus else "正常",
            }
        )

    return pd.DataFrame(rows)


def build_order_reports(orders: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    by_sku = (
        orders.groupby(["SKU", "引用产品名"], as_index=False)
        .agg(订单数=("订单号", "count"), 销售数量=("数量", "sum"), 销售额=("销售额", "sum"))
        .sort_values(["销售额", "销售数量"], ascending=False)
    )

    by_platform = (
        orders.groupby("平台", as_index=False)
        .agg(订单数=("订单号", "count"), 销售数量=("数量", "sum"), 销售额=("销售额", "sum"))
        .sort_values("销售额", ascending=False)
    )

    pending_or_exception = orders[orders["订单状态"].isin(["待处理", "异常"])].copy()
    pending_or_exception = pending_or_exception.sort_values(["订单状态", "订单日期", "订单号"])

    return by_sku, by_platform, pending_or_exception


def calculate_inventory_status(row: pd.Series) -> str:
    if row["当前库存"] <= 0:
        return "缺货"
    if row["当前库存"] < row["安全库存"]:
        return "低库存"
    return "正常"


def build_inventory_alert_report(inventory: pd.DataFrame) -> pd.DataFrame:
    report = inventory.copy()
    report["计算库存状态"] = report.apply(calculate_inventory_status, axis=1)
    report["状态是否一致"] = report["库存状态"] == report["计算库存状态"]
    report["缺口数量"] = (report["安全库存"] - report["当前库存"]).clip(lower=0)
    report["库存优先级"] = report["计算库存状态"].map({"缺货": 1, "低库存": 2, "正常": 3})
    report = report[report["计算库存状态"].isin(["低库存", "缺货"])].copy()
    return report.sort_values(["库存优先级", "缺口数量"], ascending=[True, False])


def build_replenishment_suggestion(products: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    report = inventory.merge(
        products[["SKU", "供应商", "成本", "商品状态"]],
        on="SKU",
        how="left",
    )
    report["缺口数量"] = (report["安全库存"] - report["当前库存"]).clip(lower=0)
    report["补货建议"] = report["当前库存"].apply(
        lambda value: "紧急补货" if value <= 0 else "建议补货"
    )
    report.loc[report["缺口数量"] == 0, "补货建议"] = "暂不补货"
    report["补货优先级"] = report["补货建议"].map({"紧急补货": 1, "建议补货": 2, "暂不补货": 3})
    report["预估补货成本"] = report["缺口数量"] * report["成本"]
    report = report[report["缺口数量"] > 0].copy()
    report = report[
        [
            "SKU",
            "产品名",
            "供应商",
            "商品状态",
            "当前库存",
            "安全库存",
            "库存状态",
            "缺口数量",
            "补货建议",
            "补货优先级",
            "成本",
            "预估补货成本",
        ]
    ]
    return report.sort_values(["补货优先级", "缺口数量"], ascending=[True, False])


def build_exception_reports(
    exceptions: pd.DataFrame,
    orders: pd.DataFrame,
    inventory: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary = (
        exceptions.groupby(["异常类型", "处理状态"], as_index=False)
        .agg(异常数量=("异常编号", "count"))
        .sort_values(["异常类型", "处理状态"])
    )

    open_exceptions = exceptions[~exceptions["处理状态"].isin(["已处理", "已关闭"])].copy()
    order_fields = orders[["订单号", "订单状态", "平台", "订单日期"]].drop_duplicates("订单号")
    inventory_fields = inventory[["SKU", "当前库存", "安全库存", "库存状态"]].drop_duplicates("SKU")

    open_exceptions = open_exceptions.merge(
        order_fields,
        left_on="影响订单号",
        right_on="订单号",
        how="left",
    ).merge(inventory_fields, on="SKU", how="left")

    return summary, open_exceptions[
        [
            "异常编号",
            "SKU",
            "产品名",
            "异常类型",
            "异常描述",
            "影响订单号",
            "订单状态",
            "平台",
            "当前库存",
            "安全库存",
            "库存状态",
            "处理状态",
            "负责人",
            "创建日期",
            "备注",
        ]
    ]


def main() -> None:
    products = read_csv("products.csv")
    orders = read_csv("orders.csv")
    inventory = read_csv("inventory.csv")
    replenishment = read_csv("replenishment.csv")
    exceptions = read_csv("exceptions.csv")

    tables = {
        "products.csv": products,
        "orders.csv": orders,
        "inventory.csv": inventory,
        "replenishment.csv": replenishment,
        "exceptions.csv": exceptions,
    }

    for name, df in tables.items():
        print_table_preview(name, df)

    sku_check_report = build_sku_check_report(
        products,
        {
            "orders.csv": orders,
            "inventory.csv": inventory,
            "replenishment.csv": replenishment,
            "exceptions.csv": exceptions,
        },
    )
    write_csv(sku_check_report, "sku_check_report.csv")

    by_sku, by_platform, pending_or_exception = build_order_reports(orders)
    write_csv(by_sku, "order_summary_by_sku.csv")
    write_csv(by_platform, "order_summary_by_platform.csv")
    write_csv(pending_or_exception, "pending_or_exception_orders.csv")

    inventory_alert_report = build_inventory_alert_report(inventory)
    write_csv(inventory_alert_report, "inventory_alert_report.csv")

    replenishment_suggestion = build_replenishment_suggestion(products, inventory)
    write_csv(replenishment_suggestion, "replenishment_suggestion.csv")

    exception_summary, open_exceptions = build_exception_reports(exceptions, orders, inventory)
    write_csv(exception_summary, "exception_summary.csv")
    write_csv(open_exceptions, "open_exceptions.csv")

    print("\n输出完成：")
    for file_path in sorted(OUTPUT_DIR.glob("*.csv")):
        print(f"- {file_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()

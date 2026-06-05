from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_ROOT = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

ORDER_COLUMNS = {"订单号", "日期", "SKU", "产品名", "销售额", "数量", "平台"}
INVENTORY_COLUMNS = {"SKU", "产品名", "当前库存", "安全库存"}
ADS_COLUMNS = {"日期", "SKU", "广告花费", "广告销售额"}


@dataclass
class BusinessSummary:
    sales_amount: float
    order_count: int
    sales_quantity: int
    average_order_value: float


def read_table(base_path: Path, required_columns: set[str]) -> pd.DataFrame:
    xlsx_path = base_path.with_suffix(".xlsx")
    csv_path = base_path.with_suffix(".csv")

    if xlsx_path.exists():
        df = pd.read_excel(xlsx_path)
        source_path = xlsx_path
    elif csv_path.exists():
        df = pd.read_csv(csv_path)
        source_path = csv_path
    else:
        raise FileNotFoundError(f"缺少输入文件: {xlsx_path} 或 {csv_path}")

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing = "、".join(sorted(missing_columns))
        raise ValueError(f"{source_path.name} 缺少必要字段: {missing}")

    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df["销售额"] = pd.to_numeric(df["销售额"], errors="coerce").fillna(0)
    df["数量"] = pd.to_numeric(df["数量"], errors="coerce").fillna(0).astype(int)
    return df


def clean_inventory(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["当前库存"] = pd.to_numeric(df["当前库存"], errors="coerce").fillna(0).astype(int)
    df["安全库存"] = pd.to_numeric(df["安全库存"], errors="coerce").fillna(0).astype(int)
    return df


def clean_ads(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df["广告花费"] = pd.to_numeric(df["广告花费"], errors="coerce").fillna(0)
    df["广告销售额"] = pd.to_numeric(df["广告销售额"], errors="coerce").fillna(0)
    return df


def build_business_summary(orders: pd.DataFrame) -> BusinessSummary:
    sales_amount = float(orders["销售额"].sum())
    order_count = int(orders["订单号"].nunique())
    sales_quantity = int(orders["数量"].sum())
    average_order_value = sales_amount / order_count if order_count else 0

    return BusinessSummary(
        sales_amount=sales_amount,
        order_count=order_count,
        sales_quantity=sales_quantity,
        average_order_value=average_order_value,
    )


def build_inventory_warning(inventory: pd.DataFrame) -> pd.DataFrame:
    result = inventory.copy()
    result["库存缺口"] = result["安全库存"] - result["当前库存"]
    result["状态"] = result["库存缺口"].apply(lambda gap: "需补货" if gap >= 0 else "正常")
    return result.sort_values(["状态", "库存缺口"], ascending=[False, False])


def build_ads_roi(ads: pd.DataFrame) -> pd.DataFrame:
    result = ads.copy()
    result["ROI"] = result.apply(
        lambda row: row["广告销售额"] / row["广告花费"] if row["广告花费"] else 0,
        axis=1,
    )
    result["投放状态"] = result["ROI"].apply(lambda roi: "低效" if roi < 1.5 else "正常")
    return result.sort_values(["投放状态", "ROI"], ascending=[True, True])


def build_overview_df(summary: BusinessSummary) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["今日销售额", round(summary.sales_amount, 2)],
            ["今日订单数", summary.order_count],
            ["今日销量", summary.sales_quantity],
            ["平均客单价", round(summary.average_order_value, 2)],
        ],
        columns=["指标", "数值"],
    )


def build_text_summary(
    summary: BusinessSummary,
    inventory_warning: pd.DataFrame,
    ads_roi: pd.DataFrame,
) -> str:
    low_inventory_count = int((inventory_warning["状态"] == "需补货").sum())
    low_roi_count = int((ads_roi["投放状态"] == "低效").sum())

    return "\n".join(
        [
            "跨境电商运营日报",
            "",
            f"今日总销售额为 {summary.sales_amount:.2f} 元，订单数 {summary.order_count} 单，"
            f"销量 {summary.sales_quantity} 件，平均客单价 {summary.average_order_value:.2f} 元。",
            f"库存方面，有 {low_inventory_count} 个 SKU 低于或等于安全库存，建议优先确认补货计划。",
            f"广告方面，有 {low_roi_count} 个 SKU 的 ROI 低于 1.5，建议检查投放策略、素材或产品转化。",
            "",
            "说明: 本报告由本地 MVP 自动生成，当前版本仅用于需求验证和演示。",
        ]
    )


def save_report(
    overview: pd.DataFrame,
    inventory_warning: pd.DataFrame,
    ads_roi: pd.DataFrame,
    text_summary: str,
) -> None:
    output_dir = OUTPUT_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "运营日报.xlsx"
    text_path = output_dir / "日报总结.txt"

    try:
        report_path.unlink(missing_ok=True)
        with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
            overview.to_excel(writer, sheet_name="经营概览", index=False)
            inventory_warning.to_excel(writer, sheet_name="库存预警", index=False)
            ads_roi.to_excel(writer, sheet_name="广告ROI", index=False)
        print(f"Excel日报已生成: {report_path}")
    except PermissionError:
        overview.to_csv(output_dir / "经营概览.csv", index=False, encoding="utf-8-sig")
        inventory_warning.to_csv(output_dir / "库存预警.csv", index=False, encoding="utf-8-sig")
        ads_roi.to_csv(output_dir / "广告ROI.csv", index=False, encoding="utf-8-sig")
        print(f"当前环境无法写入xlsx，已降级输出CSV: {output_dir}")

    text_path.write_text(text_summary, encoding="utf-8")

    print(f"文字日报已生成: {text_path}")


def main() -> None:
    data_dir = get_latest_data_dir()
    orders = clean_orders(read_table(data_dir / "orders", ORDER_COLUMNS))
    inventory = clean_inventory(read_table(data_dir / "inventory", INVENTORY_COLUMNS))
    ads = clean_ads(read_table(data_dir / "ads", ADS_COLUMNS))

    summary = build_business_summary(orders)
    overview = build_overview_df(summary)
    inventory_warning = build_inventory_warning(inventory)
    ads_roi = build_ads_roi(ads)
    text_summary = build_text_summary(summary, inventory_warning, ads_roi)

    save_report(overview, inventory_warning, ads_roi, text_summary)


def get_latest_data_dir() -> Path:
    run_dirs = sorted(
        [path for path in DATA_ROOT.glob("run_*") if path.is_dir()],
        key=lambda path: path.name,
        reverse=True,
    )
    if not run_dirs:
        raise FileNotFoundError("缺少输入数据目录，请先运行 src/create_sample_data.py")
    return run_dirs[0]


if __name__ == "__main__":
    main()

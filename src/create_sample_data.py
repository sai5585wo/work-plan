import csv
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_ROOT = BASE_DIR / "data"

ORDER_HEADERS = [
    "\u8ba2\u5355\u53f7",
    "\u65e5\u671f",
    "SKU",
    "\u4ea7\u54c1\u540d",
    "\u9500\u552e\u989d",
    "\u6570\u91cf",
    "\u5e73\u53f0",
]
INVENTORY_HEADERS = ["SKU", "\u4ea7\u54c1\u540d", "\u5f53\u524d\u5e93\u5b58", "\u5b89\u5168\u5e93\u5b58"]
ADS_HEADERS = ["\u65e5\u671f", "SKU", "\u5e7f\u544a\u82b1\u8d39", "\u5e7f\u544a\u9500\u552e\u989d"]


def main() -> None:
    DATA_DIR = DATA_ROOT / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    DATA_DIR.mkdir(exist_ok=True)

    orders_rows = [
        ["T20260605001", "2026-06-05", "A001", "\u624b\u673a\u58f3", 99.9, 2, "Temu"],
        ["T20260605002", "2026-06-05", "A002", "\u84dd\u7259\u8033\u673a", 159.0, 1, "TikTok"],
        ["T20260605003", "2026-06-05", "A001", "\u624b\u673a\u58f3", 99.9, 3, "Temu"],
        ["T20260605004", "2026-06-05", "A003", "\u6570\u636e\u7ebf", 39.9, 5, "Amazon"],
        ["T20260605005", "2026-06-05", "A004", "\u6536\u7eb3\u5305", 69.0, 2, "Shopee"],
        ["T20260605006", "2026-06-05", "A002", "\u84dd\u7259\u8033\u673a", 159.0, 2, "TikTok"],
    ]
    inventory_rows = [
        ["A001", "\u624b\u673a\u58f3", 42, 50],
        ["A002", "\u84dd\u7259\u8033\u673a", 120, 60],
        ["A003", "\u6570\u636e\u7ebf", 18, 30],
        ["A004", "\u6536\u7eb3\u5305", 75, 40],
    ]
    ads_rows = [
        ["2026-06-05", "A001", 120.0, 360.0],
        ["2026-06-05", "A002", 200.0, 420.0],
        ["2026-06-05", "A003", 80.0, 60.0],
        ["2026-06-05", "A004", 50.0, 180.0],
    ]

    write_csv(DATA_DIR / "orders.csv", ORDER_HEADERS, orders_rows)
    write_csv(DATA_DIR / "inventory.csv", INVENTORY_HEADERS, inventory_rows)
    write_csv(DATA_DIR / "ads.csv", ADS_HEADERS, ads_rows)

    print(f"sample data created: {DATA_DIR}")


def write_csv(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


if __name__ == "__main__":
    main()

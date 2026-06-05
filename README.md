# 跨境电商运营日报自动生成 MVP

## 项目目标

这是一个用于验证副业方向的最小 MVP：

> 运营上传订单、库存、广告 Excel，工具自动生成每日运营日报，减少人工整理表格时间。

## 功能范围

- 读取 `orders.xlsx/csv`、`inventory.xlsx/csv`、`ads.xlsx/csv`
- 校验必要字段
- 计算经营概览
- 生成库存预警
- 计算广告 ROI
- 输出 `运营日报.xlsx`，如果当前环境无法写入 xlsx，则自动降级输出 CSV
- 输出 `日报总结.txt`

## 项目结构

```text
crossborder-report-mvp/
  data/run_时间戳/       输入Excel/CSV文件
  output/run_时间戳/     输出日报文件
  src/
    create_sample_data.py
    generate_report.py
  requirements.txt
  README.md
```

## 运行方式

如果你本机已安装 Python：

```powershell
cd E:\Developer\work-plan\crossborder-report-mvp
pip install -r requirements.txt
python src\create_sample_data.py
python src\generate_report.py
```

当前 Codex 环境可用运行方式：

```powershell
cd E:\Developer\work-plan\crossborder-report-mvp
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\create_sample_data.py
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\generate_report.py
```

说明：`create_sample_data.py` 每次会创建新的 `data/run_时间戳` 目录；`generate_report.py` 默认读取最新的数据目录，并输出到新的 `output/run_时间戳` 目录。

## 输入文件字段

### orders.xlsx / orders.csv

| 字段 | 说明 |
|---|---|
| 订单号 | 唯一订单编号 |
| 日期 | 订单日期 |
| SKU | 商品SKU |
| 产品名 | 商品名称 |
| 销售额 | 订单销售额 |
| 数量 | 销售数量 |
| 平台 | Temu/TikTok/Amazon等 |

### inventory.xlsx / inventory.csv

| 字段 | 说明 |
|---|---|
| SKU | 商品SKU |
| 产品名 | 商品名称 |
| 当前库存 | 当前库存数量 |
| 安全库存 | 低于或等于该值时触发预警 |

### ads.xlsx / ads.csv

| 字段 | 说明 |
|---|---|
| 日期 | 广告日期 |
| SKU | 商品SKU |
| 广告花费 | 当日广告支出 |
| 广告销售额 | 广告带来的销售额 |

## 下一步优化

1. 支持客户自定义字段映射。
2. 接入飞书多维表格。
3. 增加日报自动发送到飞书群。
4. 增加异常趋势分析。

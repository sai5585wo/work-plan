# 7-Day Plan: Python Pandas Data Cleaning Demo

> 中文说明：这份计划用于把已经完成的飞书 ERP 流程模拟工作台，升级为 Python/Pandas 数据清洗作品。  
> 每天投入：约 2-4 小时。  
> 工具限制：本阶段只使用 Python/Pandas 和本地 CSV，不做 API、RPA、n8n、Make 或真实平台接入。  
> 目标：用代码复现飞书工作台里的业务逻辑，形成 AI 自动化工程师作品链的第二阶段案例。

## Goal（目标）

Build a Python/Pandas data cleaning demo based on cross-border e-commerce ERP mock CSV data.

中文解释：基于 `data/` 目录中的模拟数据，完成 SKU 检查、订单汇总、库存预警、补货建议和异常汇总。

完成后应具备：

- Python/Pandas 主脚本
- SKU 一致性检查报表
- 订单汇总报表
- 库存预警报表
- 补货建议报表
- 异常汇总报表
- 一段可用于面试讲解的作品说明

## Execution Progress（执行进度）

- [ ] Day 1: Python Environment and CSV Reading（环境与读取 CSV）
- [ ] Day 2: SKU Consistency Check（SKU 一致性检查）
- [ ] Day 3: Order Summary（订单汇总）
- [ ] Day 4: Inventory Alert（库存预警）
- [ ] Day 5: Replenishment Report（补货建议）
- [ ] Day 6: Exception Summary（异常汇总）
- [ ] Day 7: Portfolio Packaging（作品包装）

## Current Status（当前状态）

Current stage（当前阶段）：

> Day 1: Python Environment and CSV Reading（环境与读取 CSV，准备开始）

已完成基础：

- 已完成飞书 ERP 流程模拟工作台。
- 已建立 `data/` mock CSV 数据目录。
- 已确认下一阶段优先目标是 Python/Pandas 数据清洗。

当前输入数据：

- `data/products.csv`
- `data/orders.csv`
- `data/inventory.csv`
- `data/replenishment.csv`
- `data/exceptions.csv`

输出位置：

- `outputs/`

主脚本：

- `scripts/erp_data_cleaning_demo.py`

## Day 1: Python Environment and CSV Reading（环境与读取 CSV）

Focus（重点）：先确认 Python 能读取所有 CSV，不急着写复杂逻辑。

Tasks（任务）：

- 确认 Python 可运行。
- 确认 pandas 可用。
- 读取商品、订单、库存、补货、异常 CSV。
- 打印每张表的字段、行数和前几行数据。

Output（产出）：

能成功读取 CSV 的基础脚本。

## Day 2: SKU Consistency Check（SKU 一致性检查）

Focus（重点）：检查不同数据表是否都围绕同一套 SKU 运转。

Tasks（任务）：

- 检查订单表中的 SKU 是否都存在于商品资料表。
- 检查库存表中的 SKU 是否都存在于商品资料表。
- 检查补货表中的 SKU 是否都存在于商品资料表。
- 检查异常表中的 SKU 是否都存在于商品资料表。

Output（产出）：

- `outputs/sku_check_report.csv`

## Day 3: Order Summary（订单汇总）

Focus（重点）：用代码汇总订单，模拟运营日报中最常见的数据统计。

Tasks（任务）：

- 按 SKU 汇总订单数量、销售额、订单数。
- 按平台汇总销售额和订单数。
- 标记待处理和异常订单。

Output（产出）：

- `outputs/order_summary_by_sku.csv`
- `outputs/order_summary_by_platform.csv`
- `outputs/pending_or_exception_orders.csv`

## Day 4: Inventory Alert（库存预警）

Focus（重点）：用代码复现库存预警逻辑。

Tasks（任务）：

- 根据当前库存和安全库存重新计算库存状态。
- 找出低库存和缺货 SKU。
- 对比 CSV 中原有库存状态和代码计算结果。

Output（产出）：

- `outputs/inventory_alert_report.csv`

## Day 5: Replenishment Report（补货建议）

Focus（重点）：生成可交给采购或运营处理的补货建议。

Tasks（任务）：

- 计算缺口数量：`max(安全库存 - 当前库存, 0)`。
- 根据库存状态生成补货建议。
- 合并商品资料，带出产品名、供应商、成本。

Output（产出）：

- `outputs/replenishment_suggestion.csv`

## Day 6: Exception Summary（异常汇总）

Focus（重点）：把异常数据整理成可处理清单。

Tasks（任务）：

- 按异常类型统计数量。
- 找出未处理异常。
- 关联订单和库存信息，说明异常影响。

Output（产出）：

- `outputs/exception_summary.csv`
- `outputs/open_exceptions.csv`

## Day 7: Portfolio Packaging（作品包装）

Focus（重点）：把脚本结果转化为可面试讲解的作品。

Tasks（任务）：

- 整理主脚本：`scripts/erp_data_cleaning_demo.py`。
- 在作品说明文档中增加 Python/Pandas 数据清洗章节。
- 写 3-5 句面试讲解：这个脚本解决什么业务问题。
- 更新 AI 自动化工程师路线图中的 Stage 2 状态。

Output（产出）：

一个可展示、可运行、可讲解的 Python/Pandas 数据清洗 Demo。

## Acceptance Criteria（完成标准）

- 运行主脚本后，`outputs/` 至少生成 5 个 CSV。
- 每个输出文件不是空文件，并且字段名可读。
- `SKU004` 能识别为缺货。
- `SKU002` 能识别为低库存或需要关注。
- 订单表中的异常订单能进入异常汇总或待处理清单。
- 脚本不修改 `data/` 原始文件。

## Do Not Do Yet（暂时不要做）

- 不接真实 ERP。
- 不接平台 API。
- 不做 RPA 自动点击。
- 不做 n8n / Make。
- 不把脚本包装成完整系统。

原因：

> 当前目标是补齐 AI 自动化工程师作品链中的数据清洗能力，而不是提前进入复杂自动化。

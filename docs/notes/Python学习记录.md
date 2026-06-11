# Python 学习记录

> 记录原则：每次只记录一个小步骤。先写业务意义，再写最小 Python 代码。

## 笔记模板

```md
## 日期 / 阶段 - 小步骤名称

### 为什么做

这里写这一小步解决什么业务问题。

### 输入

这里写使用了哪张表，例如：

- `data/orders.csv`

### 处理逻辑

1. 第一步
2. 第二步
3. 第三步

### Python 最小代码

```python
# 这里只放核心代码，不放完整大脚本
```

### 代码的业务意思

- `pd.read_csv()`：读取一张 CSV 表。
- `groupby()`：把相同字段的数据放到一起统计。

### 输出

这里写终端看到什么结果，或生成了什么报表。

### 我学到的

这里用自己的话总结这一小步。
```

## Day 3 - SKU 销售汇总

### 为什么做

为了把一条条订单明细，汇总成每个 SKU 的销售表现。

### 输入

- `data/orders.csv`

### 处理逻辑

1. 读取订单表。
2. 按 SKU 分组。
3. 统计总销量、总销售额、订单笔数。
4. 在终端打印结果。

### Python 最小代码

```python
orders = pd.read_csv("data/orders.csv")

summary = orders.groupby(sku_column).agg(
    总销量=(quantity_column, "sum"),
    总销售额=(sales_column, "sum"),
    订单笔数=(order_id_column, "count"),
)
```

### 代码的业务意思

- `pd.read_csv()`：读取订单表。
- `groupby(sku_column)`：把相同 SKU 的订单放到一起。
- `sum`：统计总销量和总销售额。
- `count`：统计订单笔数。

### 输出

终端显示每个 SKU 的总销量、总销售额和订单笔数。

### 我学到的

订单表里 SKU 可以重复，因为同一个商品可以被多个订单购买。  
按 SKU 汇总后，就能从“订单明细”变成“商品销售表现”。

## Day 3 - 平台渠道汇总

### 为什么做

为了查看不同平台渠道的订单表现，判断哪个平台贡献了更多订单和销售额。

### 输入

- `data/orders.csv`

### 处理逻辑

1. 读取订单表。
2. 按平台分组。
3. 统计订单笔数、总销量、总销售额。
4. 在终端打印结果。

### Python 最小代码

```python
orders = pd.read_csv("data/orders.csv")

summary = orders.groupby(platform_column).agg(
    订单笔数=(order_id_column, "count"),
    总销量=(quantity_column, "sum"),
    总销售额=(sales_column, "sum"),
)
```

### 代码的业务意思

- `pd.read_csv()`：读取订单表。
- `groupby(platform_column)`：把同一个平台的订单放到一起。
- `count`：统计订单笔数。
- `sum`：统计总销量和总销售额。

### 输出

终端显示 Amazon、Temu、Shopee、TikTok Shop 等平台的订单笔数、总销量和总销售额。

### 我学到的

同一张订单表可以按不同维度汇总：  
按 SKU 看商品表现，按平台看渠道表现。

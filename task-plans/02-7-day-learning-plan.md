# 7-Day Learning Plan: Feishu Workflow + Amazon Listing Basics

> 中文说明：这份计划用于把你当前的飞书多维表格 MVP，从“能生成 Listing 的表格”升级成“能用于面试展示的小型工作流”。  
> 学习方式：保留英文标题和关键术语，同时用中文解释，方便你顺便积累跨境电商和工具类英文词汇。

## Goal（目标）

Upgrade the current MVP from a simple Listing prompt table into a small workflow that can be shown in interviews.

中文解释：把当前 MVP 从“简单的 Listing 提示词表格”，升级成一个可以在面试中展示的半自动工作流。

7 天后你应该完成：

- A cleaner Feishu base（更清晰的飞书多维表格）
- A workflow view（工作流视图，用于自己操作）
- An interview demo view（面试展示视图，用于给别人看）
- A product information submission form（商品信息提交表单）
- A basic status workflow（基础状态流转）
- Better understanding of Amazon Listing structure and risk words（理解 Amazon Listing 结构和风险词）

## Day 1: Clean Up Fields（整理字段）

Focus（重点）：让当前表格更清晰、更像真实工作表。

Tasks（任务）：

- Check all current fields（检查当前所有字段）。
- Keep these core input fields（保留这些核心输入字段）：
  - Chinese product name（中文品名）
  - Product category（产品类目）
  - Material/specification（材质/规格）
  - Target users（适用人群）
  - Use scenarios（使用场景）
  - Core selling points（核心卖点）
  - Target platform（目标平台）
  - Target market（目标市场）
- Keep these output fields（保留这些输出字段）：
  - English title（英文标题）
  - Five bullet points（五点描述）
  - Search keywords（搜索关键词）
  - Risk notes（风险提示）
  - Generation status（生成状态）
  - Generated prompt（生成提示词）
- Make sure `Target platform` and `Target market` are single-select fields.
  - 中文解释：把 `目标平台` 和 `目标市场` 设置成“单选”，避免每次手动输入不一致。
- Make sure `Generation status` has these options:
  - To generate（待生成）
  - Generated（已生成）
  - Need manual edit（需人工修改）
  - Completed（已完成）

Output（当天产出）：

- A clean field structure in Feishu（一个结构清楚的飞书字段体系）。

## Day 2: Create Two Views（创建两个视图）

Focus（重点）：把“自己操作用的视图”和“面试展示用的视图”分开。

Tasks（任务）：

- Create a view named `Workflow View`（创建 `Workflow View` 工作流视图）。
- Keep all fields in `Workflow View`（这个视图保留所有字段，方便你自己操作）。
- Create a view named `Interview Demo View`（创建 `Interview Demo View` 面试展示视图）。
- In `Interview Demo View`, only show these fields（展示视图只保留这些字段）：
  - Chinese product name（中文品名）
  - Product category（产品类目）
  - Target platform（目标平台）
  - Target market（目标市场）
  - English title（英文标题）
  - Five bullet points（五点描述）
  - Search keywords（搜索关键词）
  - Risk notes（风险提示）
  - Generation status（生成状态）
- Hide `Generated prompt` in the interview view.
  - 中文解释：面试展示时不要展示完整提示词，否则页面太乱。展示结果和流程价值就够了。

Output（当天产出）：

- One working view（一个自己用的工作视图）
- One clean interview view（一个干净的面试展示视图）

## Day 3: Add Filters And Grouping（添加筛选和分组）

Focus（重点）：让表格能管理任务进度，而不是只存数据。

Tasks（任务）：

- In `Workflow View`, group records by `Generation status`.
  - 中文解释：在工作流视图里，按 `生成状态` 分组。
- Create filters for（创建这些筛选条件）：
  - To generate（待生成）
  - Need manual edit（需人工修改）
  - Completed（已完成）
- Check whether the 6 existing sample products are marked correctly.
  - 中文解释：检查已有 6 个商品的状态是否正确，比如已经写完的就标记为 `Completed`。

Output（当天产出）：

- You can quickly see which products are unfinished.
  - 中文解释：你可以一眼看出哪些商品还没生成、哪些需要修改、哪些已经完成。

## Day 4: Create A Product Submission Form（创建商品提交表单）

Focus（重点）：模拟真实公司里“运营提交商品资料”的流程。

Tasks（任务）：

- Create a form from the Feishu base（从飞书多维表格生成一个表单）。
- The form should collect only input fields（表单只收集输入字段）：
  - Chinese product name（中文品名）
  - Product category（产品类目）
  - Material/specification（材质/规格）
  - Target users（适用人群）
  - Use scenarios（使用场景）
  - Core selling points（核心卖点）
  - Target platform（目标平台）
  - Target market（目标市场）
- Submit 1 test product through the form（用表单提交 1 个测试商品）。

Output（当天产出）：

- A product information submission form（一个商品信息提交表单）
- 1 new test record created from the form（通过表单新增 1 条测试记录）

## Day 5: Add Simple Automation（添加简单自动化）

Focus（重点）：让新增商品自动进入待处理状态。

Tasks（任务）：

- Create an automation rule（创建一条自动化规则）：
  - Trigger: when a new record is created（触发条件：新增记录时）
  - Action: set `Generation status` to `To generate`（执行动作：把 `生成状态` 设置为 `待生成`）
- Test the automation by submitting another product through the form.
  - 中文解释：再通过表单提交一个商品，测试自动化是否生效。
- Confirm the new record status is set automatically.
  - 中文解释：确认新记录的状态是否自动变成 `待生成`。

Output（当天产出）：

- New products automatically enter the `To generate` status.
  - 中文解释：以后新商品进入表格后，会自动进入待生成状态。

## Day 6: Study Amazon Listing Structure（学习 Amazon Listing 结构）

Focus（重点）：理解你正在生成的内容，而不是只会复制 AI 结果。

Tasks（任务）：

- Find 10 Amazon product pages from similar categories（找 10 个相似类目的 Amazon 商品页面）：
  - Bags（箱包）
  - Phone accessories（手机配件）
  - Kitchen storage（厨房收纳）
  - Beauty tools（美妆工具）
  - Daily goods（日用百货）
  - Office accessories（办公配件）
- Observe（观察）：
  - Title structure（标题结构）
  - Bullet point structure（五点描述结构）
  - Common keywords（常见关键词）
  - Material and size descriptions（材质和尺寸描述）
  - Words that may need proof（可能需要证明的词）
- Write 5 notes about what good Listings have in common.
  - 中文解释：写 5 条观察笔记，记录好的 Listing 有哪些共同点。

Output（当天产出）：

- 10 reference products reviewed（看完 10 个参考商品）
- 5 Listing writing observations（写出 5 条 Listing 写作观察）

## Day 7: Review And Package The MVP（复盘并包装 MVP）

Focus（重点）：把你的作品整理成可以讲给面试官或老板听的版本。

Tasks（任务）：

- Review the Feishu base from start to finish（从头到尾检查飞书表格）。
- Make sure there are at least 6 completed product examples（确保至少有 6 个已完成商品样本）。
- Make sure the generated prompt field works for new records（确保新增商品时，生成提示词字段能正常工作）。
- Write a short explanation（写一段简短介绍）：
  - What problem this workflow solves（这个工作流解决什么问题）
  - How the workflow runs（这个工作流怎么运行）
  - What can be automated next（下一步还能自动化什么）

Suggested explanation（建议面试表达）：

```text
I built a semi-automated Amazon Listing workflow.
我做了一个半自动 Amazon Listing 工作流。

The operator only needs to enter basic product information.
运营只需要填写商品基础信息。

The table automatically generates a standardized AI prompt.
表格会自动生成标准化 AI 提示词。

Then the AI output is reviewed and saved back into the table as an English title, five bullet points, search keywords, and risk notes.
然后把 AI 生成结果人工审核后，回填为英文标题、五点描述、搜索关键词和风险提示。

This reduces repeated prompt writing and makes Listing output more structured.
这个流程可以减少重复写提示词的时间，也能让 Listing 输出更结构化。
```

Output（当天产出）：

- A finished MVP demo（一个完成版 MVP 演示）
- A short interview explanation（一段面试介绍话术）

## Key Vocabulary（重点词汇）

- Workflow（工作流）：一套从输入到输出的流程。
- Field（字段）：表格中的一列。
- View（视图）：同一张表的不同展示方式。
- Form（表单）：给别人提交信息用的入口。
- Automation（自动化）：满足条件后自动执行动作。
- Trigger（触发条件）：什么时候开始自动化。
- Action（执行动作）：自动化具体做什么。
- Listing（商品详情页内容）：通常包含标题、五点描述、图片、关键词等。
- Bullet points（五点描述）：Amazon 商品页里常见的卖点描述。
- Search keywords（搜索关键词）：帮助商品被搜索到的词。
- Risk notes（风险提示）：提醒哪些描述可能夸大、侵权或需要证明。

## Do Not Learn This Week（这周先不要学）

Avoid these for now（暂时避开这些）：

- Python
- n8n
- Make
- API integration（API 集成）
- Paid RPA tools（付费 RPA 工具）
- SaaS product development（SaaS 产品开发）

Reason（原因）：

The current priority is to build one visible workflow and understand the business process first.

中文解释：当前优先级是先做出一个看得见、讲得清楚的小工作流，并理解跨境电商 Listing 的基础业务流程。现在过早学习太多技术，会分散注意力。

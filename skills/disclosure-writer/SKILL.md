---
name: disclosure-writer
description: Draft an attorney-facing Chinese technical disclosure from reviewed code features and evidence, preserving concrete implementation, formulas and the boundary between measured effects and intended goals.
---

# 技术交底起草与修订

读取本工作流仓库 `docs/contract.md`。以当前evidence.json及核对后的features.json为依据。技术领域、问题、操作和输出必须具体，避免把“AI赋能”“提高精度”当作实现。

建立输入—处理—输出闭环。核心技术细节写到足够复现：数据表示、变换顺序、模块交互、参数来源和边界处理。将继承骨干和个人改动分别放在内部特征表。不得自动将整体开源骨干写成个人新创。

效果按expected/observed/validated分开：预期目标用“拟/待验证”；历史现象说明评估条件与混杂因素；严格验证结果需要对应运行证据与评价协议。源码本身不能证明效果。公式存在时从实际操作推导并定义符号、维度和单位；遇到无法确认的推导保留问题，不写漂亮但与代码不同的公式。

正文不插入证据ID、评分、skill名或内部流程记录；这些在review-appendix.json。结合patent-bridge加载上游发明交底、自检与权利要求规范，先做保护点删除测试，再按技术问题—手段—效果组织内容。start/draft引擎给结构化草稿，现有技术查询和技术语义判断由Agent实际完成，不能把模板填充说成已检索。

完整申请按docs/application-contract.md填写application JSON。权利要求、步骤、公式和附图的特征引用必须覆盖到有效代码支持；详细句子的支持关系仍须精读判断。用 --application 与交底同版冻结。依赖项和附图不能为扩大保护而补造。Word候选通过export_docx导出后必须页面核查。

修订时只改工作版features.json：逐项解释问题如何处理、关联步骤和术语是否联动，再运行draft创建新版本。旧版不可覆盖。源代码变化则新建快照与案件，旧审阅记录不复用。

如果现有技术未检索，明确保留这一状态；不得写“未发现相关专利”或“具备创造性”。如用户授权检索，可用公开关键词查询权威来源，逐条记录可访问URL、日期、相关技术特征，不向外传未公开源码或完整交底文本。

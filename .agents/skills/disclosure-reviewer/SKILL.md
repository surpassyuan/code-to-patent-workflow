---
name: disclosure-reviewer
description: Review a code-grounded disclosure for implementation fidelity, terminology/formula consistency and unsupported assertions; produce revision-bound findings for multi-round correction rather than approval by prose quality.
---

# 多视角复核

读取本仓库 `docs/review-rubric.md` 和 `docs/contract.md`。每次都以当前冻结版manifest.json中的版本与正文SHA-256为绑定对象。存在application.json时，读取全部申请文件与application-support.json，并在review JSON填写完整artifact_hashes。读取正文、features、源码证据，不能仅复述上一轮结论。

依次切换三个视角，各输出一份JSON：
1. implementation：逐特征回到代码、配置和入口，检查实现、调用、条件、数据和效果证据。
2. consistency：输入输出、术语、公式、参数、实施例和步骤是否相互一致。
3. adversarial：尝试证伪稿中最强断言，找禁用模块、未来信息、不可复现收益、来源混淆和不成立的扩展。

融合上游检查：每条权利要求是否被具体实施步骤支持；删去必要特征后是否还能解决问题；依赖引用、S号、图号、公式符号和维度是否一致；D1对比是否实际读过及只读摘要的边界；是否把可配置参数说成实验最优；广义保护是否超出实现和披露范围。ID存在仅证明关联关系，不能替代句子内容核验。

具体问题包括severity、feature、description、evidence和建议fix；无问题也必须描述检查范围和剩余限制，不能只有“通过”。记录角色视角不等于独立审稿人；同一模型执行时明确同一模型，不宣称盲审或法律审核。

blocking必须修订并在新版本重新检查；warning保留交付状态，不能静默丢弃。发现信息不足可以提出问题，不擅自改研究事实。最多三版默认预算用完仍有阻断项，则报告未完成审阅稿与所需证据。

三角色复核和机器校验全部完成后才finalize，产出仍是发明人及专业人士待审稿，不是授权/申请成功证明。

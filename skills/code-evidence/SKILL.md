---
name: code-evidence
description: Extract traceable technical features from implementation code, configs and entrypoints, separating inherited code, activation and experimentally verified effects before drafting a disclosure.
---

# 实现证据提取

在完整code-to-disclosure仓库内使用，读取 `docs/contract.md`。使用start产生的evidence.json并精读源文件；静态脚本只建立AST/行号/哈希出处，不理解或证明创新。

对每个候选特征记录：中文功能、输入/输出、操作次序、关键函数、调用入口、开关/默认值、参数来源、继承/修改/新增、证据ID、支持状态、启用状态、效果状态。不要将代码作者自动等同发明人；个人分工以用户说明与可核验记录确认。

尤其核查：
- 模块是否只定义而未调用；是否因配置false、缺资产或运行时降级被关闭。
- 不同执行入口是否一致；公式所述操作是否实际执行。
- 数据类型、顺序、维度和单位是否匹配。
- 输入与额外条件是否在实际使用场景下可获得。
- 保存结果是否对应当前配置、版本和评价协议。
- 专利文字中的功能扩展与性能收益是否有实现与运行证据。

精读保存配置与结果时，按用户明确指定的路径只读；默认扫描排除权重/数据及output。不能加载不可信pickle、执行被扫描代码或自动重训。需要加入额外评估证据时，先将实际可核验记录作为明确文本输入整理到选定证据目录，重新start固定快照，并记录其原始来源；不能自行编造结果文件。

发现缺口形成具体问题，不用论文或专利措辞补实现。保留“代码原型”“已运行”“收益待验证”三个不同结论。

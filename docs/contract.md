# 数据契约与可核查边界

源码是输入，Agent负责语义分析/起草/复核，Python负责快照、结构、版本和门槛。没有模型API请求、自动外部上传或专利提交。`Python >=3.10`，核心仅标准库；无需API key。Word导出有可选依赖。上游接入见[integration](integration.md)，完整申请见[application-contract](application-contract.md)。

## 技术特征features.json

```json
{
  "title": "某技术交底书",
  "field": "具体技术领域",
  "problem": "特定数据/设备条件下的技术问题",
  "embodiment": "输入输出、处理顺序、参数来源及异常处理",
  "prior_art": "核实过的比较与URL，或尚未检索",
  "features": [{
    "id": "F1", "name": "中文操作名", "statement": "来源支持的技术操作",
    "support": "explicit", "activation": "active", "origin": "modified",
    "evidence": ["从evidence.json选取的C-ID"],
    "effect": {"status": "expected", "text": "待验证的作用"}
  }]
}
```

- support：explicit/inherent/needs-confirmation/unsupported；inherent必须由审阅者解释推导依据。
- activation：active/inactive/unknown；程序不自动推断，Agent必须检查入口及最终配置。
- origin：inherited/modified/new/unknown；不是对发明人或权属的法律认定。
- effect：expected/observed/validated/none。validated需要evidence及非空protocol，机器只校验字段/出处；是否真实实验和因果成立由复核者判断。
- 正文仅纳入有支持且active的技术特征，其余留附录。拟实施方案可以另写，不伪装成运行过。

## 复核记录

```json
{
  "revision": 1,
  "draft_sha256": "从当前r01/manifest.json读取",
  "summary": "说明核查了什么以及限制",
  "issues": [{
    "id": "I1", "severity": "blocking", "feature": "F1",
    "description": "某断言与实际代码/配置不符",
    "evidence": ["C-ID"], "fix": "具体修改建议"
  }]
}
```

角色implementation、consistency、adversarial分别登记。至少两版、各版均完成三视角；最终版无blocking。新增版本必须给修改原因。旧稿与记录冻结，源码哈希变化导致案件失效，避免旧审查应用到新实现。

## 文件边界

案件目录保存绝对源码根路径和摘录，属于私有材料，默认放仓库外。示例是自编通用数值变换代码。公开仓库只含引擎、skills、说明、测试和合成案例。扫描器不执行源码、不导入模型、不加载权重。

当前支持Python AST与UTF-8 JSON/YAML/TOML文本；不解析notebook、C++/Java、Word/PPT及二进制资产，不宣称全语言分析。YAML按带出处的文本收集，变量覆盖/条件路径由Agent人工核查。默认排除output/logs/datasets，额外证据必须明确选定并保留原始溯源。

## 输出与专业审阅

默认交付Markdown技术审阅稿、证据映射、问题/版本记录。完整申请按application契约生成同版四件套与图源；review须绑定manifest的全部artifact_hashes。引擎生成章结构，语义完整性仍需Agent和发明人核对。完整申请默认继续Word导出与页面QA；仅文本/局部稿遵循用户范围。交付位于delivery/rNN，排版候选位于exports。机器与同一模型多视角复查均不等于专业法律审阅。

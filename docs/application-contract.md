# 完整申请包的数据与版本契约

参考 `examples/application.template.json`。Agent语义分析填工作版，脚本只做结构
和证据引用检查，不会从代码自动猜出合法权利要求。

- title/abstract/field/background/problem/embodiment：中文正文。摘要300字符上限
  是本工作流的写作约定，不是自动法律合规判断。
- claims：连续整数id；text是完整权项；depends_on仅引用前面的权项，独权为[]；
  features引用已支持且启用的F-ID。不强制最低从权数量。
- steps：连续S1-Sn，text描述具体操作，features说明实现哪些特征。
  每个被权项引用的特征都必须有对应步骤。
- formulas：可选，id/latex/variables（symbol、meaning）/features。
  语义、维度和全部变量是否定义由consistency核对。
- figures：可选，连续整数id/caption/steps。工具生成对应步骤的顺序流程草图，
  复杂拓扑由Agent调整设计后另行核对，不将简单顺序图当成真实网络架构。
- prior_art：status为not-searched/partial/compared；sources中每条包含
  id/title/url/accessed_at/locator/scope（abstract或full-text）；differences
  包含feature/source/comparison。compared至少有来源和比较。URL字段校验不证明
  网页已访问，审阅者必须核验记录。

```text
python scripts/workflow.py draft --case <case> --features <features.json> --application <application.json> --reason <原因>
```

同版生成application.md、四件套md、application.json、application-support.json、
figure-N.mmd并加入manifest。review除revision和draft_sha256外须携带
**artifact_hashes = manifest.files**（完整对象），三个视角核对同一整包。
任一文件变化、申请稿哈希遗漏或过期，都不能复用审阅。
新案件还保存每份已登记review的哈希，直接删改阻断项会使审阅记录失效。
本地state文件不是防恶意管理员的安全账本；这里用于检测误改和版本混用。
机器引用检查无法防止“给F1挂上一个与代码无关的漂亮句子”，这仍是实现与反证
复核的责任；不宣称自动语义证明或自动创造性判断。

`finalize`输出在delivery/rNN，旧版交付不会被新版本覆盖或混入新文件。
默认至少两版、每版三视角、最后一版无blocking，最多三版；预算耗尽仍有问题则
交付问题清单和工作稿状态，不凑通过。

Word可选依赖：`python -m pip install -r requirements-docx.txt`。
图形渲染还需可用Chrome/Edge或Playwright浏览器；缺环境时保留Markdown并说明。
`python scripts/export_docx.py --case <case>` 使用固定版本本地转换器，候选输出
在exports/rNN_时间戳。formula-repair/pending-visual-qa状态不能当作已完成页面检查。
Agent须用可用文档工具渲染、看页、修复后才能称最终Word交付。

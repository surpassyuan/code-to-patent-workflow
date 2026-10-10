# Code to Disclosure · 代码证据驱动的专利技术交底工作流

面向算法/软件研究：从代码、配置、入口与运行记录提取技术证据，生成中文技术交底和可选完整申请审阅稿，经多轮复核与修改保留版本。由Codex或Claude Code担任Agent，Python提供确定性工具。融合版本0.2.1。

已融合两个MIT开源项目的固定版本：[中国专利.skill](https://github.com/handsomestWei/patent-disclosure-skill)和[china-patent-drafter](https://github.com/Oscima2026/china-patent-drafter-skill)。前者提供挖点、查新、交底与会稿规范；后者补充权利要求、实施步骤、附图、可编辑公式和Word交付要求。原版保留在vendor，来源与许可证见[第三方署名](THIRD_PARTY_NOTICES.md)，具体接入见[融合说明](docs/integration.md)。

**设计重点**：代码优先；区分实现/启用/验证；继承与个人改动分开；按代码证据修订文本；每轮有问题单、哈希和版本。公开示例使用通用数值变换，不包含实际研究项目的技术方案。

## 一分钟体验

```bash
python scripts/demo.py --application --output ../code-to-disclosure-v02-demo
python -m unittest discover -s tests -v
```

合成案例第一版故意将默认关闭的附加元数据路径写为启用；脚本化问题单在第二版将其移到附录，并生成同版权利要求、说明书、摘要、附图源码和支持映射。展示的是版本与门槛，不是三个LLM真的审查了此例。vendor内示例来自上游公开仓库，来源可通过固定版本和哈希核对。

## 在Codex / Claude Code里使用

```bash
python scripts/sync_skills.py
```

完整仓库内生成 `.agents/skills` 与 `.claude/skills` 项目技能。Codex输入：

> 使用 $code-to-disclosure，并通过patent-bridge融合两个上游技能。以我指定的代码目录为主要依据，生成技术交底审阅稿；如我要求完整申请，继续生成权利要求、说明书、摘要、附图和Word候选。先核对定义、调用入口与保存配置。至少两轮实现、术语/公式、反证复核；不把禁用模块或拟研究方向写成已实现。每条权利要求关联特征和代码出处。案件数据放仓库外。

Claude Code可使用 `/code-to-disclosure`，或直接指定相应SKILL.md。宿主需允许读指定目录并执行本地Python。项目技能加载方式见[官方OpenAI文档](https://learn.chatgpt.com/docs/build-skills)与[Claude Code文档](https://code.claude.com/docs/en/skills)。当前不依赖模型API key，也没有后台自动运行LLM的SDK服务。

## 可运行命令

```bash
python scripts/workflow.py start --source /path/to/code --case /path/to/private-case
# Agent读取evidence.json，填写独立工作版features.json
python scripts/workflow.py draft --case /path/to/private-case --features /path/to/features.json --reason "first supported draft"
# Agent按当前版本和正文哈希写三份review JSON
python scripts/workflow.py review --case /path/to/private-case --role implementation --findings /path/to/implementation.json
python scripts/workflow.py review --case /path/to/private-case --role consistency --findings /path/to/consistency.json
python scripts/workflow.py review --case /path/to/private-case --role adversarial --findings /path/to/adversarial.json
# 根据问题修改工作版features.json，draft创建第二版，再重新完成三份review
python scripts/workflow.py audit --case /path/to/private-case
python scripts/workflow.py finalize --case /path/to/private-case
```

start支持重复 `--include 'src/core/*.py'` 等模式、`--max-revisions 3`。模式作用于源根的POSIX相对路径，脚本使用Python fnmatch。默认只收集代码/配置文本，拒绝案件放在源树内、拒绝覆盖旧案件。

## 五个协作技能

- `code-to-disclosure`：状态与阶段推进。
- `code-evidence`：实现证据、启用条件、个人与继承部分。
- `patent-bridge`：调用固定版本的两个上游规范，调和输入顺序、输出范围与审核约束。
- `disclosure-writer`：技术闭环与迭代起草。
- `disclosure-reviewer`：实现、术语/公式、反证三视角复查。

这是顺序协作的五种能力，不假装五个模型实例或法律审核人。详细格式见[契约](docs/contract.md)、[复核清单](docs/review-rubric.md)、[流程图](docs/architecture.md)。

## 完整申请与Word

Agent填写[申请包契约](docs/application-contract.md)后，将工作版application.json与交底一起提交：

```bash
python scripts/workflow.py draft --case /path/to/private-case --features /path/to/features.json --application /path/to/application.json --reason "claims and specification revision"
```

申请包所有文件哈希写入manifest；每份review须带完整artifact_hashes，旧稿复核不能放行新申请。至少两轮后finalize到delivery/rNN。

可选Word转换（核心引擎无需第三方依赖）：

```bash
python -m pip install -r requirements-docx.txt
python scripts/export_docx.py --case /path/to/private-case
```

使用上游本地Mermaid渲染与DOCX转换器，需可用Chrome/Edge或Playwright浏览器。候选在exports中；检查export-status.json并渲染页面核查，图或公式失败不能当成最终Word交付。合成示例只说明结构，不能作为实际申请内容使用。

## GitHub发布范围

可发布本工作流、技能、测试、合成案例及已署名的上游快照。案件、原始数据、权重和未公开交底书保留本地；`.gitignore`只是一层辅助，发布前检查暂存文件。不要在此仓库加入真实项目私有代码。具体步骤见[GitHub上传指南](docs/github-upload.md)，本版检查范围见[隐私检查记录](docs/privacy-check.md)。

引擎生成Markdown、JSON和Mermaid审阅材料。完整内容需按案件补足公式、参数、附图与现有技术，Word需页面核查。自动检查不证明新颖性、创造性、权属或申请可获授权。

## 来源与实现范围

0.1版的证据引擎与技能为本地重新编写，参考证据映射与自检思路。0.2版保留并实际接入用户指定的两个上游项目。原创贡献是代码证据分析、状态区分、权项支持映射、版本绑定与有限轮次复核；不将上游专利规范和转换器声称为个人原创，也不追认历史上曾使用某个未核实的技能。

核心采用Python标准库，Python>=3.10。测试包括来源漂移、冻结稿篡改、未知证据、过期复核、缺轮次、阻断项、禁用特征、权项/步骤映射和完整申请版本绑定。GitHub Actions配置Windows/Linux测试；本地通过不等于已在GitHub执行。`python scripts/verify_vendor.py`核对两个快照的494个文件；`python scripts/package_public.py --output <新ZIP路径>`按白名单打包，排除案件与Git元数据。

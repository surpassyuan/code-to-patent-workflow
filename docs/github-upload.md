# 上传到GitHub（Windows）

推荐用GitHub Desktop，一次上传完整目录并保留隐藏技能文件夹。
上传对象是包含README.md、scripts、skills、vendor的code-to-disclosure项目目录。
ZIP是搬运备份，解压后上传源码目录，方便他人阅读、克隆和运行。

## 方法一：GitHub Desktop

1. 安装并登录[GitHub Desktop](https://desktop.github.com/)。
2. File → Add local repository → Choose，选择本地code-to-disclosure目录，再点Add repository。
   本次工作区的这个目录已经初始化Git。如果使用ZIP解压得到的目录，它没有.git；
   在提示中选择create a repository here，使用已有目录，保留当前README/许可证。
3. 在Changes里检查：可包含vendor中上游公开示例；真实项目私有代码、案件、权重、
   采集数据和未公开专利稿不应出现。`.agents`和`.claude`也要上传。
4. 若尚无提交，在Summary填`Release code-grounded patent workflow v0.2.1`，点击Commit to main。
5. 点击Publish repository。建议Name为`code-to-patent-workflow`；Description填：
   `Code-grounded Chinese patent disclosure workflow with evidence tracing, pinned skills and multi-round review.`
6. 给面试官查看可取消Keep this code private；选个人账户并Publish repository。
   日后修改，先Commit to main，再Push origin。

官方说明：[添加本地仓库](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop)、
[发布已有项目](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop)。
实际发布由你的登录账户完成。

## 方法二：PowerShell + Git

在GitHub右上角“+”→New repository，仓库名可用code-to-patent-workflow。
创建空仓库，不勾初始化README、.gitignore或License。复制仓库HTTPS地址。

在本地项目目录打开PowerShell：

```powershell
git init -b main
git status --short
git add .
git diff --cached --stat
git commit -m "Release code-grounded patent workflow v0.2.1"
git remote add origin https://github.com/YOUR_USERNAME/code-to-patent-workflow.git
git push -u origin main
```

将YOUR_USERNAME替换成你的GitHub用户名，也可以直接粘贴网页给出的HTTPS地址。
已有提交则不重复commit；若origin已存在，先`git remote -v`核对，勿盲目覆盖已有远端。
提交作者会在GitHub公开。希望隐藏真实身份时，先在GitHub Settings → Emails启用邮箱隐私，使用GitHub提供的noreply邮箱和公开昵称设置当前仓库的user.name和user.email后再commit。
认证用登录窗口/GitHub凭据管理，不把token写进地址或文件。

## 发布后检查

- 首页README能显示；THIRD_PARTY_NOTICES与两份vendor许可证可访问。
- scripts、5个skills、`.agents`、`.claude`、vendor/manifest.json都在。
- Actions中查看Windows/Linux测试。绿色结果才说明远端CI运行通过。
- 初次使用：`python scripts/demo.py --application --output ../private-demo`。
- 分享仓库链接；演示用合成案例，不上传真实案件。

公开页面可介绍“基于开源专利技能，设计代码证据驱动与多轮复核工作流”；
设计贡献重点放在编排、映射、版本检查及多轮复核。

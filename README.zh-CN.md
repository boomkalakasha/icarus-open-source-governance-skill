![BOOMKALAKASHA 水印](assets/brand/boomkalakasha/watermark-auto.svg)

# Icarus 开源治理

[English](README.md) · [技能说明](SKILL.md) · [配置示例](.icarus-open-source.example.yml) · [证据门禁](references/evidence-gates.md)

> **先把风险说清楚，再把项目公开。**
>
> **Make the risks visible before making the project public.**

在把内部原型公开之前，使用这套 Skill 扫描可达历史、显式记录隐私与来源风险、对齐中英双语文档，并整理供人工审查的发布证据。

把隐私、来源、文档、许可证和发布证据串成一条可执行、可复核的路径，让内部仓库能够审慎走向开源，而不夸大已经验证的事实。

<!-- icarus-release-fact: dynamic -->
公开物料与状态请查看
[最新 GitHub Release](https://github.com/boomkalakasha/icarus-open-source-governance-skill/releases/latest)
和[完整发布记录](https://github.com/boomkalakasha/icarus-open-source-governance-skill/releases)。
未打标签的源码仍是候选；只有复核、标签、CI、资产与 Release 证据完整后，
才能作为公开版本。

本地脚本只使用 Python 标准库和 PowerShell；第一次审查不需要安装项目专属依赖。

## 一眼看懂：它能帮你做什么

| 你的目标 | 这套 Skill 会帮你做什么 | 它支持的判断 |
| --- | --- | --- |
| 判断仓库能否安全公开 | 校验项目契约、隐私、许可证、品牌和发布输入 | 把可审查候选与不应贸然公开的“已就绪”说法分开 |
| 看清历史会暴露什么 | 扫描可达提交、元数据、生成物和打包内容 | 把来源或隐私的隐患变成可调查的问题清单 |
| 让公开文档更有分寸 | 保持中英导航对齐，品牌保持可选 | 文档易读，同时不把个人默认信息伪装成项目必选项 |
| 组装别人能复核的发布物 | 生成制品、manifest、校验和，并串起 CI/安全门禁 | 给人工审核者具体证据，而不只是一个绿色命令 |

常见场景包括：把内部原型整理成 GitHub 项目、交给客户或社区前检查仓库，
或帮助团队理解为什么源码、历史、元数据和发布物必须分开审查。这套 Skill
负责组织证据，不替你做法律、归属或生产决策。

## 60 秒路径

第一次审查按这个顺序走：

1. 复制配置示例，只替换能够举证的事实。
2. 先校验契约，再扫描当前文件和可达历史。
3. 逐条阅读发现，明确处理隐私、许可证、双语文档和品牌事项；不要把扫描通过
   当成自动批准。
4. 运行评测并打包候选，检查 `dist/manifest.json` 和 `SHA256SUMS.txt` 后，
   再申请 PR、tag 或 GitHub Release。

```powershell
Copy-Item .icarus-open-source.example.yml .icarus-open-source.yml
python scripts/validate.py --config .icarus-open-source.yml
python scripts/scan_public_risks.py --history
python scripts/run_evals.py
pwsh -NoProfile -File scripts/package.ps1
```

这些命令只验证本地候选，不会创建仓库、推送分支、发布标签、修改 GitHub 设置，也不证明生产就绪。

扫描发现问题后先分类再改：当前树发现通常需要修改源码；可达历史发现可能需要删除内容、
评估历史重写，或记录明确例外；元数据发现需要复核 author/committer。处理决定后重新运行
相关扫描，并把人工复核记录和候选版本放在一起。

## 你会得到什么

**示意证据摘要——以下为已脱敏样例，不是本仓库的实际扫描结果：**

| 证据流 | 示例发现 | 门禁 |
| --- | --- | --- |
| 当前树 | 未发现配置中的私有主机模式 | `PASS` |
| 可达历史 | 发现一个疑似令牌值：`[REDACTED_SECRET]` | `P1 HOLD`，等待来源复核 |
| 双语文档 | 导航与动态发布事实标记一致 | `PASS` |
| 打包 | 由同一暂存树生成 manifest 与 SHA-256 | `LOCAL_PASS` |
| 公开宿主 | 标签、CI、资产与仓库设置 | `NOT_OBSERVED` |

示例结论：在历史发现被处理，或由有权限的复核人明确接受之前，
**暂停公开发布**。本地扫描全绿也不会自动升级公开宿主证据。

## 覆盖范围

- 为项目、许可证决策、隐私、品牌、Git、发布和证据门禁提供小型 `.icarus-open-source.yml` 契约。
- 把当前树、可达历史、提交元数据、包和生成物风险检查分为独立证据流。
- 提供中英双语公共文档与社区模板，并明确支持、安全和发布边界。
- 品牌是可选的：附带的 BOOMKALAKASHA 套件仅为示例配置，不是项目默认项，也不代表项目归属。
- 覆盖 GitHub Flow、Conventional Commits、不可变 SemVer、校验和、CI、CodeQL 和发布工作流；发布仍需审核与独立授权。
- 提供可复用的发布文档门禁，在打包前校验 tag/源码版本一致，并让 README 的发布事实保持动态。

## 配套项目

- [AI-first Vibe Coding Skill](https://github.com/boomkalakasha/ai-first-vibe-coding-skill)：适合 Agent 实现、独立复核完成后，把项目送入开源发布门禁。
- [Icarus AI Spring Scaffold](https://github.com/boomkalakasha/icarus-ai-spring-scaffold)：适合需要安全、可审查 Java 17 服务起点的新项目。

## 明确不承诺的内容

- 本 Skill 不是法律意见，不能判断版权、商标、雇佣成果、隐私或第三方许可证权利。
- 本地文件不能证明远端 GitHub 设置、CI 结果、发布资产或生产/切流状态。
- 它不授权破坏性历史改写、公开发布或任何个人 GitHub 资料修改。

## 配置项目

复制示例到候选仓库，只替换能够举证的事实：

```powershell
Copy-Item .icarus-open-source.example.yml .icarus-open-source.yml
python scripts/validate.py --config .icarus-open-source.yml
```

`brand.mode` 默认是 `none`。只有项目所有者明确选择可替换的品牌配置时，才使用 `subtle` 或 `full`；详见[品牌说明](references/branding.md)。

## 本地证据与打包

`scripts/scan_public_risks.py --history` 会扫描本地可达提交以及 author/committer 元数据，并对未变化的文本 blob 去重，同时保留首次发现位置；它是确定性的风险标记扫描，不是完整的秘密或权利审计。可通过 `--pattern` 加入项目特定规则，或通过 `--config .icarus-open-source.yml` 读取 `privacy.forbiddenPatterns` 和历史扫描偏好，并逐条调查发现。

`scripts/package.ps1` 只暂存一次源树，再在 `dist/` 生成 `.skill`、`.zip`、`manifest.json` 和 `SHA256SUMS.txt`。manifest 会标明源树为 `clean` 或 `dirty`；只有干净的确切标签包才能进入发布审查。公开前仍须基于确切已审核标签重新核验发布资产。

`VERSION` 声明本地包版本；该版本是否已经公开发布仍以 GitHub Release 为准，未打 tag 的候选不等于公开发布。

## 参考与支持

- [公开就绪流程](references/public-readiness.md)
- [隐私与来源](references/privacy-and-provenance.md)
- [文档与本地化](references/documentation-and-localization.md)
- [GitHub 交付](references/github-delivery.md)
- [发布文档同步](references/release-documentation-sync.md)
- [贡献](CONTRIBUTING.md) · [安全](SECURITY.md) · [支持](SUPPORT.md) · [变更记录](CHANGELOG.md) · [许可证](LICENSE)

GitHub 行为以官方 [社区健康文件](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)、[Release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) 和 [CodeQL](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql) 文档为准。

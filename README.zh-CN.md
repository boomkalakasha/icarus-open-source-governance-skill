![BOOMKALAKASHA 水印](assets/brand/boomkalakasha/watermark-auto.svg)

# Icarus 开源治理

[English](README.md) · [技能说明](SKILL.md) · [配置示例](.icarus-open-source.example.yml) · [证据门禁](references/evidence-gates.md)

一套可复用、以证据为中心的治理流程：把仓库整理为公开开源候选，而不夸大已验证的事实。

## 60 秒路径

```powershell
python scripts/validate.py
python scripts/scan_public_risks.py --history
python scripts/run_evals.py
pwsh -NoProfile -File scripts/package.ps1
```

这些命令只验证本地候选，不会创建仓库、推送分支、发布标签、修改 GitHub 设置，也不证明生产就绪。

## 覆盖范围

- 为项目、许可证决策、隐私、品牌、Git、发布和证据门禁提供小型 `.icarus-open-source.yml` 契约。
- 把当前树、可达历史、提交元数据、包和生成物风险检查分为独立证据流。
- 提供中英双语公共文档与社区模板，并明确支持、安全和发布边界。
- 品牌是可选的：附带的 BOOMKALAKASHA 套件仅为示例配置，不是项目默认项，也不代表项目归属。
- 覆盖 GitHub Flow、Conventional Commits、不可变 SemVer、校验和、CI、CodeQL 和发布工作流；发布仍需审核与独立授权。

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

`scripts/scan_public_risks.py --history` 会扫描本地可达提交以及 author/committer 元数据；它是确定性的风险标记扫描，不是完整的秘密或权利审计。可通过 `--pattern` 加入项目特定规则，或通过 `--config .icarus-open-source.yml` 读取 `privacy.forbiddenPatterns` 和历史扫描偏好，并逐条调查发现。

`scripts/package.ps1` 只暂存一次源树，再在 `dist/` 生成 `.skill`、`.zip`、`manifest.json` 和 `SHA256SUMS.txt`。manifest 会标明源树为 `clean` 或 `dirty`；只有干净的确切标签包才能进入发布审查。公开前仍须基于确切已审核标签重新核验发布资产。

## 参考与支持

- [公开就绪流程](references/public-readiness.md)
- [隐私与来源](references/privacy-and-provenance.md)
- [文档与本地化](references/documentation-and-localization.md)
- [GitHub 交付](references/github-delivery.md)
- [贡献](CONTRIBUTING.md) · [安全](SECURITY.md) · [支持](SUPPORT.md) · [变更记录](CHANGELOG.md) · [许可证](LICENSE)

GitHub 行为以官方 [社区健康文件](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)、[Release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) 和 [CodeQL](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql) 文档为准。

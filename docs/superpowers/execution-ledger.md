# Open-source Productization Execution Ledger

Status values: `UNTRIAGED`, `RED`, `IN_PROGRESS`, `SPEC_REVIEW`, `QUALITY_REVIEW`, `VERIFIED`, `BLOCKED`.

| ID | Work package | Owner | Status | Required evidence | Current note |
| --- | --- | --- | --- | --- | --- |
| B1 | Brand sources and tests | Luna design implementer | UNTRIAGED | asset tests + browser QA | ImageGen API blocked by missing local key; SVG fallback authorized by controller |
| A1 | AI Skill package/eval contracts | Luna implementer | UNTRIAGED | RED/GREEN tests + manifests | baseline validator 37 files pass |
| A2 | AI Skill bilingual docs/brand | Luna implementer | UNTRIAGED | parity/link tests + rendered GitHub view | current v1.0.0 release copy drifts from assets |
| I1 | Icarus safe CLI output | Luna implementer | UNTRIAGED | path negative tests + ZIP positive test | stdout baseline retained |
| I2 | Icarus runtime/Docker evidence | Luna implementer | UNTRIAGED | package, health, greeting, Docker/Compose | baseline tests/sample pass; container smoke not fresh |
| I3 | Icarus bilingual docs/brand | Luna implementer | UNTRIAGED | parity/link checks + browser QA | Chinese link missing; Maven versions disagree |
| G1 | Governance Skill baseline eval | Luna baseline agents | VERIFIED | 3 baseline outputs + assertions | safe reasoning already strong; Skill must add consistent config, executable checks and reusable artifacts |
| G2 | Governance Skill implementation | Luna implementer | UNTRIAGED | schema/scanner/eval/package | BOOMKALAKASHA must stay optional |
| X1 | Cross-repo spec review | Main Sol | UNTRIAGED | requirement-by-requirement result | subagent DONE is not acceptance |
| X2 | Cross-repo quality/runtime review | Main Sol | UNTRIAGED | fresh commands/browser evidence | no P0/P1 allowed at release gate |
| P1 | GitHub PR/settings/releases | Main Sol | BLOCKED | authenticated GitHub evidence | in-app browser currently signed out |

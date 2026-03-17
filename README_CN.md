# Open Source Hardening Skills

[English](README.md) | **中文**

Open Source Hardening Skills 是面向 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) / Claude Code 的技能包，帮助将任意仓库——应用、库、CLI 工具或论文代码——硬化成结构清晰、可测试、易维护的开源项目。

> **与 ARIS 天然配合。** ARIS 在睡眠中自主完成科研；Open Source Hardening Skills 是下一步，将产出的代码整理成可公开发布的状态。

## 工作流

```text
[ARIS 科研流水线]                  [Open Source Hardening Skills 流水线]
  /idea-discovery                    /oss-audit        -> 扫描问题
  /auto-review-loop    ------>       /oss-plan         -> 生成清单
  /paper-writing                     /oss-refactor     -> 最小化整理
  （代码已存在）                       /oss-tests        -> 补 CI 安全测试
                                     /oss-ci           -> 拦截问题 PR
                                     /oss-docs         -> 完善文档
                                     /oss-review-loop  -> 外部质量把关
                                     （仓库达到发布标准）
```

Open Source Hardening Skills 也可以**单独使用**，对任何已有仓库进行硬化，不依赖 ARIS。

## 技能列表

| 技能 | 触发命令 | 做了什么 |
|------|---------|---------|
| oss-audit | `/oss-audit` | 从 7 个维度扫描，输出按优先级排序的文件级报告（`OSS_AUDIT.md`） |
| oss-plan | `/oss-plan` | 将审计结果转化为可直接贴入 GitHub Issue 的 PR 就绪清单（`OSS_PLAN.md`） |
| oss-refactor | `/oss-refactor` | 施加最小必要的结构调整，使测试和 CI 成为可能 |
| oss-tests | `/oss-tests` | 构建最小自动化测试循环，无需 secret 即可在 CI 运行 |
| oss-ci | `/oss-ci` | 添加或改进 GitHub Actions 流水线，拦截问题 PR |
| oss-docs | `/oss-docs` | 完善 README，补充 SECURITY.md、CHANGELOG.md 和贡献说明 |
| oss-review | `/oss-review` | 通过 Codex MCP（GPT-5.4）进行一次性外部审查 |
| oss-review-loop | `/oss-review-loop` | 迭代审查 -> 修复 -> 再审查，直到达到发布标准（最多 4 轮） |
| oss-hardening | `/oss-hardening` | 一条命令端到端编排完整流水线 |
| oss-search | `/oss-search` | 检索 GitHub 和网络，寻找参考仓库、CI 示例和最佳实践 - 无需 API Key |

## 安装

### 1. 安装并初始化 Claude Code

先安装 Claude Code，并至少启动一次完成登录和 `~/.claude/` 初始化：

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

```bash
cd your-project
claude
```

### 2. 安装技能

**macOS / Linux / WSL（一行命令安装）：**

```bash
curl -fsSL https://raw.githubusercontent.com/zeyuzhangzyz/open-source-hardening-skills/main/install.sh | bash
```

或者克隆后手动运行：

```bash
git clone https://github.com/zeyuzhangzyz/open-source-hardening-skills.git
cd open-source-hardening-skills
bash install.sh
```

**Windows PowerShell（一行命令安装）：**

```powershell
irm https://raw.githubusercontent.com/zeyuzhangzyz/open-source-hardening-skills/main/install.ps1 | iex
```

或者克隆后手动运行：

```powershell
git clone https://github.com/zeyuzhangzyz/open-source-hardening-skills.git
cd open-source-hardening-skills
.\install.ps1
```

安装脚本是幂等的：重复运行会将 skills 更新至最新版本。脚本只替换本 skill 包自带的 `oss-*` 目录，不会影响你已安装的其他 skills。

### 3. 可选：为 review 技能准备 Codex MCP

`/oss-review` 和 `/oss-review-loop` 需要 Codex MCP（配置方式与 ARIS 相同），其余 8 个技能不需要。

```bash
npm install -g @openai/codex
codex setup   # 提示时设置模型为 gpt-5.4
claude mcp add codex -s user -- codex mcp-server
```

### 4. 在目标仓库中运行

```text
/oss-hardening .
```

## 与 ARIS 配合使用

Open Source Hardening Skills 会安装到与 ARIS 相同的 `~/.claude/skills/` 目录，无冲突共存。

```bash
# ARIS 科研流程结束后，对产出代码进行硬化：
/oss-hardening .
```

## 仓库结构

```text
skills/              ARIS 兼容的技能文件（每个技能一个子目录）
  oss-audit/SKILL.md
  oss-plan/SKILL.md
  ...
tests/               技能校验测试
```

## 项目标准

- [SECURITY.md](SECURITY.md) 说明如何私下报告安全问题。
- [CHANGELOG.md](CHANGELOG.md) 记录面向发布的变更。
- [CONTRIBUTING.md](CONTRIBUTING.md) 说明如何修改技能并在本地验证。
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) 会在 push 和 pull request 上运行校验测试。

## 参与贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。快速版本：编辑 `skills/<name>/SKILL.md`，然后在仓库根目录运行：

```bash
python -m unittest discover -s tests -v
```

然后提 PR。目录名必须与 frontmatter 中的 `name` 字段一致。

## 致谢

- **[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** — 本项目设计为与 ARIS 配合使用的自主科研技能包；技能布局直接遵循 ARIS 约定。
- **[Claude Code](https://github.com/anthropics/claude-code)** — Anthropic 的 CLI，执行骨干。

## 许可证

MIT，详见 [LICENSE](LICENSE)。

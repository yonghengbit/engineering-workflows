# 使用指南

本指南面向使用 `engineering-workflow` 完成工程任务的人。Workflow 作者应阅读
[`workflow-contract.md`](workflow-contract.md)。

## 1. 这个项目解决什么问题

通常你只知道想完成什么，例如“修复一个 crash”“验证发布版本”“优化 kernel”，并不想
先研究应该调用哪个 skill、创建哪些文档或拆几个 agent。

`engineering-workflow` 把这些决定放进一个统一入口：

```text
用户描述工程目标
    ↓
engineering-workflow
    ↓
判断当前 Primary Intent
    ↓
只加载对应 workflow
    ↓
选择该 workflow 自己的 strategy / scale
    ↓
执行、验证，必要时切换 workflow
```

它覆盖六类工程目标：Development、Testing、Debugging、Performance、Investigation 和
Review。

## 2. 安装

只安装一个目录：

```text
skills/engineering-workflow/
```

不要单独复制 `references/` 中的 Development 或 Debugging；它们不是独立 skill。

### 2.1 Codex

仓库或团队共享时，把 skill 放到仓库的 `.agents/skills/`：

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/engineering-workflow <repo>/.agents/skills/
```

最终路径应为：

```text
<repo>/.agents/skills/engineering-workflow/SKILL.md
```

个人在所有本地仓库使用时，安装到用户目录：

```bash
mkdir -p "$HOME/.agents/skills"
cp -r skills/engineering-workflow "$HOME/.agents/skills/"
```

Windows PowerShell 示例：

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
Copy-Item -Recurse "skills\engineering-workflow" "$HOME\.agents\skills\"
```

Codex 会从当前目录到仓库根目录扫描 `.agents/skills`，也会读取
`$HOME/.agents/skills`。如果修改未出现，重启 Codex。完整机制见
[OpenAI 官方 Build skills 文档](https://developers.openai.com/codex/skills)。

### 2.2 Claude Code

仓库或团队共享：

```bash
mkdir -p <repo>/.claude/skills
cp -r skills/engineering-workflow <repo>/.claude/skills/
```

个人在所有本地仓库使用：

```bash
mkdir -p "$HOME/.claude/skills"
cp -r skills/engineering-workflow "$HOME/.claude/skills/"
```

最终路径分别为：

```text
<repo>/.claude/skills/engineering-workflow/SKILL.md
$HOME/.claude/skills/engineering-workflow/SKILL.md
```

Claude Code 可以自动匹配 skill，也可以通过 `/engineering-workflow` 显式调用。安装位置与
调用机制见 [Claude Code 官方 Skills 文档](https://code.claude.com/docs/en/slash-commands)。

### 2.3 其他兼容 Agent

本 skill 的可移植核心只有标准 `SKILL.md` 和相对引用的 `references/`。把完整的
`engineering-workflow` 目录复制到宿主文档指定的 Agent Skills 目录，不要只复制
`SKILL.md`，否则渐进加载的 workflow 会丢失。

宿主必须支持开放 Agent Skills 格式以及读取同目录相对文件。目录位置、显式调用符号、
自动匹配和 subagent 能力由宿主决定；本项目不会假设所有工具都使用 Codex 或 Claude Code
的语法。格式规范见 [Agent Skills specification](https://agentskills.io/specification)。

`agents/openai.yaml` 只是 OpenAI 产品的可选 UI 和调用策略扩展。其他宿主可以忽略它，
核心 workflow 不依赖该文件执行。

### 2.4 应该选哪一种

- 团队共享、项目约束稳定：优先 Repository scope。
- 个人在多个项目中复用：使用 User scope。
- 根据实际宿主选择 `.agents/skills`、`.claude/skills` 或其官方指定目录。
- 同名 skill 可能同时出现在 selector 中，因此不要在两个 scope 安装不同版本后期待它们
  自动合并。

## 3. 如何启动

最明确、最可移植的方式是显式调用：

| 宿主 | 显式调用 |
|---|---|
| Codex CLI / IDE extension | `$engineering-workflow` |
| ChatGPT | `@engineering-workflow` |
| Claude Code | `/engineering-workflow` |
| 其他兼容 Agent | 使用宿主提供的 skill selector 或调用语法 |

例如在 Codex 中：

```text
$engineering-workflow

实现一个新的 KV Cache backend。
```

在 Codex CLI 或 IDE extension 中也可以通过 `/skills` 查找 skill。OpenAI 集成通过
`agents/openai.yaml` 关闭隐式调用，避免普通低风险任务自动承担 workflow body 的上下文
成本。Claude Code 和其他宿主使用自己的 activation policy；无论宿主是否支持自动匹配，
需要混合目标、严格证据链或团队一致流程时都建议显式调用。

通常不需要告诉它：

```text
这是 DEVELOPMENT
这是 LARGE
请创建 3 个 agent
请生成 PLAN.md
```

你只需说明目标、约束和验收要求。框架会先选择 Primary Intent，再由选中的 workflow
决定过程深度、artifact、验证和是否需要 subagent。

## 4. 六类任务示例

| 类型 | 适合的真实 prompt | 当前主要结果 |
|---|---|---|
| Development | `增加一个 --prefetch CLI flag，并保持现有默认行为。` | 有意修改软件行为 |
| Testing | `运行现有单元测试，告诉我这个分支是否满足发布标准。` | 得到 PASS / FAIL / BLOCKED 结论 |
| Debugging | `REGISTER_KV_CACHE 在 DCU 上 crash，找到根因。` | 用证据证明未知故障的原因 |
| Performance | `比较旧 kernel 和新 kernel 的吞吐与 p99 latency。` | 得到受控、可复现的性能结论 |
| Investigation | `梳理 Scheduler 如何分配和释放 KV blocks。` | 理解现有实现和调用链 |
| Review | `Review 这个 PR，报告 correctness 和 compatibility 问题。` | 评价已有 change/design 的风险 |

Router 根据你现在真正想得到的结果判断，而不是看到某个关键词就分类。例如“实现功能并
添加 tests”的主要目标仍是 Development；其中运行 tests 是 Development verification。

## 5. 混合任务如何处理

真实任务可能包含多个阶段：

```text
这个 crash 帮我找到原因，修复并加测试。
```

框架不会同时激活三个 workflow，而会按依赖顺序推进：

```text
Debugging
    -> root cause confirmed
Development
    -> fix completed
Testing
    -> regression result
```

只有 Primary Deliverable 改变才切换。Debugging 中读取代码不是 Investigation；Development
中运行单元测试不是 Testing；Performance 中做正确性检查也不会自动切换。

其他常见链路：

```text
测试失败后修复
Testing -> Debugging -> Development -> Testing

性能优化
Performance -> optional Investigation -> Development -> Performance

Review 后修复确认的问题
Review -> Development -> Testing

先理解再开发
Investigation -> Development
```

每次切换只携带目标 workflow 需要的证据、约束、改动、复现方式和验证要求，不复制整个
思考过程，也不会因为切换固定创建一个新 Markdown 文件。

## 6. Development 的四档规模

Development 根据 Scope、Uncertainty、Risk 和 Parallelism 判断规模。用户不需要自己评分。

| Scale | 典型情况 | 默认 artifact |
|---|---|---|
| SMALL | 局部、明确、低风险、验证直接 | 无 |
| MEDIUM | 同一模块内有多个步骤 | 需要持久 checkpoint 时写 `PLAN.md`；真正交接时写 `HANDOFF.md` |
| LARGE | 跨模块契约、架构选择、高风险或兼容性敏感 | 有设计决定或多阶段协调时写对应 artifact；真正交接时写 `HANDOFF.md` |
| VERY_LARGE | 多 subsystem、多个独立 phase 或一个 plan 已无法表达 | `DESIGN.md`, `ROADMAP.md`, `plans/*`, `handoffs/*` |

规模不是按代码行数、文件数或耗时判断。几十行 scheduling 语义变更也可能是 LARGE；多个
独立仓库和 rollout phase 才更可能是 VERY_LARGE。

分类会在初步探索、planning/design、主要 phase 边界和最终验证前重新检查，并在发现重大
接口、数据布局、并发、协议或迁移变化时立即重评。它不会每改一个文件就重新打分。

Artifact 的用途：

- `PLAN.md`：下一步执行什么。
- `DESIGN.md`：为什么选择这个设计。
- `ROADMAP.md`：VERY_LARGE 项目如何分 phase 和协调依赖。
- `HANDOFF.md`：当前实现与验证状态，供继续工作使用。

SMALL 不会为了形式完整而生成这些文档。

## 7. Subagent 如何使用

Router 不会创建 agent。选中 workflow 后，当前宿主 agent 才结合 prompt、repository 和
自身可用能力判断是否存在可以安全并行的工作。

只有同时满足以下条件才适合 subagent：

- ownership 清楚；
- 依赖较弱；
- 修改冲突概率低；
- 输入和输出明确；
- 可以独立验证。

例如，同一个 LARGE Development 可能按两个独立 backend 和测试基础设施拆分；另一个
LARGE 任务如果所有实现都依赖同一份新接口，则应该顺序执行。

Agent role 从实际任务动态产生，不存在固定的 `debug-agent`、`cuda-agent` 或
`review-agent` taxonomy。任务很大也不等于一定 multi-agent。

## 8. 宿主指令文件与 engineering-workflow 的区别

两者解决不同问题：

```text
AGENTS.md / CLAUDE.md / equivalent
= repository-specific host rules

engineering-workflow
= task execution methodology
```

目标仓库的宿主指令文件可以规定：

- build 和 test 命令；
- 代码风格与平台限制；
- 哪些路径可修改；
- repository-specific compatibility 约束。

`engineering-workflow` 决定：

- 当前是 Development、Testing、Debugging、Performance、Investigation 还是 Review；
- 采用什么 strategy / scale；
- 是否需要 artifact、subagent 和哪些验证；
- Primary Intent 何时发生 transition。

不需要把本框架的 routing 规则复制到每个项目的 `AGENTS.md`、`CLAUDE.md` 或等效文件。
Repository rules 会先被遵守，但不拥有 workflow routing 权限。

## 9. 完整示例一：小开发

Prompt：

```text
$engineering-workflow

给现有命令增加一个可选 --dry-run flag，默认行为保持不变，并补测试。
```

内部过程：

```text
Primary Intent: Development
    -> 初步探索真实 CLI 和调用方
Scale: SMALL
    -> 不创建 PLAN.md
    -> 最小实现
    -> 更新直接相关测试
    -> 运行验证
    -> 检查 git diff
```

“补测试”是实现要求，因此没有先路由到 Testing。运行测试是 Development 的验证活动。

## 10. 完整示例二：Debug + Fix

Prompt：

```text
$engineering-workflow

LMCache 的 REGISTER_KV_CACHE 在 DCU 环境报 HIP error，找到根因，修复，并加回归测试。
```

内部过程：

```text
Primary Intent: Debugging
    -> 保存原始错误和环境
    -> 建立最小复现
    -> 比较竞争假设
    -> 判别实验支持 root cause

Transition: Debugging -> Development
    -> 按已证明的原因实现最小修复

Transition: Development -> Testing
    -> 运行回归和相关兼容性验证
```

如果无法复现，结果会明确为 blocked investigation state，而不会猜一个根因或直接提交
speculative patch。

## 11. 完整示例三：复杂性能优化

Prompt：

```text
$engineering-workflow

GPU KV transfer kernel 很慢。找到瓶颈，优化实现，并用相同 workload 证明收益。
```

内部过程：

```text
Primary Intent: Performance
    -> 定义 metric、baseline、workload、环境和控制变量
    -> 检查 correctness
    -> warmup + repeated baseline
    -> 定位 bottleneck

Optional transition: Performance -> Investigation
    -> 只有当独立的实现机制理解成为当前交付物时发生

Transition: Performance -> Development
    -> 实现优化

Transition: Development -> Performance
    -> 在相同控制条件下重新 benchmark
    -> 保存 raw results 和 variance
    -> 只对已测试环境作结论
```

最后一次 benchmark 是必须的；“代码看起来更快”或单次最好结果不能证明收益。

## 12. 如何理解最终报告

不同 workflow 的输出重点不同：

- Development：scale、改动、验证和剩余问题。
- Testing：strategy、PASS/FAIL/BLOCKED/MIXED、覆盖范围和证据。
- Debugging：复现、决定性证据、root cause 和下一步。
- Performance：环境、workload、raw evidence、variance 和结论边界。
- Investigation：verified path、inference、unknowns。
- Review：按严重度排序的 findings、假设和未测试风险。

当代码、文档和实际运行结果冲突时，当前代码与真实观测优先，随后应修复 stale
documentation。

## 13. 会不会消耗更多 token

会有额外成本，但不是把全部 workflow 一次塞进上下文。

兼容 Agent Skills 的宿主通常先看到 skill 的 `name` 和 `description`。当
`engineering-workflow` 被显式调用或匹配后，才加载顶层 `SKILL.md`；确定 Primary Intent
后只加载一个 workflow；Development 和 Testing 再各自只加载一个 scale/strategy reference。

例如 SMALL Development 的加载路径只有：

```text
SKILL.md
-> references/development/workflow.md
-> references/development/small.md
```

不会加载 Debugging、Performance 或其他 Development 档位。当前字符代理估算约 1.9k tokens；
QUICK Testing 也约 1.9k tokens。实际 token 数受 tokenizer 影响，这些数字只是防止文件增长的
工程预算。

OpenAI 集成默认关闭隐式调用，因此普通工程任务不会自动加载 skill body；安装后的 metadata
仍可能出现在 skill 列表中。其他宿主是否自动调用由其实现和用户设置决定。显式调用确实比
直接使用宿主 agent 多用一些 token，但 SMALL、QUICK、DIRECT 路径不会创建无价值文档或
默认使用 subagent。

如果极度在意一次性小任务的 token，可以不显式调用，直接使用宿主 agent；需要稳定执行本
框架时再选择 `engineering-workflow`。

仓库测试会限制常见路径、混合链路和各 intent reference 的字符预算，避免后续维护中重新
膨胀。

## 14. 当前测试数据怎样理解

`tests/evals/` 保存的是同一继承 Codex 配置、medium reasoning 的 paired forward tests：baseline
不加载 skill body，treatment 显式加载本 skill。当前 host 未暴露可核验的公开 model slug，
因此结果不冒充特定模型数据。确定性 rubric 包含 48 个 routing、授权、证据、artifact、
transition 和 subagent 检查点。

```text
frozen holdout baseline   35 / 48 = 72.9%
frozen holdout treatment  43 / 48 = 89.6%
gain                        8 checks = +16.7 percentage points
```

holdout prompts 在最终 rubric 冻结后才交给两个新 agent，评分后 rubric SHA-256 保持不变。
增益主要来自并发根因证明、Debugging -> Development -> Testing 顺序、受控性能证据和条件
修复链。另一个探索性样本为 47/48 -> 48/48，但 scorer 曾在看到输出后修正，因此不作为主要
宣传数据。

holdout 仍只有 8 个案例、不执行真实代码，而且 regex scorer 对同义表达敏感。因此它只能说明
本 skill 在这组 prompts 上改善了 routing 和 evidence discipline，不能宣传为“编码成功率提高
16.7%”。它也不证明成本、延迟、Claude Code 或其他模型/宿主上的收益。原始 JSONL、冻结
协议、rubric 和 scorer 全部保留，可复查和扩展。

<div align="center">

<img src="assets/engineering-workflows-logo.svg" width="240" alt="Engineering Workflows logo">

# Engineering Workflows

**一个入口，六种工作流，证据驱动的工程实践。**

面向 AI 编程 Agent 的目标优先工作流：根据任务选择恰当的工程过程，只加载当前需要的内容，
并把验证作为结果的一部分，而不是事后补充。

**简体中文** | [English](README.en.md)

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-open_standard-111827?style=flat-square)](https://agentskills.io)
[![Workflows](https://img.shields.io/badge/workflows-6-6366F1?style=flat-square)](#六种工作流一个入口)
[![Progressive Loading](https://img.shields.io/badge/context-progressive_loading-0EA5E9?style=flat-square)](#为什么需要它)
[![Explicit First](https://img.shields.io/badge/invocation-explicit_first-8B5CF6?style=flat-square)](#一分钟使用)
[![Holdout](https://img.shields.io/badge/holdout-43%2F48_%2889.6%25%29-10B981?style=flat-square)](#测试数据与边界)

[设计动机](#为什么需要它) ·
[安装](#一分钟安装) ·
[使用](#一分钟使用) ·
[架构](docs/architecture.md) ·
[完整指南](docs/usage.md)

</div>

---

## 为什么需要它

不同工程任务不应承担相同的流程成本。一行修复不需要跨系统重构级别的仪式；性能结论或未知
崩溃则不能在没有受控证据的情况下被接受。

Engineering Workflows 为兼容的编程 Agent 提供一个入口，并由当前目标决定执行方法：

| 原则 | 含义 |
|---|---|
| **目标优先路由** | 描述你想得到的结果，由框架选择主要工程意图。 |
| **成比例的过程** | SMALL 任务保持轻量；只有较大或高风险任务确有需要时才引入计划、工件或 subagent。 |
| **证据驱动完成** | 测试、基准、根因证明和 Review findings 都是证据，并使用明确的 PASS / FAIL / BLOCKED 语义。 |

### 六种工作流，一个入口

| 意图 | 核心问题 |
|---|---|
| **Development** | 需要有意改变什么软件行为？ |
| **Testing** | 系统是否满足明确的验收标准？ |
| **Debugging** | 什么原因导致了意外行为？ |
| **Performance** | 性能如何、原因是什么、结论在哪些受控条件下成立？ |
| **Investigation** | 现有系统实际上如何工作？ |
| **Review** | 现有改动或设计中存在哪些问题与风险？ |

只需使用宿主对应的语法调用一个 skill：

```text
Codex CLI / IDE  $engineering-workflow
ChatGPT          @engineering-workflow
Claude Code      /engineering-workflow
```

框架负责路由、workflow-specific strategy、验证深度、可选工件和目标切换。

---

## 它是什么

一个用于混合目标、高风险和证据敏感工程任务的可移植 Agent Skill。它把当前目标路由到正确的
方法，并只采用任务真正需要的过程。

```text
用户目标 + 仓库约束
    -> engineering-workflow
    -> 主要意图
    -> 一个选定的 workflow
    -> workflow-specific strategy
    -> 执行与验证
    -> 目标改变时按需切换
```

六种主要意图是 Development、Testing、Debugging、Performance、Investigation 和 Review。
用户通常只需描述想得到的结果，无需自行选择 workflow、scale、artifact 或 agent 数量。

该 skill 使用渐进加载和经过测试的上下文预算：只加载一个意图 workflow，并在必要时再加载一个
scale/strategy reference，而不是整个工作流库。常规低风险任务可直接使用宿主 Agent，无需承担
skill body 的上下文成本。

核心 skill 遵循开放的 Agent Skills 格式：一个 `SKILL.md` 入口和按需加载的 references。
`agents/openai.yaml` 是用于 UI 元数据和调用策略的可选 OpenAI 集成，非 OpenAI 宿主可以忽略。

## 为什么使用它

- 在修复未知故障前先证明根因；
- 将实现验证保留在 Development 内，避免无意义地切换工作流；
- 验证条件不可用时绝不计为 PASS；
- 性能结论必须由受控、重复的证据支持；
- 除非明确要求修复，否则 Review 保持只读；
- 当计划、handoff 和 subagent 无法提高可靠性时不使用它们。

## 一分钟安装

Codex 仓库级安装：

```bash
mkdir -p <repo>/.agents/skills
cp -r skills/engineering-workflow <repo>/.agents/skills/
```

Claude Code 仓库级安装：

```bash
mkdir -p <repo>/.claude/skills
cp -r skills/engineering-workflow <repo>/.claude/skills/
```

只安装 `engineering-workflow`。六种 workflow 是内部渐进加载的 references，不是独立 skill。
用户级安装路径和其他兼容宿主请参阅[完整安装指南](docs/usage.md#2-安装)。

## 一分钟使用

```text
$engineering-workflow

LMCache 的 REGISTER_KV_CACHE 在 DCU 环境报 HIP error，
请找到根因，修复，并补充回归测试。
```

框架首先进入 Debugging；根因得到证明后切换到 Development；最后使用 Testing 得到独立的
回归验证结论。

该 skill 采用显式调用优先策略。OpenAI 宿主通过 `agents/openai.yaml` 强制执行；其他宿主使用
各自的调用策略，因此显式选择是最可移植的用法。

## 测试数据与边界

在冻结的 8 个案例 holdout 中，相同的继承 Codex 配置在未加载 skill body 时得到 35/48
（72.9%），加载后得到 43/48（89.6%）：多通过 8 个 routing 与 evidence-discipline 检查点。
这不代表普遍的编码能力提升。冻结 rubric hash、原始 JSONL、评分器、探索性结果和限制说明
均保存在 `tests/evals/`；测试宿主未提供可验证的公开模型 slug。

## 仓库结构

```text
engineering-workflows/
├── AGENTS.md
├── README.md
├── README.en.md
├── docs/
│   ├── architecture.md
│   ├── roadmap.md
│   ├── usage.md
│   └── workflow-contract.md
├── skills/
│   └── engineering-workflow/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           ├── development/
│           ├── testing/
│           ├── debugging/
│           ├── performance/
│           ├── investigation/
│           └── review/
└── tests/
```

## 文档

- [完整使用指南](docs/usage.md)
- [架构设计](docs/architecture.md)
- [Workflow 作者契约](docs/workflow-contract.md)
- [路线图](docs/roadmap.md)

仓库特定的构建、测试、风格和平台规则仍应放在目标仓库的宿主指令文件中，例如 `AGENTS.md`
或 `CLAUDE.md`；本 skill 只提供任务执行方法。

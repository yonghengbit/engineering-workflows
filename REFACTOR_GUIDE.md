# Engineering Workflows v2 重构设计指导

## 1. 任务目标

请基于当前 `engineering-workflows` 仓库已有实现进行一次架构完善和重构。

不要从零重新设计，也不要简单推翻当前已有的：

- `adaptive-development`
- `adaptive-testing`
- `systematic-debugging`
- `performance-benchmark`
- `code-investigation`
- `code-review`
- `engineering-router`
- `workflow-contract`
- workflow scenario tests

当前版本中，各专项 workflow 的核心设计已经具有较高复用价值。

本次重构的核心目标是解决一个架构问题：

> 当前各个 workflow 作为平级 Codex Skill 暴露，并由 Codex 自身 skill matching 或用户显式选择 workflow；新的设计应改为一个统一 Engineering Workflow 入口，由 Codex 按照我们定义的轻量 Routing Policy 判断当前任务的 Primary Intent，再加载对应 workflow。

最终用户应该主要表达“我要完成什么工程任务”，而不是自己判断：

```text
这是 debugging
这是 testing
这是 development
```

框架负责完成：

```text
用户 Prompt
    ↓
Engineering Workflow
    ↓
Routing Policy
    ↓
Primary Intent
    ↓
对应 Workflow
    ↓
Workflow-specific strategy / scale
    ↓
根据任务动态决定执行方式
    ↓
必要时动态创建 subagents
    ↓
执行
    ↓
验证
    ↓
必要时发生 Workflow Transition
```

---

# 2. 核心设计原则

## 2.1 一个统一入口

整个 framework 应有一个主要 Codex Skill：

```text
engineering-workflow
```

它是用户日常工程任务的统一入口。

典型使用：

```text
$engineering-workflow

LMCache 的 REGISTER_KV_CACHE 在 DCU 环境报 HIP error，
请找到根因，修复，并补充回归测试。
```

或者：

```text
$engineering-workflow

修改 LMCache 的 KV Cache layout，
让磁盘布局直接按照 vLLM physical block layout 存储，
要求保持现有 backend 兼容。
```

用户不应该必须知道应该使用：

```text
systematic-debugging
adaptive-development
adaptive-testing
performance-benchmark
...
```

---

# 3. Router 的正确定位

Router 不应设计成：

```text
Router Agent
    ↓
spawn debugging-agent
    ↓
spawn testing-agent
```

也不要设计成一个重量级 orchestration system。

Router 本质上只是：

```text
Routing Policy
```

由当前 Codex 主 agent 根据：

```text
用户 Prompt
+
当前 repository context
+
workflow routing rules
```

判断当前 Primary Intent。

因此：

```text
Router ≠ 独立 Agent
Router ≠ 项目 AGENTS.md
Router ≠ 多 Agent 调度器
Router ≠ workflow executor
```

Router 只负责回答：

> 当前这个工程任务首先应该由哪个 workflow 接管？

一旦选择 workflow，Router 就退出当前执行阶段。

---

# 4. Router 不应该依赖项目 AGENTS.md 判断任务类型

必须明确区分两个概念。

## Repository AGENTS.md

负责：

```text
这个 repository 有什么特殊规则？
如何 build？
如何 test？
代码规范是什么？
哪些目录不能修改？
有哪些平台限制？
有哪些 repository-specific conventions？
```

即：

```text
Repository Constraints
```

## Engineering Workflow

负责：

```text
当前任务属于什么工程活动？
应该采用什么方法完成？
需要多少 planning？
需要什么 verification？
是否需要 subagent？
需要什么 artifacts？
```

即：

```text
Task Execution Methodology
```

因此整体关系应为：

```text
User Prompt
    +
Repository AGENTS.md
    │
    ▼
engineering-workflow
    │
    ▼
Routing Policy
    │
    ▼
Selected Workflow
```

而不是：

```text
AGENTS.md
    ↓
判断 Debug / Development / Testing
```

项目 `AGENTS.md` 只提供约束，不拥有 workflow routing 权限。

---

# 5. Primary Intent 分类

第一层 Router 只判断 Primary Intent。

至少保留当前六类：

```text
Development
Testing
Debugging
Performance
Investigation
Review
```

其核心问题分别是：

```text
Development
"What software behavior should be intentionally changed?"

Testing
"Does the system satisfy the required criteria?"

Debugging
"What causes this unexpected behavior?"

Performance
"How fast is the system, why, and under what conditions?"

Investigation
"How does the existing system actually work?"

Review
"What problems or risks exist in this existing change/design?"
```

不要通过关键词机械分类。

必须根据：

```text
用户当前真正想得到的结果
```

分类。

---

# 6. Routing Policy

Router 应保持简单、稳定、可预测。

建议优先采用目标判断和 precedence rules，而不是给六个 workflow 分别打复杂分数。

推荐规则：

```text
1. 已存在未知原因的错误、异常、crash、regression
   -> DEBUGGING

2. 当前主要目标是性能测量、性能解释、性能瓶颈或优化效果
   -> PERFORMANCE

3. 当前主要目标是理解现有代码、架构、调用链或数据流
   -> INVESTIGATION

4. 当前主要目标是评价已有 PR / patch / diff / design
   -> REVIEW

5. 当前主要目标是验证某项行为是否满足明确标准
   -> TESTING

6. 当前主要目标是增加或修改软件行为
   -> DEVELOPMENT
```

这只是 Router policy。

Router 不应该进一步决定：

```text
需要几个 agent
创建哪些文件
具体读哪些代码
运行哪些测试
怎么 Debug
怎么 benchmark
```

这些属于 selected workflow。

---

# 7. 混合任务的处理方式

现实任务经常同时包含：

```text
debug
implement
test
benchmark
investigate
```

不要同时激活所有 workflow。

原则：

> 由当前 Primary Intent 所属 workflow 拥有任务，直到 Primary Intent 真正发生变化。

例如：

```text
"这个 crash 是什么原因？修复后加测试。"
```

不是：

```text
Debugging + Development + Testing
同时执行
```

而是：

```text
Debugging
    ↓
root cause confirmed
    ↓
Development
    ↓
fix completed
    ↓
Testing
```

---

另一个例子：

```text
"测试这个功能，如果失败就修复。"
```

应为：

```text
Testing
    ↓
failure discovered
    ↓
Debugging
    ↓
root cause
    ↓
Development
    ↓
Testing
```

---

性能任务：

```text
"这个 kernel 很慢，找到瓶颈并优化。"
```

通常：

```text
Performance
    ↓
establish baseline
    ↓
locate bottleneck
    ↓
必要时 Investigation
    ↓
Development
    ↓
Performance
```

最后必须重新 benchmark。

---

Review：

```text
"Review 这个 PR，把严重问题修掉。"
```

应该：

```text
Review
    ↓
confirmed findings
    ↓
Development
    ↓
Testing
```

---

Investigation：

```text
"先梳理 Scheduler 的 KV block 生命周期，然后增加一种回收策略。"
```

应该：

```text
Investigation
    ↓
mental model established
    ↓
Development
```

---

# 8. Supporting Activity 不等于 Workflow Transition

必须避免过度 routing。

例如 Development 为了修改代码：

```text
阅读调用链
运行测试
查看 benchmark
```

不意味着必须：

```text
Development
-> Investigation
-> Testing
-> Performance
```

只有当 Primary Deliverable 改变时才 transition。

例如：

```text
Development 中运行 unit test
```

仍然属于 Development verification。

但是：

```text
测试发现未知 failure，
下一阶段目标变成“证明 failure 的根因”
```

才 transition：

```text
Development -> Debugging
```

---

# 9. Workflow-specific Strategy

第一层 Router 不进行复杂度判断。

选择 workflow 后，由对应 workflow 自己决定 strategy。

不要把：

```text
SMALL / MEDIUM / LARGE / VERY_LARGE
```

机械套给所有 workflow。

保留当前设计思想。

例如：

```text
Development
    -> SMALL
    -> MEDIUM
    -> LARGE
    -> VERY_LARGE
```

Testing：

```text
Testing
    -> QUICK
    -> STRUCTURED
    -> VALIDATION
```

Debugging：

```text
Debugging
    -> DIRECT
    -> SYSTEMATIC
```

Performance：

可以继续使用当前已有：

```text
CHECK
COMPARISON
CHARACTERIZATION
```

Investigation 和 Review 不需要为了“统一”强行创造四档规模。

只有 workflow 内部策略会实质改变执行方式时，才增加分类。

---

# 10. Development 四档机制应继续保留

当前 `adaptive-development` 的四档设计是 framework 中重要且成熟的一部分，应尽量保留。

核心维度：

```text
Scope
Uncertainty
Risk
Parallelism
```

继续使用：

```text
SMALL
MEDIUM
LARGE
VERY_LARGE
```

并保留动态 re-evaluation。

例如：

```text
Initial understanding
    ↓
initial classification
    ↓
exploration
    ↓
reclassification
    ↓
planning/design
    ↓
reclassification
    ↓
implementation
    ↓
major phase checkpoint
    ↓
final verification
```

但不要把 reclassification 做成每修改一个文件就重新评分。

保持：

```text
fixed checkpoints
+
event-triggered re-evaluation
```

---

# 11. Artifact 原则

Artifact 必须：

```text
按需生成
```

而不是：

```text
每个任务固定生成一套 markdown
```

Router 自己：

```text
不生成 artifact。
```

不同 workflow 自己负责决定。

例如 Development：

```text
SMALL
    no artifact

MEDIUM
    PLAN.md
    HANDOFF.md

LARGE
    DESIGN.md
    PLAN.md
    HANDOFF.md

VERY_LARGE
    DESIGN.md
    ROADMAP.md
    plans/*
    handoffs/*
```

Testing 可继续：

```text
QUICK
    no artifact

STRUCTURED
    TEST_PLAN.md
    TEST_REPORT.md

VALIDATION
    VALIDATION_PLAN.md
    results/
    VALIDATION_REPORT.md
```

Debugging 可继续：

```text
DIRECT
    no persistent artifact

SYSTEMATIC
    DEBUG.md
```

Performance：

```text
BENCHMARK_PLAN.md
results/
BENCHMARK_REPORT.md
```

Investigation：

小任务直接输出结果。

复杂、跨 session 或需要 handoff 时：

```text
INVESTIGATION.md
```

Review：

默认直接输出 findings。

不要为了 workflow framework 看起来“完整”而制造文档。

---

# 12. Subagent / Multi-Agent 设计

这是本次架构需要明确完善的一部分。

不要提前定义固定的：

```text
debug-agent
testing-agent
performance-agent
cuda-agent
review-agent
```

也不要让 Router 创建这些 agent。

应该：

```text
Selected Workflow
        +
Current Prompt
        +
Current Repository
        ↓
动态判断是否需要 subagents
```

例如一个 LARGE Development：

```text
main agent
    │
    ├── subagent: trace scheduler-side ownership
    ├── subagent: inspect connector/backend compatibility
    └── subagent: inspect relevant tests
```

另一个完全不同的 LARGE Development 可能是：

```text
main agent
    │
    ├── subagent: CUDA backend
    ├── subagent: ROCm backend
    └── subagent: benchmark infrastructure
```

agent role 应来自实际任务，而不是 framework 预先写死。

---

# 13. Subagent 创建原则

只有满足以下条件才考虑并行：

```text
clear ownership
weak dependencies
low edit conflict
explicit input
explicit output
independent verification
```

适合 subagent 的任务：

```text
独立代码路径调查
不同 backend 调查
独立 compatibility analysis
独立测试实现
benchmark infrastructure
大项目不同 phase 的准备工作
```

不适合：

```text
后一阶段依赖前一阶段定义接口
多个 agent 会修改同一组核心文件
任务本身很小
只是为了“显得是 multi-agent”
```

Router 不负责决定是否使用 subagent。

具体 workflow 做这个决定。

---

# 14. 推荐目标目录结构

请优先将当前平级 Skills 重构为：

```text
engineering-workflows/
│
├── README.md
├── AGENTS.md
│
├── docs/
│   ├── architecture.md
│   ├── workflow-contract.md
│   ├── roadmap.md
│   └── usage.md
│
├── skills/
│   └── engineering-workflow/
│       │
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       │
│       └── references/
│           │
│           ├── development/
│           │   ├── workflow.md
│           │   ├── small.md
│           │   ├── medium.md
│           │   ├── large.md
│           │   └── very-large.md
│           │
│           ├── testing/
│           │   ├── workflow.md
│           │   ├── quick.md
│           │   ├── structured.md
│           │   └── validation.md
│           │
│           ├── debugging/
│           │   └── workflow.md
│           │
│           ├── performance/
│           │   └── workflow.md
│           │
│           ├── investigation/
│           │   └── workflow.md
│           │
│           └── review/
│               └── workflow.md
│
└── tests/
    ├── test_workflow_structure.py
    └── workflow-scenarios.md
```

这里：

```text
SKILL.md
```

只负责：

```text
common contract
routing policy
workflow loading
transition rules
common execution principles
```

不要把六套 workflow 的详细执行内容全部塞进顶层 `SKILL.md`。

---

# 15. 当前文件的迁移建议

尽量复用当前内容。

大致映射：

```text
skills/engineering-router/SKILL.md
    ->
skills/engineering-workflow/SKILL.md
```

但需要修改：

```text
"optional fallback router"
```

为：

```text
"canonical engineering workflow entry point"
```

---

当前：

```text
skills/adaptive-development/SKILL.md
```

迁移成：

```text
skills/engineering-workflow/references/development/workflow.md
```

当前：

```text
skills/adaptive-development/references/*
```

迁移到：

```text
references/development/*
```

---

当前：

```text
adaptive-testing/SKILL.md
adaptive-testing/references/*
```

迁移到：

```text
references/testing/workflow.md
references/testing/*
```

---

当前：

```text
systematic-debugging/SKILL.md
```

迁移为：

```text
references/debugging/workflow.md
```

---

同理：

```text
performance-benchmark
code-investigation
code-review
```

分别迁移到对应 reference。

迁移时不要简单复制。

应检查：

```text
哪些内容属于 routing
哪些属于 workflow
哪些属于 common contract
哪些存在重复
哪些 transition 描述可以统一
```

然后进行去重。

---

# 16. 是否保留旧 Skill

当前项目还是第一版，因此优先考虑架构清晰，而不是为了兼容制造长期复杂度。

理想状态：

```text
skills/
    engineering-workflow/
```

成为唯一默认安装 Skill。

旧的：

```text
adaptive-development
adaptive-testing
systematic-debugging
...
```

不应继续作为平级、默认自动发现的主要 workflow，否则会重新出现：

```text
Codex built-in skill matching
直接绕过 Router
```

的问题。

如果确实需要兼容旧调用方式，可以设计 compatibility wrapper，但必须满足：

```text
1. wrapper 不复制 workflow 内容；
2. wrapper 只固定 Primary Intent；
3. 实际规则仍来自 engineering-workflow；
4. compatibility skill 不应重新成为主要架构。
```

如果当前仓库没有实际兼容性负担，可以直接完成干净迁移。

---

# 17. Workflow Loading 原则

顶层 Skill 不应一开始读取全部 workflow。

应该采用 progressive loading。

例如 Router 判断：

```text
DEBUGGING
```

则只加载：

```text
references/debugging/workflow.md
```

如果任务随后 transition：

```text
Debugging -> Development
```

再加载：

```text
references/development/workflow.md
```

Development 判断：

```text
LARGE
```

再加载：

```text
references/development/large.md
```

不要：

```text
启动时加载六个 workflow
+
所有 development 四档
+
所有 testing 三档
```

这样会使 workflow context 过重。

---

# 18. Workflow Transition Contract

继续保留当前 workflow contract 的思路，但建议统一精简 transition payload。

例如：

```text
From:
To:

Current Objective:
Verified Findings / Evidence:
Constraints:
Changed Files:
Known Reproduction / Procedure:
Required Next Action:
Verification Needed:
```

只传递目标 workflow 真正需要的信息。

不要把整个 previous workflow 的思考过程复制过去。

---

# 19. Source of Truth

保持以下原则：

软件实现：

```text
current code
+
git diff
```

运行行为：

```text
actual test / benchmark / runtime evidence
```

workflow 状态：

```text
workflow designated artifacts
```

文档和实际代码冲突时：

```text
实际代码和实际观测优先。
```

同时修复 stale documentation。

---

# 20. 不要做的事情

本次重构明确禁止以下方向。

不要：

```text
把 Router 做成独立 subagent。
```

不要：

```text
让 AGENTS.md 决定 Debug / Development / Testing。
```

不要：

```text
依赖 Codex 自由 skill matching 完成内部 workflow routing。
```

Codex 可以判断，但必须按照本 framework 的 routing policy 判断。

不要：

```text
六个 workflow 全部同时激活。
```

不要：

```text
把所有 workflow 内容塞进一个巨大的 SKILL.md。
```

不要：

```text
为了统一而给所有 workflow 强行套 SMALL/MEDIUM/LARGE/VERY_LARGE。
```

不要：

```text
预定义一堆固定专业 agent。
```

不要：

```text
LARGE 就默认 multi-agent。
```

不要：

```text
每次 workflow transition 都创建新的 markdown。
```

不要：

```text
每做一个小动作就重新 classification。
```

---

# 21. 必须补充的使用文档

完成代码和 Skill 重构后，请创建：

```text
docs/usage.md
```

使用文档应以实际使用者为对象，而不是 workflow 作者。

建议中文撰写，Skill 名、命令、文件名保持英文。

至少覆盖以下内容。

## 21.1 这个项目解决什么问题

解释：

```text
用户只描述工程目标
↓
engineering-workflow
↓
自动判断任务类型
↓
自动采用正确工程方法
```

---

## 21.2 安装方式

说明 user scope 和 repository scope。

重点解释推荐的使用方式。

---

## 21.3 如何启动

给出最简单例子：

```text
$engineering-workflow

实现一个新的 KV Cache backend。
```

强调用户一般不需要：

```text
指定 DEVELOPMENT
指定 LARGE
指定创建几个 agent
指定 PLAN.md
```

framework 自动决定。

---

## 21.4 六类任务示例

至少分别给出：

```text
Development
Testing
Debugging
Performance
Investigation
Review
```

真实 prompt 示例。

---

## 21.5 混合任务示例

例如：

```text
这个 crash 帮我找到原因，修复并加测试。
```

解释内部：

```text
Debugging
-> Development
-> Testing
```

---

## 21.6 Development 四档

解释：

```text
SMALL
MEDIUM
LARGE
VERY_LARGE
```

用户不需要自己判断。

解释什么时候可能产生：

```text
PLAN.md
DESIGN.md
ROADMAP.md
HANDOFF.md
```

---

## 21.7 Subagent

解释：

```text
什么时候 Codex 可能创建 subagent
为什么不是所有大任务都需要 multi-agent
agent role 为什么根据任务动态生成
```

---

## 21.8 AGENTS.md 与 engineering-workflow 的区别

必须专门写一节。

解释：

```text
AGENTS.md
= repository-specific rules

engineering-workflow
= task execution methodology
```

避免用户认为必须把 workflow 逻辑写进每个项目 `AGENTS.md`。

---

## 21.9 完整使用示例

至少给出三个完整例子：

### 示例一：小开发

```text
增加一个 CLI flag
```

展示：

```text
Development
-> SMALL
-> implementation
-> test
```

---

### 示例二：Debug + Fix

```text
REGISTER_KV_CACHE crash
```

展示：

```text
Debugging
-> root cause
-> Development
-> Testing
```

---

### 示例三：复杂性能优化

例如：

```text
优化 GPU KV transfer kernel
```

展示：

```text
Performance
-> baseline
-> bottleneck
-> Investigation if needed
-> Development
-> benchmark verification
```

---

# 22. README 的定位

重构后同步更新根目录：

```text
README.md
```

README 不应该取代完整 `docs/usage.md`。

README 只负责：

```text
项目是什么
核心架构
一分钟安装
一分钟使用
目录结构
链接到 docs/usage.md
```

完整使用说明放到：

```text
docs/usage.md
```

架构设计继续放：

```text
docs/architecture.md
```

workflow 作者规范继续放：

```text
docs/workflow-contract.md
```

---

# 23. 测试和验证

现有：

```text
tests/test_workflow_structure.py
tests/workflow-scenarios.md
```

应该保留并扩展。

至少覆盖下面的 routing scenarios。

```text
"Add one optional CLI flag."
=> Development / SMALL
```

```text
"Run the existing unit tests and tell me whether they pass."
=> Testing / QUICK
```

```text
"REGISTER_KV_CACHE crashes; find the root cause and fix it."
=> Debugging
   -> Development
   -> Testing
```

```text
"Trace how Scheduler allocates and frees KV blocks."
=> Investigation
```

```text
"Review this PR and report correctness problems."
=> Review
```

```text
"Compare baseline and new kernel throughput."
=> Performance
```

```text
"This kernel is slow. Find the bottleneck, optimize it, and verify the gain."
=> Performance
   -> optional Investigation
   -> Development
   -> Performance
```

```text
"Test this feature; if it fails, diagnose and fix it."
=> Testing
   -> Debugging
   -> Development
   -> Testing
```

还要增加 failure cases，验证 Router 不会：

```text
因为 prompt 出现 "test" 就一定选择 Testing；
因为任务需要读代码就 transition 到 Investigation；
因为任务很大就一定创建多个 agents；
因为 Development 最后跑 benchmark 就错误 transition；
一次加载所有 workflow。
```

---

# 24. Acceptance Criteria

最终实现至少满足：

### Architecture

- 存在一个 canonical `engineering-workflow` Skill。
- Router 是轻量 routing policy，而不是独立 agent。
- Router 只负责 Primary Intent。
- 六类 workflow 边界清晰。
- workflow strategy 和 task type 分层。
- Development 四档机制得到保留。
- supporting activity 与 workflow transition 有明确区别。

### Context Efficiency

- 不默认加载全部 workflow。
- 不默认加载 Development 全部四档。
- 按需 progressive load reference。

### Agents

- Router 不创建 agents。
- workflow 可以按任务动态决定 subagents。
- 不维护固定专业 agent taxonomy。
- multi-agent 使用有明确适用条件。

### Artifacts

- artifact proportional to task complexity。
- Router 不创建 artifact。
- SMALL / QUICK 等轻量任务没有文档 ceremony。

### Repository Rules

- repository `AGENTS.md` 与 workflow routing 职责分离。
- workflow framework 不把项目特定规则硬编码进 reusable workflow。

### Documentation

- README 已更新。
- architecture 已更新。
- workflow-contract 与新架构一致。
- 创建完整 `docs/usage.md`。
- 所有示例与实际最终目录和 Skill 名称一致。

### Validation

- structure tests 通过。
- workflow scenarios 已根据新架构更新。
- 不保留明显 stale documentation。
- 最终检查 git diff，避免旧架构和新架构描述同时存在造成冲突。

---

# 25. 实施要求

请直接在当前 repository 中完成修改，而不仅仅输出设计建议。

执行顺序建议：

```text
1. Inspect 当前 repository
2. 对照本设计识别可复用内容
3. 确定 migration plan
4. 建立 engineering-workflow canonical structure
5. 迁移并去重现有 workflows
6. 实现 routing policy
7. 更新 workflow transition contract
8. 更新 tests
9. 编写 docs/usage.md
10. 更新 architecture / README / roadmap
11. 搜索 stale references
12. 运行 structural tests
13. 检查 final git diff
```

原则：

```text
Reuse > Rewrite
Simplify > Duplicate
Policy > Hardcoded Agent Graph
Progressive Loading > Load Everything
Primary Intent > Keyword Matching
Dynamic Execution > Ceremony
```

---

# 26. 最终向我汇报

完成后不要只说“已完成”。

请明确给出：

```text
1. 最终目录结构
2. 哪些旧文件被迁移 / 删除 / 保留
3. Router 最终如何工作
4. 六个 workflow 如何被加载
5. workflow transition 如何处理
6. Development 四档是否保持原逻辑
7. Subagent 策略如何实现
8. AGENTS.md 在新架构中的角色
9. 新增/修改了哪些测试
10. docs/usage.md 包含哪些内容
11. 实际运行了哪些验证
12. 还有哪些已知限制
```

如果在实际实现过程中发现本设计与 Codex Skill 的真实机制存在冲突，不要默默绕过。

应：

```text
先验证实际机制
-> 保留本设计的核心目标
-> 采用最小必要调整
-> 在最终报告明确说明调整原因
```

本次重构最终追求的不是“Skill 数量更多”，而是：

> 用户只需要描述工程目标，Codex 在一个稳定、可解释的工程工作流框架下，自主选择正确的方法、正确的过程深度和必要的执行资源。
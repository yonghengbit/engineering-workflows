import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SKILL = SKILLS / "engineering-workflow"
EXPECTED_REFERENCES = {
    "development/workflow.md",
    "development/small.md",
    "development/medium.md",
    "development/large.md",
    "development/very-large.md",
    "testing/workflow.md",
    "testing/quick.md",
    "testing/structured.md",
    "testing/validation.md",
    "debugging/workflow.md",
    "performance/workflow.md",
    "investigation/workflow.md",
    "review/workflow.md",
}
LEGACY_SKILLS = {
    "adaptive-development",
    "adaptive-testing",
    "systematic-debugging",
    "performance-benchmark",
    "code-investigation",
    "code-review",
    "engineering-router",
}


def read_frontmatter(skill_md: Path) -> tuple[dict[str, str], str]:
    text = skill_md.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise AssertionError(f"{skill_md} does not start with YAML frontmatter")

    fields: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        match = re.fullmatch(r"([a-z_]+):\s*(.+)", line)
        if not match:
            raise AssertionError(f"Unsupported frontmatter line in {skill_md}: {line}")
        fields[match.group(1)] = match.group(2).strip().strip('"')
    return fields, parts[2]


class WorkflowStructureTests(unittest.TestCase):
    def test_only_canonical_skill_is_installable(self) -> None:
        actual = {
            path.name
            for path in SKILLS.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        self.assertEqual({"engineering-workflow"}, actual)
        for legacy in LEGACY_SKILLS:
            self.assertFalse((SKILLS / legacy / "SKILL.md").exists())

    def test_canonical_skill_metadata(self) -> None:
        skill_md = SKILL / "SKILL.md"
        fields, body = read_frontmatter(skill_md)
        self.assertEqual({"name", "description"}, set(fields))
        self.assertEqual("engineering-workflow", fields["name"])
        self.assertRegex(fields["description"], r"\bUse (?:explicitly|when|for)\b")
        self.assertNotRegex(fields["description"], r"(?i)\bcodex\b|\bclaude\b|\bopenai\b")
        self.assertLessEqual(len(fields["description"]), 420)
        self.assertLess(len(skill_md.read_text(encoding="utf-8").splitlines()), 500)
        self.assertNotRegex(body, r"(?i)\bTODO\b|\[TODO\]")
        self.assertFalse((SKILL / "README.md").exists())
        self.assertIn("`AGENTS.md`", body)
        self.assertIn("`CLAUDE.md`", body)

        interface = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Engineering Workflow"', interface)
        self.assertIn("$engineering-workflow", interface)
        self.assertIn("allow_implicit_invocation: false", interface)
        short = re.search(r'short_description:\s*"([^"]+)"', interface)
        self.assertIsNotNone(short)
        self.assertGreaterEqual(len(short.group(1)), 25)
        self.assertLessEqual(len(short.group(1)), 64)

    def test_reference_tree_is_exact_and_instruction_only(self) -> None:
        reference_root = SKILL / "references"
        actual = {
            path.relative_to(reference_root).as_posix()
            for path in reference_root.rglob("*.md")
        }
        self.assertEqual(EXPECTED_REFERENCES, actual)

        for relative in sorted(EXPECTED_REFERENCES):
            with self.subTest(reference=relative):
                text = (reference_root / relative).read_text(encoding="utf-8")
                self.assertFalse(text.startswith("---"))
                self.assertNotRegex(text, r"(?i)\bTODO\b|\[TODO\]")

    def test_router_maps_each_intent_to_one_workflow(self) -> None:
        top = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        routing = top.split("## Route by Requested Result", 1)[1].split(
            "## Load Progressively", 1
        )[0]
        expected = {
            "Development": "references/development/workflow.md",
            "Testing": "references/testing/workflow.md",
            "Debugging": "references/debugging/workflow.md",
            "Performance": "references/performance/workflow.md",
            "Investigation": "references/investigation/workflow.md",
            "Review": "references/review/workflow.md",
        }
        for intent, path in expected.items():
            with self.subTest(intent=intent):
                self.assertRegex(routing, rf"\| {intent} \|[^\n]+`{re.escape(path)}` \|")
                self.assertEqual(1, routing.count(f"`{path}`"))

    def test_progressive_loading_is_explicit(self) -> None:
        top = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(top, r"Load exactly one workflow(?: file)?")
        self.assertRegex(top, r"Never preload (?:all workflows or strategies|alternatives)")
        for relative in sorted(EXPECTED_REFERENCES):
            if relative.endswith("workflow.md"):
                self.assertIn(f"`references/{relative}`", top)

    def test_context_budget_for_common_paths(self) -> None:
        """Use characters as a deterministic proxy; rough English token cost is chars / 4."""
        top = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        references = SKILL / "references"

        self.assertLessEqual(len(top), 4_200)

        intent_budgets = {
            "development/workflow.md": 2_700,
            "testing/workflow.md": 2_800,
            "debugging/workflow.md": 4_200,
            "performance/workflow.md": 4_200,
            "investigation/workflow.md": 3_000,
            "review/workflow.md": 3_400,
        }
        for relative, budget in intent_budgets.items():
            with self.subTest(reference=relative):
                text = (references / relative).read_text(encoding="utf-8")
                self.assertLessEqual(len(text), budget)

        small_path = top + (references / "development/workflow.md").read_text(
            encoding="utf-8"
        ) + (references / "development/small.md").read_text(encoding="utf-8")
        quick_path = top + (references / "testing/workflow.md").read_text(
            encoding="utf-8"
        ) + (references / "testing/quick.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(small_path), 7_500)
        self.assertLessEqual(len(quick_path), 7_500)

        mixed_path = top + "".join(
            (references / relative).read_text(encoding="utf-8")
            for relative in (
                "debugging/workflow.md",
                "development/workflow.md",
                "development/small.md",
                "testing/workflow.md",
                "testing/quick.md",
            )
        )
        self.assertLessEqual(len(mixed_path), 14_800)
        for relative in sorted(EXPECTED_REFERENCES):
            if not relative.endswith("workflow.md"):
                self.assertIn(f"`references/{relative}`", top)

    def test_router_does_not_own_agents_or_artifacts(self) -> None:
        top = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("The router creates no artifacts or subagents", top)
        for condition in ("independent", "low-conflict", "explicit", "verification"):
            self.assertIn(condition, top)

    def test_user_and_author_docs_match_canonical_entry(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
        contract = (ROOT / "docs" / "workflow-contract.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("docs/usage.md", readme)
        self.assertIn("# Engineering Workflows\n", readme)
        self.assertNotIn("# Engineering Workflows for Codex", readme)
        self.assertIn("open Agent Skills", readme)
        self.assertIn("$engineering-workflow", usage)
        self.assertIn("/engineering-workflow", usage)
        self.assertIn(".agents/skills", usage)
        self.assertIn(".claude/skills", usage)
        self.assertIn("宿主指令文件与 engineering-workflow 的区别", usage)
        self.assertIn("one installable `SKILL.md`", contract)
        for intent in (
            "Development",
            "Testing",
            "Debugging",
            "Performance",
            "Investigation",
            "Review",
        ):
            self.assertIn(intent, usage)

    def test_local_markdown_links_resolve(self) -> None:
        markdown_files = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)")
        for source in markdown_files:
            text = source.read_text(encoding="utf-8")
            for target in pattern.findall(text):
                if "://" in target:
                    continue
                with self.subTest(source=source.name, target=target):
                    self.assertTrue((source.parent / target).resolve().is_file())

    def test_active_text_has_no_trailing_whitespace(self) -> None:
        text_files = [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            *sorted((ROOT / "docs").rglob("*.md")),
            *sorted(SKILL.rglob("*.md")),
            *sorted((ROOT / "tests").glob("*.md")),
            *sorted((ROOT / "tests").glob("*.py")),
            *sorted((ROOT / "tests" / "evals").rglob("*.md")),
            *sorted((ROOT / "tests" / "evals").rglob("*.json")),
            *sorted((ROOT / "tests" / "evals").rglob("*.jsonl")),
            *sorted((ROOT / "tests" / "evals").rglob("*.py")),
        ]
        for source in text_files:
            for line_number, line in enumerate(
                source.read_text(encoding="utf-8").splitlines(), start=1
            ):
                with self.subTest(source=source.name, line=line_number):
                    self.assertEqual(line.rstrip(), line)

    def test_required_scenarios_and_failure_cases_are_preserved(self) -> None:
        scenarios = (ROOT / "tests" / "workflow-scenarios.md").read_text(
            encoding="utf-8"
        )
        required_prompts = (
            "Add one optional CLI flag.",
            "Run the existing unit tests and tell me whether they pass.",
            "REGISTER_KV_CACHE crashes; find the root cause and fix it.",
            "Trace how Scheduler allocates and frees KV blocks.",
            "Review this PR and report correctness problems.",
            "Compare baseline and new kernel throughput.",
            "This kernel is slow. Find the bottleneck, optimize it, and verify the gain.",
            "Test this feature; if it fails, diagnose and fix it.",
        )
        for prompt in required_prompts:
            with self.subTest(prompt=prompt):
                self.assertIn(prompt, scenarios)

        for failure in (
            "Keyword trap",
            "Supporting activity trap",
            "Large-task agent trap",
            "Benchmark verification trap",
            "Eager-loading trap",
        ):
            self.assertIn(failure, scenarios)

    def test_proposals_never_contain_installable_skills(self) -> None:
        proposals = ROOT / "proposals"
        if proposals.exists():
            self.assertEqual([], list(proposals.rglob("SKILL.md")))

    def test_paired_forward_eval_is_reproducible(self) -> None:
        evals = ROOT / "tests" / "evals"
        rubric = json.loads((evals / "rubric.json").read_text(encoding="utf-8"))
        self.assertEqual({f"C{index}" for index in range(1, 9)}, set(rubric))
        self.assertTrue(all(len(checks) == 6 for checks in rubric.values()))

        scores = {}
        for label in ("baseline", "treatment"):
            run = evals / "results" / f"{label}-inherited-codex-medium-2026-08-12.jsonl"
            completed = subprocess.run(
                [sys.executable, str(evals / "score_run.py"), str(run)],
                check=True,
                capture_output=True,
                text=True,
            )
            scores[label] = json.loads(completed.stdout)
            self.assertEqual(48, scores[label]["total"])

        self.assertGreater(scores["treatment"]["passed"], scores["baseline"]["passed"])

        holdout_scores = {}
        for label in ("baseline", "treatment"):
            run = (
                evals
                / "results"
                / f"holdout-{label}-inherited-codex-medium-2026-08-12.jsonl"
            )
            completed = subprocess.run(
                [sys.executable, str(evals / "score_run.py"), str(run)],
                check=True,
                capture_output=True,
                text=True,
            )
            holdout_scores[label] = json.loads(completed.stdout)
            self.assertEqual(48, holdout_scores[label]["total"])

        self.assertGreater(
            holdout_scores["treatment"]["passed"], holdout_scores["baseline"]["passed"]
        )
        self.assertEqual(8, holdout_scores["treatment"]["passed"] - holdout_scores["baseline"]["passed"])


if __name__ == "__main__":
    unittest.main()

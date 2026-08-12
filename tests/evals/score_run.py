import json
import re
import sys
from pathlib import Path


def text(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: score_run.py <results.jsonl>", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parent
    rubric = json.loads((root / "rubric.json").read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    required_fields = {
        "case_id",
        "initial_objective",
        "strategy_or_scale",
        "transitions",
        "artifacts",
        "subagents",
        "safeguards",
    }

    passed = 0
    total = 0
    details = []
    seen = set()
    for record in records:
        if set(record) != required_fields:
            raise ValueError(
                f"{record.get('case_id', '<missing>')} fields differ from schema: "
                f"{sorted(set(record) ^ required_fields)}"
            )
        match = re.search(r"(\d+)$", record["case_id"])
        if not match:
            raise ValueError(f"case_id has no numeric suffix: {record['case_id']}")
        case = f"C{match.group(1)}"
        if case not in rubric:
            raise ValueError(f"unexpected case: {record['case_id']}")
        if case in seen:
            raise ValueError(f"duplicate normalized case: {case}")
        seen.add(case)
        case_passed = 0
        failures = []
        for label, field, pattern in rubric[case]:
            total += 1
            if re.search(pattern, text(record.get(field, "")), re.IGNORECASE | re.DOTALL):
                passed += 1
                case_passed += 1
            else:
                failures.append(label)
        details.append({"case": case, "passed": case_passed, "total": len(rubric[case]), "failures": failures})

    if seen != set(rubric):
        raise ValueError(f"missing cases: {sorted(set(rubric) - seen)}")

    print(json.dumps({
        "passed": passed,
        "total": total,
        "score_percent": round(100 * passed / total, 1),
        "cases": details,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

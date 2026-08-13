import argparse
import hashlib
import json
import math
import re
from pathlib import Path


FIELDS = {
    "case_id",
    "objective",
    "approach",
    "transitions",
    "artifacts",
    "agents",
    "evidence",
    "stop_conditions",
    "loaded_files",
}


def compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def proxy_tokens(characters: int) -> int:
    return math.ceil(characters / 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--source-manifest", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    rubric_path = root / "rubric.json"
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in args.run.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    passed = 0
    total = 0
    loaded_characters = 0
    output_characters = 0
    seen = set()
    loaded_once = set()
    details = []
    manifest = None
    if args.source_manifest:
        manifest = json.loads(args.source_manifest.read_text(encoding="utf-8"))["files"]

    for record in records:
        if set(record) != FIELDS:
            raise ValueError(f"{record.get('case_id')} fields differ: {sorted(set(record) ^ FIELDS)}")
        case = record["case_id"]
        if case not in rubric or case in seen:
            raise ValueError(f"unexpected or duplicate case: {case}")
        seen.add(case)

        failures = []
        case_passed = 0
        for label, field, pattern in rubric[case]:
            total += 1
            if re.search(pattern, compact(record[field]), re.IGNORECASE | re.DOTALL):
                passed += 1
                case_passed += 1
            else:
                failures.append(label)

        files = record["loaded_files"]
        if not isinstance(files, list) or any(not isinstance(path, str) for path in files):
            raise ValueError(f"{case} loaded_files must be a string list")
        if files and args.skill_root is None and manifest is None:
            raise ValueError("--skill-root or --source-manifest is required when loaded_files is not empty")
        for relative in files:
            canonical = relative.replace("\\", "/").casefold()
            if canonical not in loaded_once:
                loaded_once.add(canonical)
                if manifest is not None:
                    if relative not in manifest:
                        raise ValueError(f"loaded file absent from source manifest: {relative}")
                    entry = manifest[relative]
                    loaded_characters += entry["characters"]
                    if args.skill_root is not None:
                        candidate = (args.skill_root / relative).resolve()
                        skill_root = args.skill_root.resolve()
                        if candidate != skill_root and skill_root not in candidate.parents:
                            raise ValueError(f"path escapes skill root: {relative}")
                        if not candidate.is_file():
                            raise ValueError(f"loaded file does not exist: {relative}")
                        content = normalized_text(candidate)
                        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
                        if len(content) != entry["characters"] or digest != entry["sha256"]:
                            raise ValueError(f"source differs from manifest: {relative}")
                else:
                    candidate = (args.skill_root / relative).resolve()
                    skill_root = args.skill_root.resolve()
                    if candidate != skill_root and skill_root not in candidate.parents:
                        raise ValueError(f"path escapes skill root: {relative}")
                    if not candidate.is_file():
                        raise ValueError(f"loaded file does not exist: {relative}")
                    loaded_characters += len(normalized_text(candidate))

        output_record = {key: value for key, value in record.items() if key != "loaded_files"}
        output_characters += len(compact(output_record))
        details.append({"case": case, "passed": case_passed, "total": len(rubric[case]), "failures": failures})

    if seen != set(rubric):
        raise ValueError(f"missing cases: {sorted(set(rubric) - seen)}")

    print(json.dumps({
        "rubric_sha256": hashlib.sha256(rubric_path.read_bytes()).hexdigest(),
        "passed": passed,
        "total": total,
        "score_percent": round(100 * passed / total, 1),
        "unique_loaded_files": len(loaded_once),
        "loaded_characters": loaded_characters,
        "loaded_token_proxy": proxy_tokens(loaded_characters),
        "output_characters": output_characters,
        "output_token_proxy": proxy_tokens(output_characters),
        "combined_token_proxy": proxy_tokens(loaded_characters + output_characters),
        "cases": details,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

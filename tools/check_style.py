"""Check a limited set of PEP 8 rules without third-party dependencies.

This is not a replacement for a full pycodestyle or Ruff check.
"""

from pathlib import Path


def main():
    """Report basic formatting violations and return a process exit code."""
    root = Path(__file__).resolve().parents[1]
    paths = sorted(root.glob("*.py"))
    paths += sorted((root / "tests").glob("*.py"))
    paths += sorted((root / "tools").glob("*.py"))
    violations = 0
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            messages = []
            if len(line) > 79:
                messages.append(f"E501 line too long ({len(line)} > 79)")
            if line.rstrip() != line:
                messages.append("W291 trailing whitespace")
            if "\t" in line:
                messages.append("W191 tab character")
            if line.startswith("def ") and number > 1:
                blanks = 0
                for previous in reversed(lines[:number - 1]):
                    if previous.strip():
                        break
                    blanks += 1
                if blanks != 2:
                    messages.append(
                        f"E302 expected 2 blank lines, found {blanks}"
                    )
            for message in messages:
                print(f"{path.relative_to(root)}:{number}: {message}")
                violations += 1
    print(f"Basic style check: {violations} violations in {len(paths)} files.")
    return int(violations > 0)


if __name__ == "__main__":
    raise SystemExit(main())

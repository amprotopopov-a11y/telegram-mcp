import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXACT_PIN = re.compile(
    r"^([A-Za-z0-9_.-]+)(?:\[[A-Za-z0-9_,.-]+\])?==([^\s;]+)$"
)


def test_container_uses_complete_exact_lock_with_mcp_1_30_0():
    requirements = []
    for raw in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            requirements.append(line)

    matches = [EXACT_PIN.fullmatch(line) for line in requirements]
    assert all(matches), "every container distribution must be exactly pinned"
    normalized = {
        re.sub(r"[-_.]+", "-", match.group(1)).lower(): match.group(2)
        for match in matches
        if match is not None
    }
    assert len(normalized) == len(requirements), "container lock has duplicate packages"
    assert normalized["mcp"] == "1.30.0"

    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "COPY requirements.txt ./" in dockerfile
    assert "pip install --no-cache-dir -r requirements.txt" in dockerfile

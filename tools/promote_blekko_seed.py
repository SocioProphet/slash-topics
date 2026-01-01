from pathlib import Path
import json
from blake3 import blake3

ROOT = Path(__file__).resolve().parents[1]

SEED = ROOT / "data/blekko/blekko_slashtags_2012-10-15.json"
PACK = ROOT / "protocols/slash-topics/core@0.1.0"
TOPICS_OUT = PACK / "topics.json"
MANIFEST = PACK / "manifest.json"
PACK_JSON = PACK / "pack.json"

raw = json.loads(SEED.read_text(encoding="utf-8"))
SNAPSHOT = raw.get("snapshot", "2012-10-15")

topics = []
categories = raw.get("categories", {})
builtins = raw.get("builtins", [])

# -------------------------------------------------
# Categories: dict[str, list[str]]
# -------------------------------------------------
if isinstance(categories, dict):
    for category, slashes in categories.items():
        if not isinstance(slashes, list):
            continue
        for s in slashes:
            if not isinstance(s, str) or not s.strip():
                continue
            slash = "/" + s.strip().lstrip("/")
            topics.append({
                "name": slash.lstrip("/"),
                "slash": slash,
                "category": category,
                "description": "",
                "source": {"origin": "blekko", "snapshot": SNAPSHOT, "kind": "direct"}
            })

# -------------------------------------------------
# Builtins: list[str] OR dict[str, str|dict]
# -------------------------------------------------
if isinstance(builtins, list):
    iterable = [(s, {}) for s in builtins if isinstance(s, str)]
elif isinstance(builtins, dict):
    iterable = list(builtins.items())
else:
    iterable = []

for slash, meta in iterable:
    if not isinstance(slash, str) or not slash.strip():
        continue
    s = "/" + slash.strip().lstrip("/")
    desc = ""
    if isinstance(meta, str):
        desc = meta.strip()
    elif isinstance(meta, dict):
        desc = meta.get("description", "").strip()
    topics.append({
        "name": s.lstrip("/"),
        "slash": s,
        "category": "builtin",
        "description": desc,
        "source": {"origin": "blekko", "snapshot": SNAPSHOT, "kind": "direct"}
    })

# Dedup + sort
by_slash = {}
for t in topics:
    by_slash[t["slash"]] = t
topics = sorted(by_slash.values(), key=lambda x: x["slash"])

# Guardrail: we expect ~464 topical + 45 builtins = ~509 total
nonbuiltin = sum(1 for t in topics if t["category"] != "builtin")
total = len(topics)
if nonbuiltin < 400:
    raise SystemExit(
        f"Refusing to write: too few category topics. nonbuiltin={nonbuiltin}, total={total}. "
        f"Seed categories keys={len(categories) if isinstance(categories, dict) else 'n/a'}."
    )

PACK.mkdir(parents=True, exist_ok=True)
TOPICS_OUT.write_text(json.dumps(topics, indent=2) + "\n", encoding="utf-8")

def h(p: Path) -> str:
    return "hash://blake3/" + blake3(p.read_bytes()).hexdigest()

manifest = {}
if MANIFEST.exists():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

manifest.setdefault("schema", "slash-topics.manifest.v0")
manifest["pack"] = "slash-topics/core@0.1.0"
manifest.setdefault("canonicalization", {
    "format": "json",
    "ordering": "lexicographic",
    "encoding": "utf-8",
    "hash": "blake3"
})
manifest["artifacts"] = {
    "topics.json": {"count": total, "blake3": h(TOPICS_OUT)},
    "pack.json": {"blake3": h(PACK_JSON)} if PACK_JSON.exists() else {"missing": True}
}
MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

print(f"Promoted total={total} (categories={nonbuiltin}, builtins={total-nonbuiltin}) into core@0.1.0")

from pathlib import Path
import json
from blake3 import blake3

ROOT = Path(__file__).resolve().parents[1]

SEED = ROOT / "data/blekko/blekko_slashtags_2012-10-15.json"
PACK = ROOT / "protocols/slash-topics/derived@0.1.0"
TOPICS_OUT = PACK / "topics.json"
MANIFEST = PACK / "manifest.json"

raw = json.loads(SEED.read_text(encoding="utf-8"))
SNAPSHOT = raw.get("snapshot", "2012-10-15")

topics = []

# Categories become derived lenses, not canonical slashes
for category, entries in raw.get("categories", {}).items():
    topics.append({
        "name": category,
        "slash": f"/category/{category}",
        "category": "derived",
        "description": f"Derived category lens from blekko ({category})",
        "derived": True,
        "source": {
            "origin": "blekko",
            "snapshot": SNAPSHOT,
            "kind": "inferred"
        }
    })

topics = sorted({t["slash"]: t for t in topics}.values(), key=lambda x: x["slash"])

TOPICS_OUT.write_text(json.dumps(topics, indent=2) + "\n", encoding="utf-8")

def h(p: Path):
    return "hash://blake3/" + blake3(p.read_bytes()).hexdigest()

manifest = {
    "schema": "slash-topics.manifest.v0",
    "pack": "slash-topics/derived@0.1.0",
    "artifacts": {
        "topics.json": {
            "count": len(topics),
            "blake3": h(TOPICS_OUT)
        },
        "pack.json": {
            "blake3": h(PACK / "pack.json")
        }
    },
    "canonicalization": {
        "format": "json",
        "ordering": "lexicographic",
        "encoding": "utf-8",
        "hash": "blake3"
    }
}

MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

print(f"Derived {len(topics)} category lenses into derived@0.1.0")

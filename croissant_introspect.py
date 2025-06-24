"""Introspect Open Targets Croissant manifests and print schema relations."""

import json
import sys
import urllib.request
from typing import Dict, Any, List, Tuple
from collections import defaultdict

OT_BASE_URL = "https://platform.opentargets.org/downloads"

SAMPLE_MANIFEST = {
    "@context": "https://schema.org/",
    "@type": "Dataset",
    "name": "sample_evidence",
    "schema": {
        "fields": [
            {
                "name": "evidence_id",
                "datatype": "string",
                "isKey": True
            },
            {
                "name": "target_id",
                "datatype": "string",
                "references": {
                    "foreignKey": {"dataset": "target", "column": "id"}
                }
            },
            {
                "name": "disease_id",
                "datatype": "string",
                "references": {
                    "foreignKey": {"dataset": "disease", "column": "id"}
                }
            }
        ]
    },
    "distribution": [
        {
            "contentUrl": "https://platform.opentargets.org/downloads/sample_evidence.parquet",
            "encodingFormat": "application/x-parquet",
            "compression": "snappy",
            "sha256": "deadbeef",
            "byteSize": 1234
        }
    ]
}

def manifest_url(dataset: str) -> str:
    return f"{OT_BASE_URL}/{dataset}.croissant.json"

def fetch_manifest(dataset: str) -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(manifest_url(dataset), timeout=10) as resp:
            return json.load(resp)
    except Exception as exc:  # network‑free fallback
        print(f"[WARN] {exc}. Using embedded stub for '{dataset}'.")
        return SAMPLE_MANIFEST.copy()

def parse_structure(manifest: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str], List[Tuple[str, str, str]]]:
    cols = manifest["schema"]["fields"]
    pks = [c["name"] for c in cols if c.get("isKey")]
    fks = []
    for c in cols:
        fk = c.get("references", {}).get("foreignKey")
        if fk:
            fks.append((c["name"], fk["dataset"], fk["column"]))
    return cols, pks, fks

def build_graph(manifests):
    graph = defaultdict(list)
    for ds, mani in manifests.items():
        _, _, edges = parse_structure(mani)
        graph[ds].extend(edges)
    return graph

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        sys.exit("Usage: python croissant_introspect.py <dataset1> [dataset2 ...]")

    manifests = {ds: fetch_manifest(ds) for ds in argv}

    for ds, mani in manifests.items():
        cols, pks, fks = parse_structure(mani)
        print(f"Dataset '{ds}': {len(cols)} columns | PKs={pks or '-'} | FK edges={len(fks)}")
        for src_col, tgt_ds, tgt_col in fks:
            print(f"   FK {ds}.{src_col} -> {tgt_ds}.{tgt_col}")
        print()

    print("# Dependency graph")
    graph = build_graph(manifests)
    for src, edges in graph.items():
        for src_col, tgt_ds, tgt_col in edges:
            print(f"{src}.{src_col} -> {tgt_ds}.{tgt_col}")

if __name__ == "__main__":
    main()

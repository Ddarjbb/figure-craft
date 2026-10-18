"""Read-only keyword search of local SVG metadata and paper-figure crops.

Reference discovery deliberately ignores licensing convenience and vector purity.
Results are candidates to inspect, not a visual-similarity or permission verdict.
No third-party dependencies. Paths may be supplied explicitly or discovered locally.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import re
import sys

SKILL_ROOT = Path(__file__).resolve().parent.parent

ALIASES = {
    "编码器": ("encoder",), "解码器": ("decoder",),
    "自编码器": ("autoencoder", "vae"),
    "多层感知机": ("mlp", "perceptron"), "mlp": ("perceptron",),
    "全连接": ("fully connected", "mlp"),
    "卷积": ("convolution", "cnn"), "特征图": ("feature map",),
    "向量": ("vector",), "矩阵": ("matrix",), "张量": ("tensor",),
    "嵌入": ("embedding",), "令牌": ("token",),
    "跳跃连接": ("skip connection", "residual"),
    "残差": ("residual", "resnet"), "u-net": ("unet",), "unet": ("u-net",),
    "共享": ("shared", "sharing"), "双塔": ("dual", "siamese"),
    "分支": ("branch",), "汇合": ("fusion", "merge"),
    "注意力": ("attention",), "扩散": ("diffusion",),
    "投影": ("projection",), "压缩": ("compression",),
    "多尺度": ("multiscale", "multi-scale"),
    "训练": ("training",), "阶段": ("stage",), "局部": ("detail", "module"),
}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def truthy(value):
    return str(value).lower() in ("true", "1", "yes")


def discover(explicit, env_key, relative, fallback, kind):
    """Explicit inputs are authoritative; missing defaults are optional."""
    configured = explicit or os.environ.get(env_key)
    bundled = [SKILL_ROOT / "assets/svg-library"] if kind == "svg" else []
    guesses = [Path(configured).expanduser()] if configured else [
        *bundled,
        *(parent / relative for parent in (Path.cwd(), *Path.cwd().parents)),
    ]
    if not configured:
        try:
            guesses.append(Path.home() / fallback)
        except RuntimeError:
            pass  # The bundled library also works in environments without a home directory.
    for guess in guesses:
        if kind == "svg":
            candidate = guess if guess.name.lower() == "manifest.csv" else guess / "manifest.csv"
            if candidate.is_file():
                return candidate.resolve()
        else:
            candidate = guess / "agent_batches" if (guess / "agent_batches").is_dir() else guess
            if candidate.is_dir() and any(candidate.glob("agent_*/results.csv")):
                return candidate.resolve()
    if configured:
        raise ValueError(f"Invalid {kind} library: {configured}")
    return None


def svg_candidates(manifest):
    for row in read_csv(manifest):
        if not row.get("file"):
            continue
        path = (manifest.parent / row["file"]).resolve()
        if path.suffix.lower() != ".svg" or not path.is_file():
            continue
        yield {
            "kind": "svg", "path": str(path), "title": row.get("title") or row.get("name", ""),
            "category": row.get("category", ""), "description": row.get("description", ""),
            "source": row.get("source", ""), "source_url": row.get("page_url") or row.get("source_url", ""),
            "author": row.get("author", ""), "license": row.get("license") or "unknown",
            "license_url": row.get("license_url", ""), "tier": row.get("tier", ""),
            "has_raster": truthy(row.get("has_raster")),
            "flags": {key: row[key] for key in (
                "xml_ok", "has_script", "has_js_uri", "has_event", "has_external_ref"
            ) if key in row},
        }


def benchmark_candidates(root):
    seen = set()
    for manifest in sorted(root.glob("agent_*/results.csv")):
        for row in read_csv(manifest):
            raw_path = row.get("image_path", "").strip()
            if not raw_path:
                continue
            # Normalize the Windows separators also when inspecting a copied library on Unix.
            path = Path(raw_path.replace("\\", "/"))
            if not path.is_absolute():
                path = manifest.parent / path
            path = path.resolve()
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            yield {
                "kind": "benchmark", "path": str(path), "title": row.get("title", ""),
                "paper_id": row.get("paper_id", ""), "category": row.get("category", ""),
                "caption": row.get("caption", ""), "figure": row.get("figure_label", ""),
                "page": row.get("page", ""), "batch": manifest.parent.name,
                "source_url": row.get("source_pdf_url", ""),
                "license": "unknown; inspect source before asset reuse", "tier": "",
                "has_raster": True, "status": row.get("status", ""),
            }


def query_terms(query):
    terms = {token: 1.0 for token in re.split(r"[\s,;/|]+", query.casefold()) if token}
    for key, aliases in ALIASES.items():
        if key in query.casefold():
            for alias in aliases:
                terms.setdefault(alias, 0.6)
    return terms


def rank(candidate, terms):
    # Search metadata, never directory names or licence fields, to avoid accidental hits.
    fields = ((candidate["title"], 8), (Path(candidate["path"]).stem, 7),
              (candidate.get("paper_id", ""), 5), (candidate["category"], 3),
              (candidate.get("description", ""), 2), (candidate.get("caption", ""), 2))
    score, matched = 0.0, []
    for term, weight in terms.items():
        # ASCII terms use boundaries, so `mlp` is not a substring of an unrelated word.
        pattern = (r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
                   if term.isascii() else re.escape(term))
        best = max((value for text, value in fields
                    if re.search(pattern, text.casefold())), default=0)
        if best:
            score += weight * best
            matched.append(term)
    return dict(candidate, score=round(score, 2), matched=matched)


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("terms", nargs="+", help="Object/relationship keywords, Chinese or English")
    parser.add_argument("--library", help="SVG library directory or manifest.csv")
    parser.add_argument("--benchmark", help="Benchmark root or agent_batches directory")
    parser.add_argument("--kind", choices=("all", "svg", "benchmark"), default="all")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--vector-only", action="store_true", help="Opt-in asset filter; excludes paper PNGs")
    parser.add_argument("--tier", action="append", help="Exact asset tier filter; does not establish permission")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    try:
        svg = discover(args.library, "FIGURECRAFT_SVG_LIBRARY", Path("svg-library"),
                       Path("Documents/deepseek-harness/default-workspace/svg-library"), "svg"
                       ) if args.kind != "benchmark" else None
        benchmark = discover(args.benchmark, "FIGURECRAFT_BENCHMARK",
                             Path("cvpr2026_figure_benchmark/agent_batches"),
                             Path("Documents/ChatGPT/DDPM/cvpr2026_figure_benchmark/agent_batches"), "benchmark"
                             ) if args.kind != "svg" else None
        if not svg and not benchmark:
            raise ValueError("No local libraries found. Supply --library and/or --benchmark.")
        candidates = list(svg_candidates(svg)) if svg else []
        if benchmark:
            candidates.extend(benchmark_candidates(benchmark))
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"{error}\n")
    if args.vector_only:
        candidates = [c for c in candidates if not c["has_raster"]]
    if args.tier:
        allowed = {tier.casefold() for tier in args.tier}
        candidates = [c for c in candidates if c["tier"].casefold() in allowed]
    terms = query_terms(" ".join(args.terms))
    ranked = [hit for c in candidates if (hit := rank(c, terms))["score"] > 0]
    ranked.sort(key=lambda c: (-c["score"], c["path"]))
    result = {
        "query": " ".join(args.terms), "ranking": "metadata keywords; no license or raster preference",
        "libraries": {"svg": str(svg) if svg else None, "benchmark": str(benchmark) if benchmark else None},
        "candidate_count": len(candidates), "match_count": len(ranked), "hits": ranked[:args.limit],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Matches: {len(ranked)}; inspected metadata for {len(candidates)} available assets.")
        for i, hit in enumerate(result["hits"], 1):
            print(f"\n{i}. [{hit['kind']}] {hit['title']} (score {hit['score']})\n   {hit['path']}")
            print(f"   matched={', '.join(hit['matched'])}; license={hit['license']}; raster={hit['has_raster']}")
            if hit["kind"] == "benchmark":
                print(f"   {hit['batch']}; {hit['figure']}; page {hit['page']}; status={hit['status']}")
            print(f"   source={hit['source_url']}")
        print("\nNext: view candidate images, inspect relevant SVG structure, and record the design decision.")
        if not ranked:
            print("No matches: try object/relationship synonyms or continue with an independently designed layout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

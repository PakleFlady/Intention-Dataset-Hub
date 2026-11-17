"""Create a local-only player for an exact official TSV record; never copy media."""

import argparse
import csv
import html
import re
from pathlib import Path


def make_preview(video_root: Path, annotations: Path, sample_id: str) -> str:
    if not re.fullmatch(r"S\d+_E\d+_\d+", sample_id):
        raise ValueError("Expected a sample ID such as S06_E04_70")
    with annotations.open(encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row.get("id", "").strip() == sample_id]
    if len(rows) != 1 or not rows[0].get("text") or not rows[0].get("label", "").strip():
        raise ValueError("The TSV must contain exactly one complete matching record")
    video = video_root.resolve() / f"MIntRec_{sample_id}.mp4"
    if not video.is_file():
        raise ValueError(f"No matching video: {video}")
    row = rows[0]
    return f'''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><title>MIntRec 本地输入输出</title>
<style>body{{font:18px system-ui;max-width:900px;margin:40px auto;padding:20px;background:#f4f6fa;color:#17253b}}video{{width:100%;max-height:520px;background:#000}}section{{background:white;padding:24px;border-radius:12px}}code{{background:#e9eef7;padding:4px}}</style>
<h1>MIntRec · 本地真实样例</h1><section>
<p>样例编号：<code>{sample_id}</code></p>
<video controls preload="metadata" src="{html.escape(video.as_uri(), quote=True)}"></video>
<h2>输入：视频、音轨与文字</h2><p>{html.escape(row['text'])}</p>
<h2>输出：官方意图标签</h2><p><code>{html.escape(row['label'].strip())}</code></p>
<p>从你提供的官方 TSV 精确匹配；仅规范化标签前后空白。标签来自观察者标注。</p>
<p>本页面只读取本地文件，不上传视频。请勿把生成的页面或素材目录提交到仓库。</p>
</section></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--sample-id", default="S06_E04_70")
    args = parser.parse_args()
    content = make_preview(args.video_root, args.annotations, args.sample_id)
    output = Path(__file__).resolve().parents[1] / "local-data/mintrec-example.html"
    output.parent.mkdir(exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

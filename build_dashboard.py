#!/usr/bin/env python3
"""Regenerate index.html from the reports in reports/.

Run after adding a report. Reads each reports/YYYY-MM-DD-<slug>.md, pulls its
frontmatter plus a few rows the SKILL.md template guarantees, and writes a
single self-contained dashboard file.
"""

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"

# Palette values come from the dataviz skill's reference instance.
PALETTE = {
    "surface": "#fcfcfb", "plane": "#f9f9f7", "primary": "#0b0b0b",
    "secondary": "#52514e", "muted": "#898781", "grid": "#e1e0d9",
    "rule": "#c3c2b7", "accent": "#2a78d6", "border": "rgba(11,11,11,0.10)",
    "d_surface": "#1a1a19", "d_plane": "#0d0d0d", "d_primary": "#ffffff",
    "d_secondary": "#c3c2b7", "d_muted": "#898781", "d_grid": "#2c2c2a",
    "d_rule": "#383835", "d_accent": "#3987e5", "d_border": "rgba(255,255,255,0.10)",
}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[end + 4:]


def table_row(body, label):
    """Pull the value cell out of a `| **label** | value |` row."""
    m = re.search(r"^\|\s*\*{0,2}" + re.escape(label) + r"\*{0,2}\s*\|(.+?)\|\s*$",
                  body, re.MULTILINE)
    return m.group(1).strip() if m else ""


def north_star(body):
    """The metric itself, out of section 3.

    Reports state it three ways: a `- **North Star…**` bullet with the metric
    inside the bold, the same bullet with it after the colon, or a bare
    paragraph when the report says the company never published one.
    """
    sec = re.search(r"^##\s*3\..*?北极星.*?$(.*?)(?=^##\s)", body, re.MULTILINE | re.DOTALL)
    if not sec:
        return ""
    chunk = sec.group(1)
    line = ""
    for pattern in (r"^-\s*(\*\*North Star.+)$", r"^-\s*(.+)$", r"^(?!#)(\S.+)$"):
        m = re.search(pattern, chunk, re.MULTILINE)
        if m:
            line = m.group(1)
            break
    if not line:
        return ""
    line = re.sub(r"\*\*|`", "", line)
    line = re.sub(r"^\s*North Star[^：:]*[：:]\s*", "", line)
    line = line.lstrip("：: 。")
    sentences = [s for s in line.split("。") if s.strip()]
    if not sentences:
        return ""
    out = sentences[0]
    if len(out) < 14 and len(sentences) > 1:
        out += "。" + sentences[1]
    return (out[:150] + "…") if len(out) > 150 else out + "。"


# --- the business-model diagram ---------------------------------------------

def parse_model(body):
    m = re.search(r"```model\s*\n(.*?)\n```", body, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def text_px(s, size):
    """CJK glyphs are about one em wide; latin ones roughly half that."""
    return sum(size if ord(c) > 0x2E80 else size * 0.55 for c in s)


def _units(s):
    """CJK breaks anywhere; a run of latin/digits/punctuation stays together."""
    return re.findall(r"[A-Za-z0-9$%./,+\-–—]+|.", s)


def wrap_px(s, max_px, size, max_lines=2):
    lines, cur = [], ""
    for ch in _units(s):
        if text_px(cur + ch, size) > max_px and cur:
            lines.append(cur)
            cur = ch
            if len(lines) == max_lines:
                break
        else:
            cur += ch
    if len(lines) < max_lines and cur:
        lines.append(cur)
    if len(lines) == max_lines and text_px(s, size) > max_px * max_lines:
        lines[-1] = lines[-1][:-1] + "…"
    return lines


def esc(s):
    return html.escape(str(s), quote=True)


def _node_lines(node, w):
    return (wrap_px(node.get("label", ""), w - 20, 14, 2),
            wrap_px(node.get("sub", ""), w - 20, 11, 2) if node.get("sub") else [])


def _node_height(label_lines, sub_lines):
    return 20 + 19 * len(label_lines) + 14 * len(sub_lines) + 10


def _node(x, y, w, h, node, role="", subject=False):
    label_lines, subs = _node_lines(node, w)
    cx = x + w / 2
    top = y + (h - _node_height(label_lines, subs)) / 2
    stroke = "var(--accent)" if subject else "var(--rule)"
    out = []
    if role:
        out.append(f'<text x="{cx}" y="{y - 9}" text-anchor="middle" font-size="11" '
                   f'font-weight="600" fill="var(--muted)">{esc(role)}</text>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
               f'fill="var(--surface)" stroke="{stroke}" stroke-width="{2 if subject else 1}"/>')
    for i, line in enumerate(label_lines):
        out.append(f'<text x="{cx}" y="{top + 24 + i * 19}" text-anchor="middle" '
                   f'font-size="14" font-weight="600" fill="var(--primary)">{esc(line)}</text>')
    base = top + 24 + 19 * (len(label_lines) - 1)
    for i, line in enumerate(subs):
        out.append(f'<text x="{cx}" y="{base + 19 + i * 14}" text-anchor="middle" '
                   f'font-size="11" fill="var(--muted)">{esc(line)}</text>')
    return "".join(out)


def _arrow(x1, x2, y, label, money=True):
    """Solid accent = money moving. Dashed grey = something given away free."""
    mid = (x1 + x2) / 2
    tag = "付费" if money else "免费"
    lines = wrap_px(f"{tag} · {label}" if label else tag, x2 - x1 - 8, 11.5, 2)
    stroke = "var(--accent)" if money else "var(--muted)"
    dash = "" if money else ' stroke-dasharray="6 4"'
    out = [f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{stroke}" '
           f'stroke-width="2"{dash} marker-end="url(#{"ah" if money else "ahg"})"/>']
    for i, line in enumerate(lines):
        dy = y - 12 - (len(lines) - 1 - i) * 14
        out.append(f'<text x="{mid}" y="{dy}" text-anchor="middle" font-size="11.5" '
                   f'fill="var(--secondary)">{esc(line)}</text>')
    return "".join(out)


def render_model_svg(m):
    """Money flows left to right: who pays -> the company -> where it goes."""
    if not m or not m.get("vendor"):
        return ""
    W, TOP = 900, 62
    three = bool(m.get("payee"))
    outflow_is_money = m.get("outflow_kind", "money") != "free"
    box_w = 180 if three else 240
    xs = [0, 360, 720] if three else [90, 570]

    nodes = [m["payer"], m["vendor"]] + ([m["payee"]] if three else [])
    BOX_H = max(_node_height(*_node_lines(n, box_w)) for n in nodes)

    parts = [_node(xs[0], TOP, box_w, BOX_H, m["payer"], "谁掏钱"),
             _node(xs[1], TOP, box_w, BOX_H, m["vendor"], "这家公司", subject=True)]
    parts.append(_arrow(xs[0] + box_w, xs[1], TOP + BOX_H / 2, m.get("flow", "")))
    if three:
        role = "钱再流向谁" if outflow_is_money else "谁在用，但不掏钱"
        parts.append(_node(xs[2], TOP, box_w, BOX_H, m["payee"], role))
        parts.append(_arrow(xs[1] + box_w, xs[2], TOP + BOX_H / 2,
                            m.get("outflow", ""), money=outflow_is_money))

    y = TOP + BOX_H
    if m.get("budget"):
        parts.append(f'<text x="{xs[0] + box_w / 2}" y="{y + 19}" text-anchor="middle" '
                     f'font-size="11" fill="var(--muted)">这笔钱出自 · {esc(m["budget"])}</text>')
        y += 22

    metrics = m.get("metrics", [])[:4]
    if metrics:
        y += 30
        parts.append(f'<line x1="0" y1="{y - 20}" x2="{W}" y2="{y - 20}" '
                     f'stroke="var(--grid)" stroke-width="1"/>')
        step = W / len(metrics)
        for i, met in enumerate(metrics):
            cx = step * i + step / 2
            parts.append(f'<text x="{cx}" y="{y + 2}" text-anchor="middle" font-size="11" '
                         f'fill="var(--muted)">{esc(met.get("k", ""))}</text>')
            parts.append(f'<text x="{cx}" y="{y + 24}" text-anchor="middle" font-size="17" '
                         f'font-weight="600" fill="var(--primary)">{esc(met.get("v", ""))}</text>')
        y += 34

    legend = "箭头方向就是钱的方向"
    if three and not outflow_is_money:
        legend = "蓝色实线＝钱的流向；灰色虚线＝免费提供，不收钱"
    return (f'<svg class="flow" viewBox="0 0 {W} {y + 8}" role="img" '
            f'aria-label="商业模式资金流向图">'
            f'<defs>'
            f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="var(--accent)"/></marker>'
            f'<marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="var(--muted)"/></marker>'
            f'</defs>'
            f'<text x="0" y="15" font-size="12" font-weight="600" fill="var(--secondary)">'
            f'钱从哪儿来，又流到哪儿去</text>'
            f'<text x="{W}" y="15" text-anchor="end" font-size="11" fill="var(--muted)">'
            f'{esc(legend)}</text>'
            + "".join(parts) + "</svg>")


# --- a small markdown renderer, scoped to the shapes our template produces ---

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def render_markdown(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced blocks are data (the ```model payload), not prose — the
        # diagram renders them instead.
        if stripped.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue

        if stripped.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in block]
            # Drop the |---|---| separator row.
            body_rows = [r for r in cells[1:] if not all(set(c) <= set("-: ") for c in r)]
            out.append("<table><thead><tr>"
                       + "".join(f"<th>{inline(c)}</th>" for c in cells[0])
                       + "</tr></thead><tbody>")
            for r in body_rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            out.append(f"<h{min(level + 1, 6)}>{inline(stripped.lstrip('# ').strip())}"
                       f"</h{min(level + 1, 6)}>")
            i += 1
            continue

        if stripped in ("---", "***"):
            out.append("<hr>")
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>")
            while i < len(lines) and (re.match(r"^[-*]\s+", lines[i].strip())
                                      or re.match(r"^\d+\.\s+", lines[i].strip())):
                item = re.sub(r"^([-*]|\d+\.)\s+", "", lines[i].strip())
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append(f"</{tag}>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip()[0] in "|#-*":
            para.append(lines[i].strip())
            i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
        else:
            out.append(f"<p>{inline(stripped)}</p>")
            i += 1
    return "\n".join(out)


def load_reports():
    items = []
    for path in sorted(REPORTS.glob("2*.md"), reverse=True):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta.get("company"):
            continue
        items.append({
            "company": meta.get("company", path.stem),
            "sector": meta.get("sector", "未分类"),
            "date": meta.get("date", path.stem[:10]),
            "tier": meta.get("growth_tier", ""),
            "arr": meta.get("arr", "未公开"),
            "valuation": meta.get("valuation", "未公开"),
            "growth": table_row(body, "增长倍数") or "见报告",
            "per_head": table_row(body, "人均创收"),
            "north_star": north_star(body),
            "flow": render_model_svg(parse_model(body)),
            "html": render_markdown(body),
        })
    return items


def build(items):
    sectors = {}
    for it in items:
        sectors.setdefault(it["sector"].split("（")[0].split("(")[0].strip(), []).append(it["company"])

    updated = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

    tiles = [("已分析公司", str(len(items))), ("覆盖赛道", str(len(sectors))),
             ("最近更新", items[0]["date"] if items else "—")]

    cards = []
    for n, it in enumerate(items):
        cards.append(f"""
    <article class="card">
      <button class="card-head" aria-expanded="false" data-target="r{n}">
        <span class="card-title">
          <span class="name">{html.escape(it['company'])}</span>
          <span class="sector">{html.escape(it['sector'])}</span>
        </span>
        <span class="date">{html.escape(it['date'])}</span>
      </button>
      {f'<div class="flow-wrap">{it["flow"]}</div>' if it["flow"] else ""}
      <dl class="facts">
        <div><dt>ARR</dt><dd>{inline(it['arr'])}</dd></div>
        <div><dt>增长倍数</dt><dd>{inline(it['growth'])}</dd></div>
        <div><dt>估值</dt><dd>{inline(it['valuation'])}</dd></div>
        {f"<div><dt>人均创收</dt><dd>{inline(it['per_head'])}</dd></div>" if it['per_head'] else ""}
        {f"<div class='wide'><dt>北极星指标</dt><dd>{inline(it['north_star'])}</dd></div>" if it['north_star'] else ""}
      </dl>
      <div class="report" id="r{n}" hidden>{it['html']}</div>
    </article>""")

    p = PALETTE
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 创业公司研究看板</title>
<style>
:root {{
  color-scheme: light;
  --surface:{p['surface']}; --plane:{p['plane']}; --primary:{p['primary']};
  --secondary:{p['secondary']}; --muted:{p['muted']}; --grid:{p['grid']};
  --rule:{p['rule']}; --accent:{p['accent']}; --border:{p['border']};
}}
@media (prefers-color-scheme: dark) {{
  :root:where(:not([data-theme="light"])) {{
    color-scheme: dark;
    --surface:{p['d_surface']}; --plane:{p['d_plane']}; --primary:{p['d_primary']};
    --secondary:{p['d_secondary']}; --muted:{p['d_muted']}; --grid:{p['d_grid']};
    --rule:{p['d_rule']}; --accent:{p['d_accent']}; --border:{p['d_border']};
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --surface:{p['d_surface']}; --plane:{p['d_plane']}; --primary:{p['d_primary']};
  --secondary:{p['d_secondary']}; --muted:{p['d_muted']}; --grid:{p['d_grid']};
  --rule:{p['d_rule']}; --accent:{p['d_accent']}; --border:{p['d_border']};
}}
* {{ box-sizing: border-box; }}
body {{
  margin:0; padding:32px 20px 80px; background:var(--plane); color:var(--primary);
  font:15px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif;
}}
.wrap {{ max-width: 960px; margin: 0 auto; }}
header h1 {{ font-size:26px; margin:0 0 6px; letter-spacing:-.01em; }}
header p {{ margin:0; color:var(--secondary); font-size:14px; }}
.tiles {{ display:flex; gap:12px; flex-wrap:wrap; margin:24px 0 8px; }}
.tile {{
  flex:1 1 150px; background:var(--surface); border:1px solid var(--border);
  border-radius:10px; padding:14px 16px;
}}
.tile .k {{ font-size:12px; color:var(--muted); letter-spacing:.02em; }}
.tile .v {{ font-size:28px; font-weight:600; margin-top:2px; }}
.sectors {{ display:flex; flex-wrap:wrap; gap:8px; margin:20px 0 28px; }}
.chip {{
  font-size:12px; color:var(--secondary); background:var(--surface);
  border:1px solid var(--border); border-radius:999px; padding:4px 11px;
}}
.card {{
  background:var(--surface); border:1px solid var(--border); border-radius:12px;
  margin-bottom:14px; overflow:hidden;
}}
.card-head {{
  width:100%; display:flex; justify-content:space-between; align-items:baseline;
  gap:14px; padding:16px 18px; background:none; border:0; cursor:pointer;
  text-align:left; color:inherit; font:inherit;
}}
.card-head:hover {{ background:color-mix(in srgb, var(--accent) 6%, transparent); }}
.card-title {{ display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; }}
.name {{ font-size:18px; font-weight:600; }}
.name::after {{ content:"▸"; color:var(--muted); font-size:12px; margin-left:8px; }}
.card-head[aria-expanded="true"] .name::after {{ content:"▾"; }}
.sector {{ font-size:12px; color:var(--secondary); }}
.date {{ font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; white-space:nowrap; }}
.flow-wrap {{ padding:2px 18px 6px; }}
svg.flow {{ width:100%; height:auto; display:block; overflow:visible; }}
.facts {{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
  gap:2px; margin:0; padding:0 18px 16px; background:transparent;
}}
.facts > div {{ padding:8px 0; border-top:1px solid var(--grid); }}
.facts .wide {{ grid-column:1/-1; }}
.facts dt {{ font-size:11px; color:var(--muted); letter-spacing:.03em; }}
.facts dd {{ margin:2px 0 0; font-size:13px; color:var(--secondary); }}
.report {{ padding:4px 18px 24px; border-top:1px solid var(--grid); }}
.report h2 {{ font-size:18px; margin:26px 0 8px; }}
.report h3 {{ font-size:15px; margin:20px 0 6px; }}
.report p {{ margin:8px 0; }}
.report table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; }}
.report th, .report td {{
  border-bottom:1px solid var(--grid); padding:7px 9px; text-align:left; vertical-align:top;
}}
.report th {{ color:var(--muted); font-weight:500; font-size:12px; }}
.report td:first-child {{ white-space:nowrap; }}
.report ul, .report ol {{ padding-left:20px; margin:8px 0; }}
.report li {{ margin:4px 0; }}
.report code {{
  background:color-mix(in srgb, var(--primary) 7%, transparent);
  padding:1px 5px; border-radius:4px; font-size:12px;
}}
.report hr {{ border:0; border-top:1px solid var(--grid); margin:22px 0; }}
.report a {{ color:var(--accent); }}
footer {{ margin-top:36px; color:var(--muted); font-size:12px; }}
.toggle {{
  position:fixed; top:16px; right:16px; background:var(--surface); color:var(--secondary);
  border:1px solid var(--border); border-radius:8px; padding:6px 11px;
  font:12px system-ui,sans-serif; cursor:pointer;
}}
</style></head><body>
<button class="toggle" id="t">明/暗</button>
<div class="wrap">
<header>
  <h1>AI 创业公司研究看板</h1>
  <p>按「增长速度 &gt; 规模」挑选，一天一家，绝不重复。点公司名展开全文。</p>
</header>

<div class="tiles">
{"".join(f'<div class="tile"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in tiles)}
</div>

<div class="sectors">
{"".join(f'<span class="chip">{html.escape(s)} · {html.escape("、".join(c))}</span>' for s, c in sectors.items())}
</div>

{"".join(cards)}

<footer>
  生成于 {updated}。数据口径不统一（GMV 与 ARR 混杂、部分为估算），因此刻意不做跨公司柱状图对比 —— 每家的口径以卡片内报告为准。
</footer>
</div>
<script>
document.querySelectorAll('.card-head').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var panel = document.getElementById(b.dataset.target);
    var open = b.getAttribute('aria-expanded') === 'true';
    b.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
  }});
}});
document.getElementById('t').addEventListener('click', function () {{
  var dark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
}});
</script>
</body></html>
"""


if __name__ == "__main__":
    reports = load_reports()
    (ROOT / "index.html").write_text(build(reports), encoding="utf-8")
    print(f"index.html regenerated — {len(reports)} reports")

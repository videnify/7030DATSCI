"""Generate Appendix Figure A7: causal DAG used for the pooled DoWhy estimate.

Nodes and edges are taken verbatim from Table 4 (Structural causal model edges
in the primary DoWhy estimate) and from the frozen DoWhy graph specification in
notebooks/04_causal_analysis.ipynb (cell id "dowhy-model"). No mediators, nodes
or edges are added beyond what is in the frozen model.

Output: reports/figures/A7_causal_dag.svg and reports/figures/A7_causal_dag.png
(rasterised via rsvg-convert at 3x scale for dissertation embedding).

Visual style matches docs/architecture/research_governance.svg (same box fill,
stroke colour, arrowhead marker, font) so the two appendix diagrams read as one
family.
"""
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_SVG = REPO_ROOT / "reports" / "figures" / "A7_causal_dag.svg"
OUT_PNG = REPO_ROOT / "reports" / "figures" / "A7_causal_dag.png"

BOX_FILL = "#F3F7FC"
BOX_STROKE = "#5B8FC7"
TEXT_DARK = "#1E1E1E"
TEXT_GREY = "#4F4F4F"
TEXT_FOOT = "#969696"

WIDTH, HEIGHT = 720, 460
BOX_W, BOX_H = 200, 60

NODES = {
    "vix": {"x": 40, "y": 60, "label": "VIX regime"},
    "prior": {"x": 40, "y": 340, "label": "Prior-day return"},
    "sentiment": {"x": 270, "y": 200, "label": "Daily sentiment"},
    "outcome": {"x": 500, "y": 200, "label": "Next-day SPY return"},
}

EDGES = [
    ("sentiment", "outcome"),
    ("vix", "outcome"),
    ("vix", "sentiment"),
    ("prior", "outcome"),
    ("prior", "sentiment"),
]


def center(node):
    n = NODES[node]
    return n["x"] + BOX_W / 2, n["y"] + BOX_H / 2


def edge_path(src, dst):
    x1, y1 = center(src)
    x2, y2 = center(dst)
    # shrink the line so it starts/ends at the box edge rather than the centre
    dx, dy = x2 - x1, y2 - y1
    length = (dx**2 + dy**2) ** 0.5
    ux, uy = dx / length, dy / length
    sx1 = NODES[src]["x"] + BOX_W / 2 + ux * (BOX_W / 2 - 4) if abs(ux) > abs(uy) else x1 + ux * (BOX_H / 2)
    # Simpler robust approach: clip to box rectangle boundary along the direction vector
    def clip(node, ux, uy, sign):
        cx, cy = center(node)
        tx = (BOX_W / 2) / abs(ux) if ux != 0 else float("inf")
        ty = (BOX_H / 2) / abs(uy) if uy != 0 else float("inf")
        t = min(tx, ty)
        return cx + sign * ux * t, cy + sign * uy * t

    p1 = clip(src, ux, uy, 1)
    p2 = clip(dst, ux, uy, -1)
    return p1, p2


def build_svg():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Arial, Helvetica, sans-serif">'
    )
    parts.append(
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M1 1L9 5L1 9Z" fill="{BOX_STROKE}"/></marker></defs>'
    )
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#FFFFFF"/>')
    parts.append(
        f'<text x="{WIDTH/2}" y="30" text-anchor="middle" font-size="18" font-weight="700" '
        f'fill="{TEXT_DARK}">Causal DAG for the Pooled DoWhy Estimate</text>'
    )
    parts.append(
        f'<text x="{WIDTH/2}" y="48" text-anchor="middle" font-size="11" fill="{TEXT_FOOT}" '
        f'font-style="italic">Nodes and edges as specified in Table 4 (frozen DoWhy graph)</text>'
    )

    # edges first so boxes sit on top of arrowheads
    for src, dst in EDGES:
        (x1, y1), (x2, y2) = edge_path(src, dst)
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{BOX_STROKE}" stroke-width="1.6" marker-end="url(#arrow)"/>'
        )

    for node in NODES.values():
        cx = node["x"] + BOX_W / 2
        cy = node["y"] + BOX_H / 2
        parts.append(
            f'<rect x="{node["x"]}" y="{node["y"]}" width="{BOX_W}" height="{BOX_H}" rx="9" '
            f'fill="{BOX_FILL}" stroke="{BOX_STROKE}" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="14" font-weight="700" '
            f'fill="{TEXT_DARK}">{node["label"]}</text>'
        )

    parts.append(
        f'<text x="{WIDTH/2}" y="{HEIGHT-16}" text-anchor="middle" font-size="9.5" fill="{TEXT_FOOT}">'
        f'Arrows encode modelling assumptions rather than experimentally proven relationships.</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg = build_svg()
    OUT_SVG.write_text(svg, encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-z", "4", "-o", str(OUT_PNG), str(OUT_SVG)],
        check=True,
    )
    print(f"wrote {OUT_SVG}")
    print(f"wrote {OUT_PNG}")


if __name__ == "__main__":
    main()

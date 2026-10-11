"""Inline SVG pipeline diagrams. Labels use only wording already on the site."""


def _box(x, y, w, h, title, sub, accent=False):
    cls = "dg-box-accent" if accent else "dg-box"
    cx = x + w / 2
    sub_svg = f'<text class="dg-sub" x="{cx:g}" y="{y + h / 2 + 40:g}" text-anchor="middle">{sub}</text>' if sub else ""
    ty = y + h / 2 - (6 if sub else -14)
    return (
        f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="22"/>'
        f'<text class="dg-title" x="{cx:g}" y="{ty:g}" text-anchor="middle">{title}</text>'
        f"{sub_svg}"
    )


def _arrow(x1, y1, x2, y2):
    # Line plus a filled triangular head pointing from (x1, y1) to (x2, y2).
    import math

    ang = math.atan2(y2 - y1, x2 - x1)
    L, W = 22, 13
    bx, by = x2 - L * math.cos(ang), y2 - L * math.sin(ang)
    px, py = -math.sin(ang) * W, math.cos(ang) * W
    pts = f"{x2:.1f},{y2:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}"
    return f'<line class="dg-arrow" x1="{x1}" y1="{y1}" x2="{bx:.1f}" y2="{by:.1f}"/><polygon class="dg-head" points="{pts}"/>'


def claimcheck(prefix):
    tid = f"{prefix}-title"
    body = "".join([
        _box(40, 50, 400, 200, "205 tasks", "verified ground truth", accent=True),
        _box(520, 50, 400, 200, "Agent harness", "GPT-OSS 120B and 20B"),
        _box(520, 290, 400, 200, "Grading", "hardened"),
        _box(40, 290, 400, 200, "LLM-as-a-judge", "different model family"),
        _arrow(446, 150, 514, 150),
        _arrow(720, 256, 720, 284),
        _arrow(514, 390, 446, 390),
    ])
    return (
        f'<svg viewBox="0 0 960 540" role="img" aria-labelledby="{tid}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{tid}">claimcheck pipeline: 205 tasks with verified ground truth go to an agent harness '
        f"running GPT-OSS 120B and 20B, then to hardened grading, then to an LLM-as-a-judge from a different model family.</title>"
        f"{body}</svg>"
    )


def claimcheck_mcp(prefix):
    tid = f"{prefix}-title"
    body = "".join([
        _box(40, 50, 380, 200, "AI agent", ""),
        _box(500, 50, 420, 200, "MCP server", "3 tools: list, read, run", accent=True),
        _box(240, 290, 480, 200, "Docker sandbox", "claimcheck's 205 tasks"),
        _arrow(426, 150, 494, 150),
        _arrow(710, 256, 640, 286),
    ])
    return (
        f'<svg viewBox="0 0 960 540" role="img" aria-labelledby="{tid}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{tid}">claimcheck-mcp: an AI agent uses the MCP server and its 3 tools (list, read, run) '
        f"to work on claimcheck's 205 tasks in a Docker sandbox.</title>"
        f"{body}</svg>"
    )


def _box_lines(x, y, w, h, lines, accent=False):
    """Box with one or more title-style lines, vertically centred."""
    cls = "dg-box-accent" if accent else "dg-box"
    cx = x + w / 2
    step = 48
    first = y + h / 2 + 14 - step * (len(lines) - 1) / 2
    texts = "".join(
        f'<text class="dg-title" x="{cx:g}" y="{first + i * step:g}" text-anchor="middle">{t}</text>'
        for i, t in enumerate(lines)
    )
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="22"/>{texts}'


def ab_framework(prefix):
    tid = f"{prefix}-title"
    body = "".join([
        _box_lines(40, 50, 400, 200, ["SRM checks"], accent=True),
        _box_lines(520, 50, 400, 200, ["z-tests and", "Welch's t-tests"]),
        _box_lines(520, 290, 400, 200, ["Guardrails"]),
        _box_lines(40, 290, 400, 200, ["ship, continue,", "or rollback"]),
        _arrow(446, 150, 514, 150),
        _arrow(720, 256, 720, 284),
        _arrow(514, 390, 446, 390),
    ])
    return (
        f'<svg viewBox="0 0 960 540" role="img" aria-labelledby="{tid}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{tid}">A/B Experimentation and Decision Framework: SRM checks, then z-tests and '
        f"Welch's t-tests, then guardrails that decide ship, continue, or rollback.</title>"
        f"{body}</svg>"
    )

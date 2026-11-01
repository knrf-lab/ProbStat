"""Draw labelled boxplots (SVG) for the worked solutions. Output: svg/<name>.svg"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
os.makedirs(OUT, exist_ok=True)


def boxplot(name, lo, q1, med, q3, hi, outliers, fences, axis, step, unit):
    W, H, L, R = 640, 175, 30, 610
    a0, a1 = axis
    X = lambda v: L + (v - a0) / (a1 - a0) * (R - L)
    y, h = 87, 34
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif" font-size="11">']
    # fences
    for lab, v in zip(("LL", "UL"), fences):
        if a0 <= v <= a1:
            s.append(f'<line x1="{X(v):.1f}" y1="10" x2="{X(v):.1f}" y2="133" stroke="#b3261e" stroke-dasharray="4,3"/>')
            s.append(f'<text x="{X(v):.1f}" y="9" fill="#b3261e" text-anchor="middle">{lab} = {v:g}</text>')
    # whiskers
    s.append(f'<line x1="{X(lo):.1f}" y1="{y}" x2="{X(q1):.1f}" y2="{y}" stroke="#000" stroke-width="1.6"/>')
    s.append(f'<line x1="{X(q3):.1f}" y1="{y}" x2="{X(hi):.1f}" y2="{y}" stroke="#000" stroke-width="1.6"/>')
    for v in (lo, hi):
        s.append(f'<line x1="{X(v):.1f}" y1="{y-10}" x2="{X(v):.1f}" y2="{y+10}" stroke="#000" stroke-width="1.6"/>')
    # box
    s.append(f'<rect x="{X(q1):.1f}" y="{y-h/2}" width="{X(q3)-X(q1):.1f}" height="{h}" fill="#dfe7f3" stroke="#1f3b63" stroke-width="1.8"/>')
    s.append(f'<line x1="{X(med):.1f}" y1="{y-h/2}" x2="{X(med):.1f}" y2="{y+h/2}" stroke="#1f3b63" stroke-width="2.6"/>')
    # labels above, staggered into rows so they never overlap
    labels = [("min", lo), ("Q1", q1), ("Q2", med), ("Q3", q3), ("max*" if outliers else "max", hi)]
    rows_last = []
    for lab, v in labels:
        txt = f"{lab}={v:g}"; w = 7 * len(txt)
        r = 0
        while r < len(rows_last) and X(v) - w / 2 < rows_last[r] + 6:
            r += 1
        if r == len(rows_last):
            rows_last.append(-1e9)
        rows_last[r] = X(v) + w / 2
        yy = y - h / 2 - 5 - 13 * r
        s.append(f'<line x1="{X(v):.1f}" y1="{yy+2}" x2="{X(v):.1f}" y2="{y-h/2}" stroke="#999" stroke-width="0.6"/>')
        s.append(f'<text x="{X(v):.1f}" y="{yy}" text-anchor="middle" font-size="10" fill="#1f3b63">{txt}</text>')
    # outliers
    for v in outliers:
        s.append(f'<text x="{X(v):.1f}" y="{y+5}" text-anchor="middle" font-size="16" fill="#b3261e">*</text>')
        s.append(f'<text x="{X(v):.1f}" y="{y+22}" text-anchor="middle" font-size="10" fill="#b3261e">{v:g}</text>')
    # axis
    s.append(f'<line x1="{L}" y1="143" x2="{R}" y2="143" stroke="#333"/>')
    v = a0
    while v <= a1 + 1e-9:
        s.append(f'<line x1="{X(v):.1f}" y1="143" x2="{X(v):.1f}" y2="148" stroke="#333"/><text x="{X(v):.1f}" y="161" text-anchor="middle" font-size="10">{v:g}</text>')
        v += step
    s.append(f'<text x="{R}" y="173" text-anchor="end" font-size="10">{unit}</text>')
    if outliers:
        s.append(f'<text x="{L}" y="173" font-size="10">* outlier · whisker ends at the last value inside the fences (max*)</text>')
    s.append("</svg>")
    open(os.path.join(OUT, name + ".svg"), "w").write("\n".join(s))


# Real Quiz 1 LA40 Q2 (amplitudo, mV)
boxplot("LA_q2", 22, 24, 26, 29, 29, [65, 67, 75], (16.5, 36.5), (10, 80), 10, "mV")
# Real Quiz 1 LB40 Q1 (suhu, °C)
boxplot("LB_q1", 16, 24, 27, 56, 85, [], (-24, 104), (-30, 110), 10, "°C")
# Practice midterm M2 (latency, ms)
boxplot("M_q2", 11, 13, 15, 17, 18, [48, 52], (7, 23), (5, 55), 5, "ms")
# Slides example: sodium in cheese
boxplot("cheese", 260, 292.5, 325, 340, 340, [520], (221.25, 411.25), (200, 540), 40, "mg")
print("svg ok")

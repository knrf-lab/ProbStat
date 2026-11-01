"""Generate statistical tables (HTML) for the binder: standard normal, cumulative binomial, cumulative Poisson."""
from math import comb, exp, erf, sqrt, factorial

OUT = "/projects/sandbox/probstat-binder/src/70_tables.html"


def phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def binc(x, n, p):
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(x + 1))


def poic(x, lam):
    return sum(exp(-lam) * lam**i / factorial(i) for i in range(x + 1))


def fmt(v):
    # Devore style: 4 decimals without the leading zero; anything that rounds to 1 prints as 1.000
    return "1.000" if round(v, 4) >= 1 else f"{v:.4f}"[1:]


h = []
tab = lambda s: h.append(s)

# ---------- Z TABLE ----------
cols = [i / 100 for i in range(10)]
for sign, title, rows in [
    ("neg", "Standard Normal Table: Φ(z) = P(Z ≤ z), z ≤ 0", [-(i / 10) for i in range(34, -1, -1)]),
    ("pos", "Standard Normal Table: Φ(z) = P(Z ≤ z), z ≥ 0", [i / 10 for i in range(0, 35)]),
]:
    anchor = '<anchor id="T" label="T · Statistical Tables"/>' if sign == "neg" else ""
    tab(f'<section class="table-page">{anchor}<anchor id="T-z{sign}"/><h2 class="sec">{"T.1" if sign=="neg" else "T.2"} {title}</h2>')
    tab('<p class="tnote">Row = z to one decimal, column = second decimal. '
        + ('For negative z: z = −1.36 → row −1.3, column .06.' if sign == "neg" else 'z = 1.36 → row 1.3, column .06 → .9131.')
        + ' Area is to the <b>LEFT</b> of z <span class="id">(luas di kiri z)</span>.</p>')
    tab('<table class="ztab"><thead><tr><th>z</th>' + "".join(f"<th>.0{i}</th>" for i in range(10)) + "</tr></thead><tbody>")
    for r in rows:
        cells = []
        for c in cols:
            z = r - c if sign == "neg" else r + c
            if sign == "neg" and r == 0 and c > 0:
                z = -c
            cells.append(f"<td>{phi(z):.4f}</td>")
        label = f"−{abs(r):.1f}" if sign == "neg" else f"{r:.1f}"
        if sign == "neg" and r == 0:
            label = "−0.0"
        tab(f"<tr><th>{label}</th>{''.join(cells)}</tr>")
    tab("</tbody></table>")
    if sign == "pos":
        tab('<p class="tnote">Handy critical values: z<sub>.10</sub> = 1.28, z<sub>.05</sub> = 1.645, '
            'z<sub>.025</sub> = 1.96, z<sub>.01</sub> = 2.33, z<sub>.005</sub> = 2.58 (area to the RIGHT). '
            'Beyond the table: z ≥ 3.50 → Φ ≈ 1.0000; z ≤ −3.50 → Φ ≈ 0.0000.</p>')
    tab("</section>")

# ---------- BINOMIAL ----------
ps = [0.05, 0.10, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 0.95]
ns_pages = [[5, 6, 7, 8, 9], [10, 12, 15], [20, 25]]
for pi_, ns in enumerate(ns_pages):
    tab(f'<section class="table-page"><anchor id="T-bin{pi_}"/><h2 class="sec">T.3 Cumulative Binomial: B(x; n, p) = P(X ≤ x)'
        + (" (cont.)" if pi_ else "") + "</h2>")
    if pi_ == 0:
        tab('<p class="tnote">P(X = k) = B(k) − B(k−1). P(X ≥ k) = 1 − B(k−1). P(X &gt; k) = 1 − B(k). '
            'Calculator check: <b>Binomial CD</b> gives the same value.</p>')
    for n in ns:
        tab(f'<table class="btab"><thead><tr><th class="nlab">n = {n}<br>x</th>' + "".join(f"<th>{p:.2f}".replace("0.", ".") + "</th>" for p in ps) + "</tr></thead><tbody>")
        for x in range(n + 1):
            tab(f"<tr><th>{x}</th>" + "".join(f"<td>{fmt(binc(x, n, p))}</td>" for p in ps) + "</tr>")
        tab("</tbody></table>")
    tab("</section>")

# ---------- POISSON ----------
groups = [
    ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 8),
    ([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0], 18),
    ([8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 18.0, 20.0], 36),
]
for gi, (lams, xmax) in enumerate(groups):
    if gi != 2:
        if gi == 0:
            tab('<section class="table-page"><anchor id="T-poi"/><h2 class="sec">T.4 Cumulative Poisson: F(x; λ) = P(X ≤ x)</h2>'
                '<p class="tnote">λ = mean number of events in the interval (scale it to the interval asked: λ<sub>new</sub> = rate × length). '
                'P(X = k) = F(k) − F(k−1). Calculator check: <b>Poisson CD</b>.</p>')
    else:
        tab('<section class="table-page"><anchor id="T-poi2"/><h2 class="sec">T.4 Cumulative Poisson (cont.)</h2>')
    tab('<table class="ptab"><thead><tr><th>x \\ λ</th>' + "".join(f"<th>{l:g}</th>" for l in lams) + "</tr></thead><tbody>")
    for x in range(xmax + 1):
        row = [poic(x, l) for l in lams]
        tab(f"<tr><th>{x}</th>" + "".join(f"<td>{fmt(v)}</td>" for v in row) + "</tr>")
    tab("</tbody></table>")
    if gi != 0:
        tab("</section>")

open(OUT, "w").write("\n".join(h))
print("wrote", OUT)

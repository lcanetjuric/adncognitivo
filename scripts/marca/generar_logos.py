"""
Genera las piezas vectoriales de la marca ADNCognitivo.

Uso (solo si querés regenerar los logos; la web ya incluye los SVG listos):
    pip install fonttools brotli uharfbuzz
    npm install            # trae las fuentes Outfit desde @fontsource
    python3 scripts/marca/generar_logos.py

Todo el texto se convierte a trazos (paths), así los SVG se ven igual
en cualquier computadora aunque no tenga la tipografía instalada.
"""
import math
import os
import random

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTES = os.path.join(RAIZ, "node_modules", "@fontsource", "outfit", "files")
SALIDA = os.path.join(RAIZ, "src", "assets", "img", "marca")
os.makedirs(SALIDA, exist_ok=True)

NEGRO = "#1F1F1F"
MARFIL = "#F7F4EC"


# ---------------------------------------------------------------- tipografía
class Fuente:
    def __init__(self, peso):
        ruta = os.path.join(FUENTES, f"outfit-latin-{peso}-normal.woff2")
        self.tt = TTFont(ruta)
        self.glyphset = self.tt.getGlyphSet()
        self.upm = self.tt["head"].unitsPerEm
        buf = self.tt.reader.file
        # uharfbuzz necesita la fuente descomprimida
        import io
        tmp = io.BytesIO()
        self.tt.flavor = None
        self.tt.save(tmp)
        self.hbfont = hb.Font(hb.Face(tmp.getvalue()))
        self.orden = self.tt.getGlyphOrder()

    def texto(self, cadena, x, y, tam, espaciado=0.0):
        """Devuelve (path_d, ancho) del texto con línea base en y."""
        b = hb.Buffer()
        b.add_str(cadena)
        b.guess_segment_properties()
        hb.shape(self.hbfont, b, {"kern": True})
        esc = tam / self.upm
        partes = []
        cx = 0
        for info, pos in zip(b.glyph_infos, b.glyph_positions):
            nombre = self.orden[info.codepoint]
            pen = SVGPathPen(self.glyphset, ntos=lambda v: f"{v:.2f}")
            tp = TransformPen(pen, (esc, 0, 0, -esc, x + (cx + pos.x_offset) * esc, y))
            self.glyphset[nombre].draw(tp)
            partes.append(pen.getCommands())
            cx += pos.x_advance + espaciado * self.upm
        return " ".join(p for p in partes if p), cx * esc


# ------------------------------------------------------------ trazo de pincel
def ruido(semilla):
    r = random.Random(semilla)
    fases = [(r.uniform(0, 6.28), r.uniform(0.6, 1.4) * k) for k in (1, 2.3, 4.1)]

    def f(t):
        return sum(math.sin(t * w * 3 + p) / (i + 1) for i, (p, w) in enumerate(fases)) / 1.8

    return f


def pincel(puntos, ancho, semilla=1, variacion=0.35, afinar=True):
    """Convierte una polilínea en una forma rellena con ancho irregular
    (aspecto de marcador / pincel seco)."""
    n = len(puntos)
    if n < 2:
        return ""
    nz = ruido(semilla)
    izq, der = [], []
    for i, (x, y) in enumerate(puntos):
        a = puntos[max(i - 1, 0)]
        b = puntos[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        t = i / (n - 1)
        w = ancho * (1 + variacion * nz(t))
        if afinar:
            w *= 0.55 + 0.45 * min(1, min(t, 1 - t) * 7)
        w /= 2
        izq.append((x + nx * w, y + ny * w))
        der.append((x - nx * w, y - ny * w))
    contorno = izq + der[::-1]
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in contorno) + "Z"
    return d


def linea(p0, p1, semilla, pasos=24, curva=0.0, temblor=0.6):
    """Segmento levemente curvo y tembloroso entre dos puntos."""
    r = random.Random(semilla)
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = []
    for i in range(pasos + 1):
        t = i / pasos
        c = math.sin(math.pi * t) * curva
        j = r.uniform(-temblor, temblor) * (0.3 if i in (0, pasos) else 1)
        pts.append((x0 + dx * t + nx * (c + j), y0 + dy * t + ny * (c + j)))
    # suavizado simple
    s = [pts[0]]
    for i in range(1, len(pts) - 1):
        s.append(((pts[i - 1][0] + 2 * pts[i][0] + pts[i + 1][0]) / 4,
                  (pts[i - 1][1] + 2 * pts[i][1] + pts[i + 1][1]) / 4))
    s.append(pts[-1])
    return s


def rotar(p, c, ang):
    a = math.radians(ang)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


# ------------------------------------------------------------------- marco
def marco_escalonado(A, B, ancho, semilla=7, ang=-1.2):
    """Marco dibujado con dos rectángulos unidos por un escalón:
    A (detrás de ADN) y B (detrás de Cognitivo). Los bordes se pasan
    un poco en las esquinas, como un trazo hecho a mano."""
    ax0, ay0, ax1, ay1 = A
    bx0, by0, bx1, by1 = B
    c = ((ax0 + bx1) / 2, (ay0 + by1) / 2)
    segs = [
        ((ax0 - 4, ay0), (ax1 + 3, ay0 - 1), 1.5),
        ((ax1, ay0 - 3), (ax1 + 1, by0 + 3), 0),
        ((ax1 - 3, by0), (bx1 + 6, by0 + 1), -1.5),
        ((bx1, by0 - 5), (bx1 - 1, by1 + 5), 1.2),
        ((bx1 + 4, by1), (ax1 - 2, by1 + 1), 1.8),
        ((ax1, by1 + 3), (ax1 + 1, ay1 - 3), 0),
        ((ax1 + 3, ay1), (ax0 - 5, ay1 - 1), -1.2),
        ((ax0, ay1 + 5), (ax0 + 1, ay0 - 6), 1.0),
    ]
    out = []
    for i, (p0, p1, cv) in enumerate(segs):
        p0, p1 = rotar(p0, c, ang), rotar(p1, c, ang)
        largo = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        pts = linea(p0, p1, semilla + i, pasos=max(6, int(largo / 8)), curva=cv, temblor=0.5)
        out.append(pincel(pts, ancho, semilla + 11 * i, variacion=0.3))
    return out


# ------------------------------------------------------------------- hélice
def _eje(base, tope, curva):
    """Eje levemente curvo (bezier cuadrática) para que la hélice 'fluya'."""
    (x0, y0), (x1, y1) = base, tope
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    cx, cy = mx + (-dy / L) * curva, my + (dx / L) * curva

    def f(t):
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
        tx = 2 * (1 - t) * (cx - x0) + 2 * t * (x1 - cx)
        ty = 2 * (1 - t) * (cy - y0) + 2 * t * (y1 - cy)
        l = math.hypot(tx, ty) or 1
        return x, y, -ty / l, tx / l, tx / l, ty / l

    return f


def _hebras(base, tope, amplitud, vueltas, curva, N=200):
    eje = _eje(base, tope, curva)
    out = []
    for fase in (0, math.pi):
        h = []
        for i in range(N + 1):
            t = i / N
            x, y, nx, ny, _, _ = eje(t)
            ang = 2 * math.pi * vueltas * t + fase
            amp = amplitud * (0.72 + 0.28 * math.sin(math.pi * t))
            h.append(((x + nx * math.sin(ang) * amp, y + ny * math.sin(ang) * amp), math.cos(ang)))
        out.append(h)
    return out, eje


def helice(base, tope, amplitud=24, vueltas=2.4, ancho=6.5, semilla=3, fondo=MARFIL, color=NEGRO,
           curva=18, peldanos=True, paso_peldano=9):
    """Doble hélice dibujada a mano. Devuelve SVG (grupo)."""
    N = 200
    (h1, h2), eje = _hebras(base, tope, amplitud, vueltas, curva, N)
    partes = []
    peld = []
    if peldanos:
        k = 0
        for i in range(4, N - 3, paso_peldano):
            t = i / N
            s = math.sin(2 * math.pi * vueltas * t)
            if abs(s) < 0.5:
                continue
            (p, _), (q, _) = h1[i], h2[i]
            _, _, _, _, ux, uy = eje(t)
            a = (p[0] + (q[0] - p[0]) * 0.18, p[1] + (q[1] - p[1]) * 0.18)
            b = (p[0] + (q[0] - p[0]) * 0.82, p[1] + (q[1] - p[1]) * 0.82)
            a = (a[0] + ux * 3, a[1] + uy * 3)
            pts = linea(a, b, semilla + 100 + k, pasos=6, temblor=0.5)
            peld.append(pincel(pts, ancho * 0.62, semilla + 200 + k, variacion=0.25))
            k += 1
    partes.append(f'<g fill="{color}">' + "".join(f'<path d="{d}"/>' for d in peld) + "</g>")

    def tramos(h, delante_si):
        res, act = [], []
        for (p, z) in h:
            if (z > 0) == delante_si:
                act.append(p)
            else:
                if len(act) > 2:
                    res.append(act)
                act = []
        if len(act) > 2:
            res.append(act)
        return res

    atras = tramos(h1, False) + tramos(h2, False)
    delante = tramos(h1, True) + tramos(h2, True)
    ds_atras = [pincel(sg, ancho, semilla + 300 + 13 * j, variacion=0.35) for j, sg in enumerate(atras)]
    ds_del = [pincel(sg, ancho, semilla + 500 + 13 * j, variacion=0.35) for j, sg in enumerate(delante)]
    halo = "".join(f'<path d="{d}"/>' for d in ds_del)
    partes.append(f'<g fill="{color}">' + "".join(f'<path d="{d}"/>' for d in ds_atras) + "</g>")
    if fondo:
        partes.append(f'<g fill="{fondo}" stroke="{fondo}" stroke-width="{ancho*1.1:.1f}" stroke-linejoin="round">{halo}</g>')
    partes.append(f'<g fill="{color}">{halo}</g>')
    return "".join(partes)


def helice_halo(base, tope, amplitud, vueltas, ancho, fondo, curva=18):
    """Silueta gruesa del color de fondo: 'corta' el marco donde lo cruza la hélice."""
    (h1, h2), _ = _hebras(base, tope, amplitud, vueltas, curva)
    ds = ["M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p, _ in h) for h in (h1, h2)]
    return "".join(
        f'<path d="{d}" fill="none" stroke="{fondo}" stroke-width="{ancho*3:.1f}" stroke-linecap="round"/>' for d in ds
    )


def rayos(centro, angulos, r0, r1, ancho, semilla, color):
    out = []
    for i, a in enumerate(angulos):
        rad = math.radians(a)
        p0 = (centro[0] + math.cos(rad) * r0, centro[1] + math.sin(rad) * r0)
        p1 = (centro[0] + math.cos(rad) * r1, centro[1] + math.sin(rad) * r1)
        pts = linea(p0, p1, semilla + i, pasos=8, temblor=0.3, curva=0.6)
        out.append(pincel(pts, ancho, semilla + 7 * i, variacion=0.2))
    return f'<g fill="{color}">' + "".join(f'<path d="{d}"/>' for d in out) + "</g>"


def subrayado(x0, x1, y, ancho, semilla, color):
    pts = linea((x0, y + 2), (x1, y - 2), semilla, pasos=30, curva=-2.5, temblor=0.4)
    return f'<path fill="{color}" d="{pincel(pts, ancho, semilla, variacion=0.3)}"/>'


def svg(w, h, cuerpo, titulo, fondo=None, pad=0):
    bg = f'<rect width="100%" height="100%" fill="{fondo}"/>' if fondo else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2*pad:.0f} {h + 2*pad:.0f}" '
        f'role="img" aria-label="{titulo}"><title>{titulo}</title>'
        + (f'<rect x="{-pad}" y="{-pad}" width="{w + 2*pad:.0f}" height="{h + 2*pad:.0f}" fill="{fondo}"/>' if fondo else "")
        + cuerpo + "</svg>"
    )


# ------------------------------------------------------------------ piezas
F800 = Fuente(800)
F400 = Fuente(400)
F300 = Fuente(300)


def logo_horizontal(tinta=NEGRO, fondo_papel=MARFIL, fondo_rect=None, con_tagline=False):
    T = 120
    base_y = 250
    x_texto = 176
    d_adn, w_adn = F800.texto("ADN", x_texto, base_y, T, espaciado=-0.01)
    x_cog = x_texto + w_adn + 14
    d_cog, w_cog = F400.texto("Cognitivo", x_cog, base_y, T, espaciado=-0.005)
    cap = 0.709 * T
    A = (118, base_y - cap - 34, x_texto + w_adn + 6, base_y + 30)
    B = (A[2], base_y - cap - 20, x_cog + w_cog + 24, base_y + 46)
    marco = marco_escalonado(A, B, 6.2, semilla=21)
    partes = []
    partes.append(f'<g fill="{tinta}">' + "".join(f'<path d="{d}"/>' for d in marco) + "</g>")
    # hélice cruzando el borde izquierdo del marco
    hb_base, hb_tope = (58, 340), (212, 22)
    if fondo_papel:
        partes.append(helice_halo(hb_base, hb_tope, 38, 1.55, 7.6, fondo_papel, curva=-26))
    partes.append(helice(hb_base, hb_tope, amplitud=38, vueltas=1.55, ancho=7.6, semilla=5, fondo=fondo_papel,
                         color=tinta, curva=-26))
    partes.append(f'<path fill="{tinta}" d="{d_adn}"/>')
    partes.append(f'<path fill="{tinta}" d="{d_cog}"/>')
    # rayos
    partes.append(rayos((150, 64), [196, 226, 258], 52, 90, 6, 31, tinta))
    partes.append(rayos((B[2] - 30, B[1] + 6), [-100, -62, -24], 34, 66, 5.5, 41, tinta))
    ancho = B[2] + 70
    alto = 350
    cuerpo = "".join(partes)
    if con_tagline:
        d_tag, w_tag = F300.texto("FORMACIÓN Y RECURSOS BASADOS EN EVIDENCIA", 0, 0, 26, espaciado=0.32)
        xt = (A[0] + B[2]) / 2 - w_tag / 2
        d_tag, _ = F300.texto("FORMACIÓN Y RECURSOS BASADOS EN EVIDENCIA", xt, 392, 26, espaciado=0.32)
        cuerpo += f'<path fill="{tinta}" d="{d_tag}"/>'
        alto = 420
    return svg(ancho, alto, cuerpo, "ADNCognitivo", fondo=fondo_rect, pad=20 if fondo_rect else 0)


def logo_compacto(tinta=NEGRO, fondo_papel=MARFIL, fondo_rect=None, sticker=True):
    T = 104
    x = 150
    d_adn, w_adn = F800.texto("ADN", x, 150, T, espaciado=-0.01)
    d_cog, w_cog = F400.texto("Cognitivo", x - 36, 262, T * 0.86)
    A = (70, 58, x + w_adn + 22, 172)
    B = (A[0] + 10, 172, x - 36 + w_cog + 26, 298)
    partes = []
    # relleno tipo sticker (papel) detrás del marco
    relleno = fondo_papel or MARFIL
    if sticker:
        partes.append(
            f'<path fill="{relleno}" d="M{A[0]-10},{A[1]-6} L{A[2]+6},{A[1]-8} L{A[2]+8},{B[1]-4} L{B[2]+10},{B[1]} L{B[2]+8},{B[3]+10} L{B[0]-12},{B[3]+8} Z"/>'
        )
    # marco: forma en L invertida (dos cajas apiladas)
    c = ((A[0] + B[2]) / 2, (A[1] + B[3]) / 2)
    segs = [
        ((A[0] - 4, A[1]), (A[2] + 4, A[1] - 1), 1.5),
        ((A[2], A[1] - 4), (A[2] + 1, B[1] + 4), 0.5),
        ((A[2] - 4, B[1]), (B[2] + 5, B[1] + 1), -1),
        ((B[2], B[1] - 4), (B[2] - 1, B[3] + 5), 1.2),
        ((B[2] + 5, B[3]), (B[0] - 5, B[3] + 1), 1.5),
        ((B[0], B[3] + 4), (B[0] + 1, B[1]), 0),
        ((B[0], B[1]), (A[0], A[1] - 5), 0.6),
    ]
    ds = []
    for i, (p0, p1, cv) in enumerate(segs):
        p0, p1 = rotar(p0, c, -1.5), rotar(p1, c, -1.5)
        largo = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ds.append(pincel(linea(p0, p1, 60 + i, pasos=max(6, int(largo / 8)), curva=cv, temblor=0.5), 6, 70 + i, 0.3))
    partes.append(f'<g fill="{tinta}">' + "".join(f'<path d="{d}"/>' for d in ds) + "</g>")
    hb_base, hb_tope = (40, 318), (176, 22)
    partes.append(helice_halo(hb_base, hb_tope, 34, 1.5, 7, relleno, curva=-22))
    partes.append(helice(hb_base, hb_tope, amplitud=34, vueltas=1.5, ancho=7, semilla=9, fondo=relleno, color=tinta, curva=-22))
    partes.append(f'<path fill="{tinta}" d="{d_adn}"/><path fill="{tinta}" d="{d_cog}"/>')
    partes.append(rayos((104, 50), [196, 230, 264], 44, 76, 5.5, 51, tinta))
    return svg(B[2] + 30, 340, "".join(partes), "ADNCognitivo", fondo=fondo_rect, pad=18)


def isotipo(tinta=NEGRO, fondo_papel=MARFIL, fondo_rect=None, grueso=False):
    w = 9.5 if grueso else 7
    partes = [helice((84, 240), (122, 16), amplitud=40, vueltas=1.5, ancho=w, semilla=13, fondo=fondo_papel, color=tinta,
                     curva=-14, paso_peldano=11)]
    if not grueso:
        partes.append(rayos((102, 128), [168, 192, 212], 70, 96, 5, 81, tinta))
        partes.append(rayos((102, 128), [-12, 12, 34], 70, 96, 5, 91, tinta))
    return svg(204, 256, "".join(partes), "ADNCognitivo", fondo=fondo_rect, pad=0)


def logo_monocromo(tinta=NEGRO):
    T = 120
    d_adn, w_adn = F800.texto("ADN", 0, 110, T, espaciado=-0.01)
    d_cog, w_cog = F400.texto("Cognitivo", w_adn + 4, 110, T, espaciado=-0.005)
    cuerpo = f'<path fill="{tinta}" d="{d_adn}"/><path fill="{tinta}" d="{d_cog}"/>'
    cuerpo += subrayado(60, 60 + (w_adn + w_cog) * 0.34, 162, 7, 5, tinta)
    cuerpo += rayos((w_adn + w_cog - 70, 36), [-104, -70], 20, 50, 5, 3, tinta)
    return svg(w_adn + w_cog + 10, 180, cuerpo, "ADNCognitivo")


def favicon():
    # cuadrado negro con la hélice en marfil, trazo grueso para tamaños chicos
    cuerpo = f'<rect width="256" height="256" rx="36" fill="{NEGRO}"/>'
    cuerpo += helice((112, 236), (144, 20), amplitud=58, vueltas=1.0, ancho=25, semilla=13, fondo=NEGRO, color=MARFIL,
                     curva=-10, paso_peldano=34)
    return svg(256, 256, cuerpo, "ADNCognitivo")


def escribir(nombre, contenido):
    with open(os.path.join(SALIDA, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("✓", nombre)


if __name__ == "__main__":
    escribir("logo-horizontal.svg", logo_horizontal())
    escribir("logo-horizontal-tagline.svg", logo_horizontal(con_tagline=True))
    escribir("logo-horizontal-oscuro.svg", logo_horizontal(tinta=MARFIL, fondo_papel=NEGRO))
    escribir("logo-horizontal-fondo-oscuro.svg", logo_horizontal(tinta=MARFIL, fondo_papel=NEGRO, fondo_rect=NEGRO))
    escribir("logo-compacto.svg", logo_compacto())
    escribir("logo-compacto-oscuro.svg", logo_compacto(tinta=MARFIL, fondo_papel=NEGRO, sticker=True))
    escribir("isotipo.svg", isotipo())
    escribir("isotipo-oscuro.svg", isotipo(tinta=MARFIL, fondo_papel=NEGRO))
    escribir("logo-monocromo.svg", logo_monocromo())
    escribir("logo-monocromo-blanco.svg", logo_monocromo(tinta=MARFIL))
    escribir("favicon.svg", favicon())

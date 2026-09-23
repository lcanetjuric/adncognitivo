"""
Genera el lenguaje gráfico dibujado de ADNCognitivo (mismo trazo de
marcador que el logo): flechas, estrellas, rayos, subrayados, marcos
y los dibujos de cada área.

    python3 scripts/marca/generar_dibujos.py

Salida:
  src/_includes/dibujos.svg          → sprite que se inserta en cada página
  src/assets/img/dibujos/*.svg       → piezas sueltas (marcos, etc.)
"""
import math
import os
import random

from generar_logos import RAIZ, linea, pincel, helice

SPRITE = os.path.join(RAIZ, "src", "_includes", "dibujos.svg")
SUELTOS = os.path.join(RAIZ, "src", "assets", "img", "dibujos")
os.makedirs(SUELTOS, exist_ok=True)

W = 3.2  # grosor base (en un lienzo de 100)


def L(p0, p1, s, w=W, curva=0.0, temblor=0.35, afinar=True):
    largo = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    pts = linea(p0, p1, s, pasos=max(5, int(largo / 3)), curva=curva, temblor=temblor)
    return pincel(pts, w, s * 3 + 1, variacion=0.3, afinar=afinar)


def poli(puntos, s, w=W, temblor=0.3, cerrar=False):
    pts = list(puntos) + ([puntos[0]] if cerrar else [])
    out = []
    for i in range(len(pts) - 1):
        out.append(L(pts[i], pts[i + 1], s + i, w, temblor=temblor, afinar=False))
    return out


def curva_pts(fn, t0, t1, n=60):
    return [fn(t0 + (t1 - t0) * i / n) for i in range(n + 1)]


def C(fn, t0, t1, s, w=W, n=60, jitter=0.35, afinar=True):
    r = random.Random(s)
    pts = [(x + r.uniform(-jitter, jitter), y + r.uniform(-jitter, jitter)) for x, y in curva_pts(fn, t0, t1, n)]
    # suavizar
    sm = [pts[0]] + [((pts[i - 1][0] + 2 * pts[i][0] + pts[i + 1][0]) / 4, (pts[i - 1][1] + 2 * pts[i][1] + pts[i + 1][1]) / 4)
                     for i in range(1, len(pts) - 1)] + [pts[-1]]
    return pincel(sm, w, s * 7 + 3, variacion=0.3, afinar=afinar)


def elipse(cx, cy, rx, ry, s, w=W, a0=-0.3, extra=0.45, deriva=2.0):
    return C(lambda t: (cx + (rx + deriva * t / 6.28) * math.cos(t), cy + (ry + deriva * 0.6 * t / 6.28) * math.sin(t)),
             a0, a0 + 2 * math.pi + extra, s, w, n=90)


def punta(p, ang, s, largo=9, w=W, apertura=32):
    """Punta de flecha: dos trazos desde p."""
    out = []
    for k, sg in enumerate((1, -1)):
        a = math.radians(ang + 180 + sg * apertura)
        q = (p[0] + math.cos(a) * largo, p[1] + math.sin(a) * largo)
        out.append(L(p, q, s + k, w))
    return out


def simbolo(id_, vb, paths, titulo=None):
    t = f"<title>{titulo}</title>" if titulo else ""
    return f'<symbol id="{id_}" viewBox="{vb}">{t}' + "".join(f'<path d="{d}"/>' for d in paths) + "</symbol>"


S = {}

# --- signos sueltos -----------------------------------------------------------
def con_punta(fn, s, largo=11, w=W, t1=1.0):
    x1, y1 = fn(t1)
    x0, y0 = fn(t1 - 0.03)
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return [C(fn, 0, t1, s, w), *punta((x1, y1), ang, s + 1, largo, w)]


S["flecha-curva"] = ("0 0 100 60", con_punta(lambda t: (8 + 80 * t, 50 - 38 * math.sin(math.pi * t * 0.85)), 11))
S["flecha"] = ("0 0 60 24", [L((3, 13), (54, 11), 21, curva=-1.5), *punta((55, 11), 0, 22, 9)])
S["flecha-abajo"] = ("0 0 40 70", con_punta(lambda t: (14 + 12 * math.sin(t * 3), 4 + 58 * t), 31, 10))
S["externo"] = ("0 0 24 24", [L((5, 19), (19, 5), 41, 2.6), L((9, 4.5), (19.5, 4.5), 42, 2.6), L((19.5, 4.5), (19.5, 15), 43, 2.6)])
S["asterisco"] = ("0 0 40 40", [L((20, 3), (20, 37), 51, 3.6), L((5, 11), (35, 29), 52, 3.6), L((5, 29), (35, 11), 53, 3.6)])
S["rayos"] = ("0 0 50 40", [L((6, 34), (14, 20), 61, 3.4), L((20, 30), (24, 6), 62, 3.4), L((32, 32), (44, 16), 63, 3.4)])
S["rayos-2"] = ("0 0 50 50", [L((25, 20), (25, 4), 71, 3.4), L((13, 26), (3, 18), 72, 3.4), L((37, 26), (47, 18), 73, 3.4)])
S["zigzag"] = ("0 0 90 40", [
    L((4, 30), (60, 12), 81, 2.4), L((14, 34), (72, 16), 82, 2.4), L((24, 38), (86, 18), 83, 2.4),
    L((60, 12), (14, 34), 84, 1.6), L((72, 16), (24, 38), 85, 1.6)])
S["etiqueta"] = ("0 0 110 50", poli([(6, 12), (96, 8), (98, 16), (104, 16), (104, 34), (99, 34), (98, 42), (7, 44)], 91, 3, cerrar=True))
S["globo"] = ("0 0 100 70", [
    C(lambda t: (50 + 44 * math.cos(t), 30 + 24 * math.sin(t)), 2.2, 2.2 + 2 * math.pi - 0.5, 101, 3.2),
    L((20, 48), (10, 64), 102, 3.2), L((10, 64), (32, 52), 103, 3.2)])
S["pregunta"] = ("0 0 40 64", [
    C(lambda t: (20 + 13 * math.cos(t), 18 + 13 * math.sin(t)), -3.3, 0.9, 111, 4.2),
    C(lambda t: (28 - 8 * t, 29 + 14 * t), 0, 1, 112, 4.2, n=12),
    elipse(20, 55, 2.2, 2.2, 113, 3.8, extra=0.2, deriva=0)])
S["exclamacion"] = ("0 0 24 64", [L((13, 4), (11, 42), 121, 4.8), elipse(11, 55, 2.3, 2.3, 122, 4, extra=0.2, deriva=0)])
S["subrayado"] = ("0 0 200 16", [C(lambda t: (4 + 190 * t, 10 - 4 * math.sin(math.pi * t) + 2 * t), 0, 1, 131, 4.2, n=80)])
S["subrayado-doble"] = ("0 0 200 22", [
    C(lambda t: (4 + 190 * t, 8 - 3 * math.sin(math.pi * t)), 0, 1, 141, 3.6, n=80),
    C(lambda t: (30 + 150 * t, 17 - 2 * math.sin(math.pi * t) - t), 0, 1, 142, 3, n=60)])
S["circulo"] = ("0 0 200 80", [elipse(100, 40, 94, 33, 151, 3.4, a0=-2.6, extra=0.6, deriva=5)])
S["espiral"] = ("0 0 60 60", [C(lambda t: (30 + t * 1.9 * math.cos(t), 30 + t * 1.9 * math.sin(t)), 0.6, 4 * math.pi + 0.8, 161, 2.8, n=140)])
S["mas"] = ("0 0 30 30", [L((15, 4), (15, 26), 171, 3.6), L((4, 15), (26, 15), 172, 3.6)])
S["punto"] = ("0 0 20 20", [elipse(10, 10, 2.2, 2.2, 181, 6, extra=0.3, deriva=0)])

# --- interfaz -------------------------------------------------------------------
S["buscar"] = ("0 0 32 32", [elipse(13, 13, 9, 9, 201, 2.8, extra=0.4, deriva=0.6), L((20, 20), (29, 29), 202, 3.2)])
S["cuenta"] = ("0 0 32 32", [elipse(16, 10, 6, 6.5, 211, 2.8, extra=0.4, deriva=0.4),
                             C(lambda t: (16 + 12 * math.cos(t), 30 + 11 * math.sin(t)), math.pi + 0.1, 2 * math.pi - 0.1, 212, 2.8)])
S["menu"] = ("0 0 32 32", [L((4, 8), (28, 8), 221, 3.2), L((4, 16), (26, 16), 222, 3.2), L((4, 24), (28, 24), 223, 3.2)])
S["cerrar"] = ("0 0 32 32", [L((6, 6), (26, 26), 231, 3.4), L((26, 6), (6, 26), 232, 3.4)])
S["descarga"] = ("0 0 32 32", [L((16, 3), (16, 21), 241, 3), *punta((16, 21), 90, 242, 7, 3), *poli([(4, 20), (4, 28), (28, 28), (28, 20)], 243, 3)])

# --- dibujos de áreas (lienzo 100×100) -----------------------------------------
# Formación: libro abierto con rayitas de ideas
S["area-formacion"] = ("0 0 100 100", [
    C(lambda t: (50 - 38 * t, 36 - 7 * math.sin(math.pi * t)), 0, 1, 301),
    C(lambda t: (50 + 38 * t, 36 - 7 * math.sin(math.pi * t)), 0, 1, 302),
    L((12, 36), (12, 80), 303), L((88, 36), (88, 80), 304),
    C(lambda t: (12 + 38 * t, 80 + 6 * math.sin(math.pi * t)), 0, 1, 305),
    C(lambda t: (50 + 38 * t, 86 - 6 * math.sin(math.pi * t)), 0, 1, 306),
    L((50, 36), (50, 86), 307),
    L((20, 50), (42, 50), 308, 2.2), L((20, 59), (40, 60), 309, 2.2), L((20, 68), (38, 68), 310, 2.2),
    L((58, 50), (80, 49), 311, 2.2), L((58, 59), (78, 59), 312, 2.2),
    L((50, 22), (50, 10), 313, 2.8), L((36, 24), (29, 14), 314, 2.8), L((64, 24), (71, 14), 315, 2.8),
])
# Materiales: hojas apiladas con clip
S["area-materiales"] = ("0 0 100 100", [
    *poli([(30, 16), (84, 20), (80, 88), (26, 84)], 321, cerrar=True),
    *poli([(22, 22), (26, 22)], 322), L((26, 84), (18, 82), 323), L((18, 82), (22, 22), 324), L((22, 22), (30, 18), 325),
    L((38, 38), (70, 40), 326, 2.2), L((37, 50), (72, 52), 327, 2.2), L((36, 62), (66, 63), 328, 2.2), L((36, 73), (56, 74), 329, 2.2),
    C(lambda t: (72 + 6 * math.cos(t), 16 + 12 * math.sin(t) * (1 if t < math.pi else 0.8)), -math.pi / 2, 2 * math.pi, 330, 2.6),
    L((76, 20), (76, 30), 331, 2.4),
])
# Experiencias: cursor que hace clic + ondas
S["area-experiencias"] = ("0 0 100 100", [
    *poli([(40, 32), (40, 84), (52, 72), (60, 90), (68, 86), (60, 69), (76, 68)], 341, 3.2, cerrar=True),
    C(lambda t: (40 + 16 * math.cos(t), 32 + 16 * math.sin(t)), math.pi * 1.05, math.pi * 1.95, 342, 2.6),
    C(lambda t: (40 + 28 * math.cos(t), 32 + 28 * math.sin(t)), math.pi * 1.1, math.pi * 1.9, 343, 2.6),
    L((14, 34), (4, 34), 344, 2.8), L((18, 18), (10, 10), 345, 2.8),
])
# Publicaciones: revista / libro con líneas de texto y una estrella
S["area-publicaciones"] = ("0 0 100 100", [
    *poli([(26, 14), (78, 12), (80, 88), (24, 90)], 351, cerrar=True),
    L((34, 26), (70, 25), 352, 5), L((34, 38), (58, 37), 353, 2.2),
    L((34, 52), (70, 51), 354, 2), L((34, 60), (70, 60), 355, 2), L((34, 68), (68, 68), 356, 2), L((34, 76), (56, 76), 357, 2),
    L((16, 20), (16, 84), 358, 2.6), L((10, 26), (10, 78), 359, 2.2),
    L((88, 8), (88, 22), 360, 2.6), L((81, 15), (95, 15), 361, 2.6), L((83, 10), (93, 20), 362, 2.2), L((93, 10), (83, 20), 363, 2.2),
])
# Recursos: bandeja con flecha que baja
S["area-recursos"] = ("0 0 100 100", [
    L((50, 10), (50, 58), 371, 3.4), *punta((50, 60), 90, 372, 14, 3.4, 38),
    *poli([(12, 52), (14, 84), (86, 86), (88, 52)], 373),
    L((30, 70), (70, 71), 374, 2.2),
])
# Proyectos: nodos conectados (pensamiento en red, abstracto)
S["area-proyectos"] = ("0 0 100 100", [
    elipse(24, 30, 9, 9, 381), elipse(74, 22, 8, 8, 382), elipse(62, 74, 11, 11, 383), elipse(20, 76, 6, 6, 384),
    L((32, 28), (66, 23), 385, 2.4), L((29, 38), (54, 66), 386, 2.4), L((72, 30), (65, 63), 387, 2.4), L((26, 76), (51, 75), 388, 2.4),
])
# Hélice pequeña para detalles
S["helice"] = ("0 0 120 260", [])
helice_svg = helice((52, 244), (72, 16), amplitud=34, vueltas=1.5, ancho=7, semilla=13, fondo=None, curva=-14, paso_peldano=11)
helice_svg = helice_svg.replace('fill="#1F1F1F"', 'fill="currentColor"')

partes = []
for k, (vb, ps) in S.items():
    if k == "helice":
        partes.append(f'<symbol id="d-helice" viewBox="0 0 120 260">{helice_svg}</symbol>')
    else:
        partes.append(simbolo(f"d-{k}", vb, ps))

with open(SPRITE, "w", encoding="utf-8") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">'
            '<defs>' + "".join(partes) + "</defs></svg>\n")
print("✓ sprite", len(S), "dibujos")


# --- marcos para border-image (9 cortes) ---------------------------------------
def marco(nombre, color, semilla, grosor=3.4):
    # lienzo 120×120; corte 24 → esquinas dibujadas, lados que se estiran
    r = random.Random(semilla)
    j = lambda: r.uniform(-1.2, 1.2)
    pts = [(8 + j(), 9 + j()), (112 + j(), 7 + j()), (111 + j(), 112 + j()), (9 + j(), 111 + j())]
    ds = []
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        # prolongar un poco cada lado (se pasa de la esquina)
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy)
        a2 = (a[0] - dx / l * 4, a[1] - dy / l * 4)
        b2 = (b[0] + dx / l * 3, b[1] + dy / l * 3)
        ds.append(L(a2, b2, semilla + i, grosor, curva=r.uniform(-0.8, 0.8), temblor=0.25))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120">'
           + "".join(f'<path fill="{color}" d="{d}"/>' for d in ds) + "</svg>")
    with open(os.path.join(SUELTOS, nombre), "w") as f:
        f.write(svg)


marco("marco-1.svg", "#1F1F1F", 401)
marco("marco-2.svg", "#1F1F1F", 417)
marco("marco-fino.svg", "#1F1F1F", 433, 2.2)
marco("marco-claro.svg", "#F7F4EC", 449)

# cuadrícula de cuaderno (fondo de portadas sin imagen)
with open(os.path.join(SUELTOS, "cuadricula.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22">'
            '<path d="M22 0H0V22" fill="none" stroke="#D8D5CC" stroke-width="1"/></svg>')
# subrayado suelto para CSS
sub = S["subrayado"]
with open(os.path.join(SUELTOS, "subrayado.svg"), "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{sub[0]}" preserveAspectRatio="none">'
            + "".join(f'<path fill="#1F1F1F" d="{d}"/>' for d in sub[1]) + "</svg>")
with open(os.path.join(SUELTOS, "subrayado-coral.svg"), "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{sub[0]}" preserveAspectRatio="none">'
            + "".join(f'<path fill="#D99B8D" d="{d}"/>' for d in sub[1]) + "</svg>")
print("✓ marcos y fondos")

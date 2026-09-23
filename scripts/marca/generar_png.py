"""
Genera favicons PNG e imagen para redes (Open Graph) a partir de los SVG.
Requiere: pip install playwright  (y un Chromium disponible)
    python3 scripts/marca/generar_png.py
"""
import asyncio, os, pathlib
from playwright.async_api import async_playwright

RAIZ = pathlib.Path(__file__).resolve().parents[2]
MARCA = RAIZ / "src/assets/img/marca"
IMG = RAIZ / "src/assets/img"

def pagina(cuerpo, w, h, fondo="#F7F4EC"):
    return f"""<html><body style="margin:0;width:{w}px;height:{h}px;background:{fondo};display:grid;place-items:center;overflow:hidden">{cuerpo}</body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        async def foto(html, w, h, salida, transparente=False):
            pg = await b.new_page(viewport={"width": w, "height": h})
            tmp = MARCA / "_tmp.html"
            tmp.write_text(html, encoding="utf-8")
            await pg.goto(tmp.as_uri())
            await pg.wait_for_timeout(300)
            tmp.unlink()
            await pg.screenshot(path=str(salida), omit_background=transparente)
            await pg.close()
        fav = (MARCA / "favicon.svg").as_uri()
        for tam, nombre in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icono-512.png")]:
            await foto(pagina(f'<img src="{fav}" width="{tam}" height="{tam}">', tam, tam, "transparent"), tam, tam, MARCA / nombre, True)
        logo = (MARCA / "logo-horizontal-tagline.svg").as_uri()
        await foto(pagina(f'<img src="{logo}" style="width:880px">', 1200, 630), 1200, 630, IMG / "og-adncognitivo.png")
        # avatar cuadrado para Instagram / redes
        comp = (MARCA / "logo-compacto.svg").as_uri()
        await foto(pagina(f'<img src="{comp}" style="width:760px">', 1080, 1080), 1080, 1080, MARCA / "avatar-redes-1080.png")
        comp_o = (MARCA / "logo-compacto-oscuro.svg").as_uri()
        await foto(pagina(f'<img src="{comp_o}" style="width:760px">', 1080, 1080, "#1F1F1F"), 1080, 1080, MARCA / "avatar-redes-oscuro-1080.png")
        await b.close()
    print("PNG generados")

asyncio.run(main())

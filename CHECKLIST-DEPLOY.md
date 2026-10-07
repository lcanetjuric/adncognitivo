# Registro de deploy — adncognitivo en tac.com.ar/adncognitivo

Inicio: 2026-10-07. Contexto y decisiones: [DEPLOY-TAC.md](DEPLOY-TAC.md).

Cada paso se completa y se marca antes de pasar al siguiente. Al marcarlo, completar la fecha. La línea "Revertir" es cómo se deshace ese paso si todavía no se hizo el siguiente.

Producción (`tac.com.ar`) no cambia hasta el paso 12.

## Ya hecho

Código y decisiones, todavía sin commit ni publicación.

- [x] Reverse proxy descartado: en Ferozo `mod_proxy_http` no está disponible.
- [x] Sitio de edición publicado en Netlify: https://adncognitivo.netlify.app/
- [x] Deploy de Ferozo confirmado como manual (pull desde el panel, no hay webhook).
- [x] Plantillas con el filtro `url` de Eleventy (`--pathprefix=/adncognitivo/` solo en el build de la TAC).
- [x] `inscripcion.njk` apunta a `/adncognitivo-api/inscripcion.php`.
- [x] Escritos en disco, sin commit: `inscripcion.php`, el SQL de `adncognitivo_inscripciones`, `sync-tac.yml` y `check-adncognitivo-scope.yml`.

## Puesta en marcha

- [x] **1. Confirmar la casilla de aviso.** En `inscripcion.php`, `$avisoPara` está en `germanesalinas@gmail.com` para el primer deploy, y así se puede ver si el mail sale. La casilla definitiva, para un deploy posterior, es `adncognitivo@gmail.com`.
  - Fecha: 2026-10-07
  - Revertir: cambiar la constante. Todavía no está en ningún remoto.

- [x] **2. Commit local en ConicetTAC.** Desde `origin/master`, rama `adncognitivo-api`, solo estos archivos: `check-adncognitivo-scope.yml`, `var/www/html/adncognitivo-api/inscripcion.php`, `modificaciones/2026-09-29/crear_adncognitivo_inscripciones.sql.txt`. Sin push. `2026-09-01-deploy.md` no entra.
  - Fecha: 2026-10-07
  - Revertir: borrar la rama local. GitHub, Ferozo y la base no se enteran.

- [x] **3. Commit local en adncognitivo.** En la rama `incluir-en-tac`: plantillas, `main.css`, `package-lock.json`, `.gitignore`, `.github/workflows/sync-tac.yml`, `DEPLOY-TAC.md` y este archivo. Sin push.
  - Fecha: 2026-10-07
  - Revertir: quitar el commit de la rama. Netlify no se entera.

- [ ] **4. Pull request de la infraestructura, sin merge.** Push de `adncognitivo-api` y PR hacia `master` de `gercho25/ConicetTAC`.
  - Fecha:
  - Revertir: cerrar el PR y borrar la rama remota. `master` sigue igual.

- [ ] **5. Merge de esa infraestructura a `master`.** No apretar el pull de Ferozo.
  - Fecha:
  - Revertir: revert del merge en GitHub. El sitio sigue sirviendo lo que Ferozo tiene hoy.

- [ ] **6. Migración SQL en producción.** Correr `modificaciones/2026-09-29/crear_adncognitivo_inscripciones.sql.txt` en la base `sitioweb`.
  - Fecha:
  - Revertir: `DROP TABLE adncognitivo_inscripciones;`

- [ ] **7. Secreto `TAC_PUSH_TOKEN`.** En `lcanetjuric/adncognitivo` → Settings → Secrets and variables → Actions. Token de GitHub con escritura sobre `gercho25/ConicetTAC`.
  - Fecha:
  - Revertir: borrar el secreto. Sin él, el Action de sync no puede abrir el PR.

- [ ] **8. Push a `main` de adncognitivo.** Dispara el build de Netlify y, si el secreto ya está, el Action que abre el PR `sync/adncognitivo`. En Netlify el prefijo no se aplica. El formulario de ese sitio pasa a postear a `/adncognitivo-api/inscripcion.php`, que en `adncognitivo.netlify.app` no existe: las inscripciones pasan a hacerse solo desde `tac.com.ar`.
  - Fecha:
  - Revertir: revert del commit en `main`. Netlify vuelve a publicar la versión anterior.

- [ ] **9. Revisar el PR `sync/adncognitivo`.** Tiene que tocar solo `var/www/html/adncognitivo/` y el chequeo de alcance tiene que pasar. No mergear si el chequeo falla.
  - Fecha:
  - Revertir: cerrar el PR.

- [ ] **10. Marcar el chequeo como obligatorio.** En `gercho25/ConicetTAC` → Settings → Branches → protección de `master` → exigir el check de `check-adncognitivo-scope.yml`. GitHub recién lo ofrece en la lista después de que el workflow corrió al menos una vez (paso 9).
  - Fecha:
  - Revertir: sacar ese check de la regla de protección.

- [ ] **11. Merge del PR de sync a `master`.** Sigue sin deploy de Ferozo.
  - Fecha:
  - Revertir: revert del merge en GitHub.

- [ ] **12. Pull en Ferozo.** Panel → Mi sitio web → Git → acción de pull sobre ConicetTAC. Recién ahí `tac.com.ar` recibe la API y la copia estática.
  - Fecha:
  - Revertir: revert de los merges en `master` y otro pull en Ferozo. La tabla del paso 6 sigue existiendo hasta el `DROP TABLE`.

- [ ] **13. Prueba en `tac.com.ar/adncognitivo/`.** Navegación, una inscripción real (fila en `adncognitivo_inscripciones` y mail a la casilla del paso 1), y que la home de WordPress, `/v2/` y `/evaluacion/` siguen igual.
  - Fecha:
  - Revertir: el del paso 12, más el `DROP TABLE` si se quiere sacar también la fila de prueba.

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
  - Revertir: cambiar la constante en la rama. Ya está en el PR, no en `master`.

- [x] **2. Commit local en ConicetTAC.** Desde `origin/master`, rama `adncognitivo-api`, solo estos archivos: `check-adncognitivo-scope.yml`, `var/www/html/adncognitivo-api/inscripcion.php`, `modificaciones/2026-09-29/crear_adncognitivo_inscripciones.sql.txt`. Sin push. `2026-09-01-deploy.md` no entra.
  - Fecha: 2026-10-07
  - Revertir: borrar la rama local. GitHub, Ferozo y la base no se enteran.

- [x] **3. Commit local en adncognitivo.** En la rama `incluir-en-tac`: plantillas, `main.css`, `package-lock.json`, `.gitignore`, `.github/workflows/sync-tac.yml`, `DEPLOY-TAC.md` y este archivo. Sin push.
  - Fecha: 2026-10-07
  - Revertir: quitar el commit de la rama. Netlify no se entera.

- [x] **4. Pull request de la infraestructura, sin merge.** Push de `adncognitivo-api` y PR hacia `master` de `gercho25/ConicetTAC`: https://github.com/gercho25/ConicetTAC/pull/1
  - Fecha: 2026-10-07
  - Revertir: cerrar el PR y borrar la rama remota. `master` sigue igual.

- [x] **5. Merge de esa infraestructura a `master`.** Commit `68bfad1a`. No apretar el pull de Ferozo.
  - Fecha: 2026-10-07
  - Revertir: revert del merge en GitHub. El sitio sigue sirviendo lo que Ferozo tiene hoy.

- [x] **6. Migración SQL en producción.** Correr `modificaciones/2026-09-29/crear_adncognitivo_inscripciones.sql.txt` en la base `sitioweb`.
  - Fecha: 2026-10-07
  - Revertir: `DROP TABLE adncognitivo_inscripciones;`

- [x] **7. Secreto `TAC_PUSH_TOKEN`.** En `lcanetjuric/adncognitivo` → Settings → Secrets and variables → Actions, pestaña Secrets. Token de GitHub con escritura sobre `gercho25/ConicetTAC`.
  - Fecha: 2026-10-07
  - Revertir: borrar el secreto. Sin él, el Action de sync no puede abrir el PR.

- [x] **8. Push a `main` de adncognitivo.** Dispara el build de Netlify y, si el secreto ya está, el Action que abre el PR `sync/adncognitivo`. En Netlify el prefijo no se aplica. El formulario de ese sitio pasa a postear a `/adncognitivo-api/inscripcion.php`, que en `adncognitivo.netlify.app` no existe: las inscripciones pasan a hacerse solo desde `tac.com.ar`.
  - Fecha: 2026-10-07. `main` quedó en `052995e`. Action [37663845110](https://github.com/lcanetjuric/adncognitivo/actions/runs/37663845110) en verde.
  - Revertir: revert del commit en `main`. Netlify vuelve a publicar la versión anterior.

- [x] **9. Revisar el PR `sync/adncognitivo`.** Tiene que tocar solo `var/www/html/adncognitivo/` y el chequeo de alcance tiene que pasar. No mergear si el chequeo falla. https://github.com/gercho25/ConicetTAC/pull/2 — el chequeo `check-scope` pasó y el diff solo agrega archivos bajo `var/www/html/adncognitivo/`.
  - Fecha: 2026-10-07
  - Revertir: cerrar el PR.

- [x] **10. Marcar el chequeo como obligatorio.** No se puede: `gercho25/ConicetTAC` es privado y el plan gratuito no incluye protección de ramas (GitHub pide Pro, o hacer el repo público). El workflow igual corre en cada PR. El freno queda en mirar que `check-scope` esté en verde antes de mergear, como en el paso 9.
  - Fecha: 2026-10-07
  - Revertir: no queda una regla activa que sacar.

- [x] **11. Merge del PR de sync a `master`.** Commit `9c70e1db`. Sigue sin deploy de Ferozo. https://github.com/gercho25/ConicetTAC/pull/2
  - Fecha: 2026-10-07
  - Revertir: revert del merge en GitHub.

- [x] **12. Pull de Git sobre `public_html`.** No se reintenta. Desplegar respondió `fatal: not a git repository`. Esa entrada de Ferozo no se vuelve a usar: un clone del repo entero no coincide con la web. Backup de `public_html` hecho el 2026-10-07.
  - Fecha: 2026-10-07
  - Revertir: no hubo cambios en el servidor.

- [ ] **13. Rama `deploy`.** El Action de `main` compila con `/adncognitivo/` y reemplaza la rama `deploy` de `lcanetjuric/adncognitivo`. La raíz de esa rama es el sitio. Todavía no está conectada a Ferozo.
  - Fecha:
  - Revertir: borrar la rama `deploy`. `main` y `tac.com.ar` no cambian por eso.

- [ ] **14. Git nuevo en Ferozo.** Directorio vacío `public_html/adncognitivo`, repo `lcanetjuric/adncognitivo`, rama `deploy`. Hay que agregar la clave SSH de Ferozo en ese repo. No tocar la entrada que apunta a `public_html`.
  - Fecha:
  - Revertir: borrar esa entrada de Git. La carpeta del sitio se puede vaciar. El resto de `public_html` no entra.

- [ ] **15. Webhook de Ferozo** para que cada actualización de `deploy` haga el pull sola.
  - Fecha:
  - Revertir: borrar el webhook en GitHub.

- [ ] **16. Subir `inscripcion.php` una vez** a `public_html/adncognitivo-api/`. No cambia con el CMS.
  - Fecha:
  - Revertir: borrar esa carpeta.

- [ ] **17. Prueba en `tac.com.ar/adncognitivo/`.** Navegación, una inscripción real (fila en `adncognitivo_inscripciones` y mail a la casilla del paso 1), y que la home de WordPress, `/v2/` y `/evaluacion/` siguen igual.
  - Fecha:
  - Revertir: borrar `public_html/adncognitivo` y `public_html/adncognitivo-api`, más el `DROP TABLE` si se quiere sacar también la fila de prueba.

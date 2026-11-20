<div align="center">

<p>
  <a href="README.md">English</a> ·
  <a href="README.pt.md">Português</a> ·
  <strong>Español</strong>
</p>

# 🛡️ Steam Reviews Toxicity List

**Lista multilingüe de toxicidad y violaciones de TOS curada a partir de reseñas de Steam para blindar pipelines de LLMs antes de la inferencia.**

<p>
  <img src="https://img.shields.io/badge/Idiomas-EN%20%7C%20PT%20%7C%20ES-blue" alt="Idiomas: EN | PT | ES" />
  <img src="https://img.shields.io/badge/Enfoque-LLM%20TOS%20Shield-purple" alt="Enfoque: LLM TOS Shield" />
  <img src="https://img.shields.io/badge/Acci%C3%B3n-Remover-red" alt="Acción: Remover" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licencia-MIT-green" alt="Licencia: MIT" /></a>
</p>

</div>

> **Aviso de Contenido (Content Warning):** Este repositorio contiene términos ofensivos, discurso de odio y lenguaje sexual explícito listados **estrictamente con fines defensivos de moderación de contenido, investigación de seguridad y filtrado previo a LLMs**. El proyecto no respalda ningún término incluido y no debe utilizarse para acoso ni generación de contenido abusivo.
>
> *Proyecto independiente y open source, sin afiliación con Valve/Steam, Google, OpenAI, Anthropic ni ningún proveedor de IA.*

---

## Objetivo

Actuar como una **capa local y determinista de blindaje previo a la inferencia**, detectando y eliminando textos nocivos generados por usuarios (reseñas de Steam, comentarios, chats, tickets) **antes** de enviarlos a APIs de LLMs con Términos de Servicio estrictos — como **Google Gemini** (incluidos los modelos de la familia `gemini-decision`), **OpenAI**, entre otros.

### Problemas y riesgos que resuelve

Al enviar grandes volúmenes de contenido generado por usuarios (UGC) directamente a LLMs comerciales, tu sistema queda expuesto a riesgos operativos y de cuenta:

- **Bloqueos HTTP 400 (`PROHIBITED_CONTENT` / `TOS Violation`):** el contenido extremo es rechazado en la entrada, rompiendo pipelines por lotes, deteniendo colas y desperdiciando reintentos.
- **Riesgo de restricción, suspensión o baneo del proyecto/cuenta:** el envío recurrente de contenido que infringe los Términos de Servicio puede activar sistemas automáticos antiabuso del proveedor, provocando **limitación de cuota, bloqueo de la API key, suspensión del proyecto o baneo permanente de la cuenta**.
- **Desperdicio de latencia y costo:** consumir tokens y tiempo de red en textos que inevitablemente serán bloqueados o no aportan valor analítico.
- **Falsos positivos de listas genéricas:** muchas listas públicas bloquean palabras habituales en videojuegos o lenguaje coloquial (como `die`, `morrer`, `aviso`, `caralho`). Esta lista de TOS se enfoca **únicamente en términos de alto riesgo real**, dejando los términos leves o contextuales para capas de censura separadas.

---

## Estructura del Proyecto

```text
├── lists/
│   ├── tos/
│   │   ├── en.csv          # Términos en Inglés
│   │   ├── pt.csv          # Términos en Portugués
│   │   └── es.csv          # Términos en Español
│   └── lista_tos.csv       # Lista consolidada (generada desde lists/tos/*.csv)
├── scripts/
│   └── build_and_validate.py
├── .github/workflows/
│   └── validate.yml        # Validación automática en Pull Requests
├── README.md               # English
├── README.pt.md            # Português
├── README.es.md            # Español
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

Cada idioma cuenta con su propio CSV en `lists/tos/` para facilitar las revisiones y contribuciones de hablantes nativos. El archivo `lists/lista_tos.csv` consolida automáticamente todos los idiomas.

---

## Esquema de Columnas

Todos los archivos CSV utilizan codificación UTF-8 y comparten exactamente las mismas 5 columnas:

| Columna | Obligatoria | Descripción | Valores esperados |
| :--- | :---: | :--- | :--- |
| `termo` | Sí | Palabra o expresión exacta (en minúsculas) a bloquear antes de la inferencia. | Ej.: `nigger`, `maricones`, `a las mujeres se les pega` |
| `classificacao` | Sí | Acción recomendada para el filtro local. En la lista de TOS, **todas las entradas deben ser `remover`** (descartar/bloquear el texto antes de llamar a la API). | `remover` |
| `linguagem` | Sí | Código ISO 639-1 del idioma. Debe coincidir con el nombre del archivo `lists/tos/<linguagem>.csv`. | `en`, `pt`, `es`, `fr`, `de`, etc. |
| `motivo` | Sí | Motivo técnico por el cual el término está incluido. | `TOS Violation` |
| `categoria` | Sí | Categoría de infracción de política asociada al término. | `Discurso de ódio (Racismo)`, `Discurso de ódio (Homofobia)`, `Discurso de ódio (Capacitismo)`, `Violência / Discurso de ódio (Misoginia)`, `Conteúdo sexual explícito`, `Ameaça / Violência` |

---

## Validación y Build Local

Después de editar cualquier archivo en `lists/tos/`, ejecuta el script para validar el formato y regenerar `lists/lista_tos.csv`:

```bash
python scripts/build_and_validate.py
```

Para validar sin modificar archivos (el mismo comando ejecutado en CI):

```bash
python scripts/build_and_validate.py --check
```

---

## Colabora con el Proyecto

La jerga en internet cambia rápido y cada idioma tiene sus propias variantes y formas de evasión. **Tu contribución ayuda a toda la comunidad a mantener pipelines de IA más seguros y estables.**

Puedes colaborar de tres maneras:
1. **Agregando nuevos términos** en un idioma existente (`lists/tos/es.csv`, `en.csv`, `pt.csv`).
2. **Añadiendo un nuevo idioma** creando un archivo `lists/tos/<codigo_iso>.csv` (ej.: `fr.csv`, `de.csv`, `it.csv`).
3. **Reportando falsos positivos** mediante una Issue si algún término bloquea reseñas legítimas.

Lee la guía rápida en [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir tu Pull Request.

---

## Licencia

Distribuido bajo la licencia [MIT](LICENSE).

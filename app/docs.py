from collections.abc import Iterable

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRoute

from app import settings


DOC_MODULES = [
    {
        "slug": "auth",
        "title": "Auth",
        "description": "Autenticacion y registro de usuarios.",
        "prefixes": ("/auth",),
    },
    {
        "slug": "usuarios",
        "title": "Usuarios",
        "description": "Perfil y administracion de usuarios.",
        "prefixes": ("/api/usuarios",),
    },
    {
        "slug": "finanzas",
        "title": "Finanzas",
        "description": "Bancos, cuentas, categorias y movimientos.",
        "prefixes": ("/api/finanzas",),
    },
    {
        "slug": "compras",
        "title": "Compras",
        "description": "Compras, detalles, locales y vinculos con movimientos.",
        "prefixes": ("/api/compras",),
    },
    {
        "slug": "catalogo",
        "title": "Catalogo",
        "description": "Productos, marcas, categorias y subcategorias.",
        "prefixes": ("/api/catalogo",),
    },
    {
        "slug": "nutricion",
        "title": "Nutricion",
        "description": "Consumos, metas, peso y tablas nutricionales.",
        "prefixes": ("/api/nutricion",),
    },
    {
        "slug": "entrenamientos",
        "title": "Entrenamientos",
        "description": "Ejercicios, gimnasio, fuerza y series.",
        "prefixes": ("/api/entrenamientos",),
    },
    {
        "slug": "lecturas",
        "title": "Lecturas",
        "description": "Libros y registros de lectura.",
        "prefixes": ("/api/lecturas",),
    },
]


OPENAPI_TAGS = [
    {"name": "Auth", "description": "Autenticacion y registro."},
    {"name": "Usuario", "description": "Perfil y administracion de usuarios."},
    {"name": "Finanzas", "description": "Operaciones del dominio de finanzas."},
    {"name": "Compras", "description": "Operaciones del dominio de compras."},
    {"name": "Catalogo", "description": "Operaciones del dominio de catalogo."},
    {"name": "Nutricion", "description": "Operaciones del dominio de nutricion."},
    {"name": "Entrenamientos", "description": "Operaciones del dominio de entrenamientos."},
    {"name": "Lecturas", "description": "Operaciones del dominio de lecturas."},
]


def install_docs(app: FastAPI) -> None:
    app.state.module_openapi_cache = {}

    @app.get("/", include_in_schema=False)
    def docs_root_redirect():
        return RedirectResponse(url="/docs", status_code=307)

    @app.get("/docs", include_in_schema=False)
    def docs_menu():
        return HTMLResponse(_build_docs_menu_html())

    @app.get("/docs/global", include_in_schema=False)
    def docs_global():
        return _swagger_with_nav(
            openapi_url="/openapi.json",
            title=f"{settings.TITLE_API} - Documentacion Global",
        )

    @app.get("/openapi.json", include_in_schema=False)
    def openapi_global():
        return app.openapi()

    @app.get("/redoc", include_in_schema=False)
    def docs_redoc():
        return _redoc_with_nav(
            openapi_url="/openapi.json",
            title=f"{settings.TITLE_API} - ReDoc",
        )

    for module in DOC_MODULES:
        _register_module_docs(app, module)


def use_custom_openapi(app: FastAPI) -> None:
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        app.openapi_schema = get_openapi(
            title=settings.TITLE_API,
            version=settings.VERSION_API,
            description=(
                "API encargada de realizar registros a areas como finanzas, "
                "deportes, habitos, compras y mas."
            ),
            routes=app.routes,
            tags=OPENAPI_TAGS,
        )
        return app.openapi_schema

    app.openapi = custom_openapi


def _register_module_docs(app: FastAPI, module: dict[str, object]) -> None:
    slug = str(module["slug"])
    title = str(module["title"])

    @app.get(f"/docs/{slug}", include_in_schema=False, name=f"docs_{slug}")
    def module_docs(slug: str = slug, title: str = title):
        return _swagger_with_nav(
            openapi_url=f"/openapi/{slug}.json",
            title=f"{settings.TITLE_API} - {title}",
        )

    @app.get(f"/openapi/{slug}.json", include_in_schema=False, name=f"openapi_{slug}")
    def module_openapi(slug: str = slug):
        return get_module_openapi(app, slug)


def get_module_openapi(app: FastAPI, slug: str) -> dict:
    cache = app.state.module_openapi_cache
    if slug in cache:
        return cache[slug]

    module = next((item for item in DOC_MODULES if item["slug"] == slug), None)
    if not module:
        raise ValueError(f"Modulo de documentacion no encontrado: {slug}")

    routes = _filter_routes_by_prefixes(app.routes, module["prefixes"])
    schema = get_openapi(
        title=f"{settings.TITLE_API} - {module['title']}",
        version=settings.VERSION_API,
        description=str(module["description"]),
        routes=routes,
    )
    cache[slug] = schema
    return schema


def _filter_routes_by_prefixes(routes: Iterable, prefixes: tuple[str, ...]) -> list[APIRoute]:
    return [
        route
        for route in routes
        if isinstance(route, APIRoute)
        and route.include_in_schema
        and any(route.path.startswith(prefix) for prefix in prefixes)
    ]


def _build_docs_menu_html() -> str:
    cards = "\n".join(
        (
            f"""
            <a class="card" href="/docs/{module['slug']}">
                <span class="eyebrow">Modulo</span>
                <h2>{module['title']}</h2>
                <p>{module['description']}</p>
            </a>
            """
        ).strip()
        for module in DOC_MODULES
    )

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{settings.TITLE_API} - Documentacion</title>
        <style>
            :root {{
                --bg: #f4efe6;
                --panel: rgba(255, 252, 246, 0.9);
                --ink: #1f2937;
                --muted: #5b6470;
                --line: rgba(31, 41, 55, 0.12);
                --accent: #0f766e;
                --accent-2: #d97706;
                --shadow: 0 18px 45px rgba(31, 41, 55, 0.12);
            }}
            * {{
                box-sizing: border-box;
            }}
            body {{
                margin: 0;
                font-family: "Segoe UI", sans-serif;
                color: var(--ink);
                background:
                    radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 32%),
                    radial-gradient(circle at top right, rgba(217, 119, 6, 0.16), transparent 26%),
                    linear-gradient(180deg, #fcfaf6 0%, var(--bg) 100%);
                min-height: 100vh;
            }}
            .shell {{
                max-width: 1120px;
                margin: 0 auto;
                padding: 48px 24px 64px;
            }}
            .hero {{
                display: grid;
                gap: 20px;
                margin-bottom: 32px;
            }}
            .badge {{
                width: fit-content;
                padding: 8px 14px;
                border-radius: 999px;
                background: rgba(15, 118, 110, 0.1);
                color: var(--accent);
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }}
            h1 {{
                margin: 0;
                font-size: clamp(2.2rem, 5vw, 4.2rem);
                line-height: 1;
                max-width: 10ch;
            }}
            .lead {{
                margin: 0;
                max-width: 62ch;
                color: var(--muted);
                font-size: 1.05rem;
                line-height: 1.7;
            }}
            .actions {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
            }}
            .button {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                border-radius: 14px;
                padding: 12px 18px;
                font-weight: 700;
                transition: transform 0.15s ease, box-shadow 0.15s ease;
            }}
            .button:hover {{
                transform: translateY(-1px);
                box-shadow: var(--shadow);
            }}
            .button-primary {{
                background: var(--ink);
                color: white;
            }}
            .button-secondary {{
                background: var(--panel);
                color: var(--ink);
                border: 1px solid var(--line);
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
            }}
            .card {{
                text-decoration: none;
                color: inherit;
                background: var(--panel);
                border: 1px solid var(--line);
                border-radius: 22px;
                padding: 22px;
                box-shadow: var(--shadow);
                min-height: 180px;
                display: grid;
                align-content: start;
                gap: 12px;
                transition: transform 0.18s ease, border-color 0.18s ease;
            }}
            .card:hover {{
                transform: translateY(-4px);
                border-color: rgba(15, 118, 110, 0.35);
            }}
            .eyebrow {{
                color: var(--accent-2);
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.78rem;
                font-weight: 700;
            }}
            .card h2 {{
                margin: 0;
                font-size: 1.25rem;
            }}
            .card p {{
                margin: 0;
                color: var(--muted);
                line-height: 1.6;
            }}
            @media (max-width: 640px) {{
                .shell {{
                    padding: 28px 16px 40px;
                }}
                .card {{
                    min-height: 160px;
                }}
            }}
        </style>
    </head>
    <body>
        <main class="shell">
            <section class="hero">
                <span class="badge">Documentacion API</span>
                <h1>{settings.TITLE_API}</h1>
                <p class="lead">
                    Elige un modulo para navegar una documentacion mas acotada y facil de recorrer.
                    Si prefieres ver toda la API junta, tambien tienes acceso al Swagger global.
                </p>
                <div class="actions">
                    <a class="button button-primary" href="/docs/global">Ver Swagger global</a>
                    <a class="button button-secondary" href="/openapi.json">Descargar OpenAPI global</a>
                </div>
            </section>
            <section class="grid">
                {cards}
            </section>
        </main>
    </body>
    </html>
    """


def _swagger_with_nav(*, openapi_url: str, title: str) -> HTMLResponse:
    swagger_response = get_swagger_ui_html(openapi_url=openapi_url, title=title)
    html = swagger_response.body.decode("utf-8")
    nav = """
    <style>
        .docs-home-link {
            position: fixed;
            top: 16px;
            right: 16px;
            z-index: 10000;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 14px;
            border-radius: 999px;
            background: #111827;
            color: #ffffff;
            text-decoration: none;
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 700;
            box-shadow: 0 10px 24px rgba(17, 24, 39, 0.18);
        }
        .docs-home-link:hover {
            background: #0f766e;
        }
        @media (max-width: 640px) {
            .docs-home-link {
                top: auto;
                right: 12px;
                bottom: 12px;
            }
        }
    </style>
    <a class="docs-home-link" href="/docs">Volver al menu</a>
    """
    html = html.replace("</body>", f"{nav}</body>")
    return HTMLResponse(
        content=html,
        status_code=swagger_response.status_code,
        media_type=swagger_response.media_type,
    )


def _redoc_with_nav(*, openapi_url: str, title: str) -> HTMLResponse:
    redoc_response = get_redoc_html(openapi_url=openapi_url, title=title)
    html = redoc_response.body.decode("utf-8")
    nav = """
    <style>
        .docs-home-link {
            position: fixed;
            top: 16px;
            right: 16px;
            z-index: 10000;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 14px;
            border-radius: 999px;
            background: #111827;
            color: #ffffff;
            text-decoration: none;
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 700;
            box-shadow: 0 10px 24px rgba(17, 24, 39, 0.18);
        }
        .docs-home-link:hover {
            background: #0f766e;
        }
        @media (max-width: 640px) {
            .docs-home-link {
                top: auto;
                right: 12px;
                bottom: 12px;
            }
        }
    </style>
    <a class="docs-home-link" href="/docs">Volver al menu</a>
    """
    html = html.replace("</body>", f"{nav}</body>")
    return HTMLResponse(
        content=html,
        status_code=redoc_response.status_code,
        media_type=redoc_response.media_type,
    )

AUTH_SCHEMA = "auth"
USUARIOS_SCHEMA = "usuarios"
HABITOS_SCHEMA = "habitos"
LECTURAS_SCHEMA = "lecturas"
FINANZAS_SCHEMA = "finanzas"
ENTRENAMIENTOS_SCHEMA = "entrenamientos"


def table_ref(schema: str, table: str) -> str:
    return f"{schema}.{table}"

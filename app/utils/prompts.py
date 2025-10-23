prompt_classify = """Actúa como un asistente que clasifica mensajes en categorías.
    Mensaje: "{}"
    Devuelve en formato JSON con las siguientes claves:
    - categoria: tipo de actividad (entrenamiento_fuerza, entrenamiento_aerobico, habito_salud, otro)
    - confianza: valor numérico entre 0 y 1"""